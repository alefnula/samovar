__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
import logging

try:
    from urlparse import urlparse      # py2
except ImportError:
    from urllib.parse import urlparse  # py3

from samovar.scm import Repository
from tea.system import platform
from tea.ds.config import MultiConfig
from tea.console.color import cprint, Color
from tea.utils.crypto import decrypt
from samovar import utils

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    def __init__(self, message):
        super(ConfigurationError, self).__init__()
        self.message = message

    def __repr__(self):
        return 'ConfigurationError: %s' % self.message
    __str__ = __repr__


class LambdaDict(object):
    '''This provides lazy evaluation of lambda functions'''
    def __init__(self, d):
        self.d = d

    def __getitem__(self, name):
        return self.d[name]()


class Configuration(MultiConfig):
    def __init__(self, *args, **kwargs):
        super(Configuration, self).__init__(*args, **kwargs)
        self.__repositories    = None
        # Executables
        # TODO: Not actually cross platform
        if platform.is_a(platform.WINDOWS):
            self.executables = LambdaDict({
                '7z'           : lambda: utils.find_exe('pf',  ['7-Zip', '7z.exe'], '7z.exe'),
                'devenv'       : lambda: utils.find_exe('pf',  ['Microsoft Visual Studio 1?.0', 'Common7', 'IDE', 'devenv.com'], 'devenv.com'),  # MUST BE .COM!!! NOT .EXE!!!
                'msbuild'      : lambda: utils.find_exe('win', ['Microsoft.NET', 'Framework', 'v4.0.30319', 'msbuild.exe'], 'msbuild.exe'),
                'msbuild_2008' : lambda: utils.find_exe('win', ['Microsoft.NET', 'Framework', 'v3.5', 'msbuild.exe'], 'msbuild.exe'),
                'nunit'        : lambda: utils.find_exe('pf',  ['NUnit 2.*.*', 'bin', 'net-2.0', 'nunit-console.exe'], 'nunit-console.exe'),
                'ipy'          : lambda: utils.find_exe('pf',  ['IronPython 2.7', 'ipy64.exe'], 'ipy64.exe'),
                'python'       : lambda: utils.find_exe(None,  ['C:\\', 'Python2*', 'python.exe'], 'python.exe'),
                'tortoisehg'   : lambda: utils.find_exe('pf',  ['TortoiseHg', 'thg.exe'], 'thg.exe'),
            })
        elif platform.is_a(platform.POSIX):
            self.executables = {
                '7z'           : '7z',
                'msbuild'      : 'xbuild',
                'python'       : 'python',
            }

    @property
    def active(self):
        active = self.get('active')
        if active is None:
            raise ConfigurationError('None of the workspaces is active')
        return active

    @property
    def active_workspace(self):
        return self.get('workspaces.%s' % self.active)

    @property
    def active_path(self):
        '''Returns the current workspace path'''
        return self.active_workspace['path']

    @property
    def logdir(self):
        return os.path.join(self.active_path, 'logs')

    @property
    def all_repositories(self):
        workspace = self.active_workspace
        if workspace is None:
            cprint('None of the workspaces is selected as current\n', Color.red)
            raise ConfigurationError('No current workspace')
        repos = []
        for name in sorted(workspace['repositories']):
            repo = workspace['repositories'][name]
            username, password = self.credentials_for(repo['source'])
            repos.append(Repository(name=name, path=os.path.abspath(os.path.join(workspace['path'], name)),
                                    source=repo['source'], username=username, password=password))
        return repos

    @property
    def repositories(self):
        aliases = self.get('workspaces.%s.aliases' % self.active, {})
        repos = self.all_repositories
        if self.get('options.selected_repositories'):
            full_repo_names = [(aliases[repo] if repo in aliases else repo) for repo in self.get('options.selected_repositories')]
            repos = [r for r in repos if r.name in full_repo_names]
        if self.get('options.skipped_repositories'):
            full_repo_names = [(aliases[repo] if repo in aliases else repo) for repo in self.get('options.skipped_repositories')]
            repos = [r for r in repos if r.name not in full_repo_names]
        return repos

    def credentials_for(self, url):
        url = urlparse(url).netloc
        for cred in self.get('credentials'):
            if cred['url'] == url:
                return cred['username'], decrypt(cred['password'])
        return None, None
