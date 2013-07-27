__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

from tea.commander import BaseCommand
from ._parsing import HgStyle, HgLexer


class Command(BaseCommand):
    '''Perform hg commit on all selected repositories'''

    option_list = BaseCommand.option_list + (
        ('A, addremove', {'action': 'store_true', 'help': 'mark new/missing files as added/removed before'}),
        ('m, message',   {'action': 'store',      'help': 'use this as a commit message'                  }),
        ('amend',        {'action': 'store_true', 'help': 'Amend the parent of the working dir.'          }),
        ('u, user',      {'action': 'store',      'help': 'Record the specified user as commiter.'        }),
    )

    Style = HgStyle
    Lexer = HgLexer
    
    def handle(self, *args, **kwargs):
        # Message can be a keyword and positional argument
        if len(args) > 0 and kwargs.get('message') is not None:
            self.ui.error('Abort: cannot provied message as switch and positional argument')
        message = kwargs.get('message') or (args[0] if args else None)
        if (message is None or message.strip() == ''):
            self.ui.error('Abort: empty commit message')
        else:
            for repo in self.config.repositories:
                commiter = self._get_commiter(repo, kwargs.get('user'))
                status, output, error = repo.hg.commit(message=message, addremove=kwargs.get('addremove'),
                                                       amend=kwargs.get('amend'), user=commiter) 
                self.ui.report(repo, status, {'output': output, 'error': error})
             
    def _get_commiter(self, repo, user):
        if user is not None: return user
        
        # Try in repository
        config_path = 'workspaces.%s.repositories.%s.commiter' % (self.config.active, repo.name)
        repo_commiter = self.config.get(config_path, None)
        if repo_commiter is not None:
            return repo_commiter
        # Try in workspace
        return self.config.get('workspaces.%s.commiter' % self.config.active, None)
