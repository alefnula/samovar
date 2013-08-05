__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

from tea.commander import BaseCommand
from ._parsing import HgStyle, HgLexer, Token


class Command(BaseCommand):
    '''Perform hg fetch of all needed repositories'''

    Style = HgStyle
    Lexer = HgLexer
    LexerConfig = {
        'statuses': {
            0: Token.Ok,
            1: Token.NoChanges,
            2: Token.Failed,    # Uncommited changes
        }
    }

    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.hg.fetch()
            self.ui.report(repo, status, {'output': output, 'error': error})
