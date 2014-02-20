__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from samovar.commander import BaseCommand
from tea.utils.crypto import encrypt


class Command(BaseCommand):
    '''
    Manages repository credentials.

    Usage:
        credentials set
        credentials list
    '''

    def handle(self, *args, **kwargs):
        if len(args) == 1 and args[0] == 'set':
            url = self.ui.ask('Url: ')
            parsed = urlparse.urlparse(url)
            url = parsed.netloc if parsed.netloc else parsed.path

            username = self.ui.ask('Username: ')
            password = encrypt(self.ui.ask('Password: ', True))

            data = {
                    'url': url,
                    'username': username,
                    'password': password,
                }

            current_creds = self.config.get(self.id, None)
            if current_creds:
                for i, cred in enumerate(current_creds):
                    if cred['url'] == url:
                        self.config.delete('%s.%s' % (self.id, i))
            else:
                self.config.set(self.id, [])
            self.config.insert(self.id, data)

        elif len(args) == 1 and args[0] == 'list':
            for cred in self.config.get(self.id, []):
                self.ui.info('%s -> %s' % (cred['url'], cred['username']))
        else:
            self.print_usage()
