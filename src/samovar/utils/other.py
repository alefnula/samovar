__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
import json
import glob
import urllib
import logging

try:
    import urlparse
    import urllib2 as request
except:
    from urllib import request
    import urllib.parse as urlparse 

# tea imports
from tea import shutil

logger = logging.getLogger(__name__)


def rotate_logfile(logfile):
    if os.path.isfile(logfile):
        files = {}
        for f in glob.glob(logfile + '.*'):
            try:
                num = int(f.rpartition('.')[-1])
                files[num] = f
            except:
                pass
        for num in sorted(files, reverse=True):
            shutil.move('%s.%s' % (logfile, num), '%s.%s' % (logfile, num + 1))
        shutil.move(logfile, '%s.0' % logfile)


def find_exe(prefix, path, alternative):
    if prefix is None:
        found = glob.glob(os.path.join(*path))
        if len(found) == 1:
            return found[0]
    elif prefix.lower() == 'pf':
        for pf in ('ProgramFiles', 'ProgramFiles(x86)', 'ProgramW6432'):
            found = glob.glob(os.path.join(os.environ.get(pf, ''), *path))
            if len(found) == 1:
                return found[0]
    elif prefix.lower() == 'win':
        windir = os.environ.get('WINDIR', 'C:\\windows')
        found = glob.glob(os.path.join(windir, *path))
        if len(found) == 1:
            return found[0]
    else:
        logger.warning('find_exe: Unknown prefix "%s"' % prefix)
    logger.warning('find_exe: %s not found on the system!' % alternative)
    return alternative


def urlfetch(url, username, password):
    '''Return (ok, data)'''
    password_manager = request.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, username, password)
    auth_handler = request.HTTPBasicAuthHandler(password_manager)
    opener = request.build_opener(auth_handler)
    error = None
    logger.debug('Fetching %s' % url)
    for _ in range(5):
        try:
            response = opener.open(url)
            return True, response.read()
        except Exception as e:
            error = str(e)
            logger.debug('Could not get: "%s". Retrying.' % url)
    logger.warning('Failed to get: "%s"' % url)
    return False, error


def get_repos_from_checkout(checkout_path, url, username, password, cls):
    repos = []
    parsed = urlparse.urlparse(url)
    for root, directories, _ in os.walk(checkout_path):
        if '.hg' in directories:
            name = root.replace(checkout_path, '').replace('\\', '/').strip('/')
            repos.append(cls(name=name, path=root,
                             source=urlparse.urlunparse(parsed._replace(path='/'.join([parsed.path, name]))),
                             username=username, password=password))
            del directories[:]
    return repos


def get_repos_from_web(ui, url, prefix, username, password):
    parsed = urlparse.urlparse(url)
    if parsed.netloc == 'bitbucket.org':
        return get_repos_from_bitbucket(ui, parsed, prefix, username, password)
    return get_repos_from_hgweb(ui, parsed, prefix, username, password)


def get_repos_from_bitbucket(ui, parsed, prefix, username, password):
    repos = []
    ok, data = urlfetch('https://api.bitbucket.org/1.0/user/repositories/', username, password)
    if ok:
        for r in json.loads(data):
            name = r['name']
            source = urlparse.urlunparse(parsed._replace(path='%s/%s' % (r['owner'], r['slug'])))
            if prefix is None:
                repos.append((name, source))
            else:
                if name.startswith(prefix):
                    repos.append((name.replace(prefix, '', 1).strip('/'), source))
    else:
        url = urlparse.urlunparse(parsed)
        ui.error('Could not get %s: %s\n' % (url, data))
        logger.error('Could not get %s: %s' % (url, data))
    return repos


def get_repos_from_hgweb(ui, parsed, prefix, username, password):
    repos = []
    if prefix:
        if parsed.path == '':
            parsed = parsed._replace(path=prefix)
        else:
            parsed = parsed._replace(path='%s/%s' % (parsed.path, prefix))
    ok, data = urlfetch(urlparse.urlunparse(parsed._replace(query=urllib.urlencode({'style': 'raw'}))), username, password)
    if ok:
        for line in filter(None, map(lambda x: x.strip(), data.strip().split('\n'))):
            repos.append((
                line.replace(parsed.path, '').strip('/'),
                urlparse.urlunparse(parsed._replace(path=line))
            ))
    else:
        url = urlparse.urlunparse(parsed)
        ui.error('Could not get %s: %s\n' % (url, data))
        logger.error('Could not get %s: %s' % (url, data))
    return repos


def setup_readline():
    try:
        import readline

        def complete(text, state):
            return (glob.glob(text + '*') + [None])[state]

        readline.set_completer_delims(' \t\n;')
        readline.parse_and_bind("tab: complete")
        readline.set_completer(complete)
    except:
        pass
