__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

from samovar.commander import BaseCommand
from ._parsing import HgStyle, HgLexer, Token


class Command(BaseCommand):
    '''Perform hg pull of all selected repositories'''
    Style = HgStyle
    Lexer = HgLexer
    LexerConfig = {
        'statuses': {
            0: Token.Ok,
            1: Token.NoChanges,
        }
    }

    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.pull()
            if 'no changes found' in output:
                status = 1
            self.ui.report(repo, status, {'output': output, 'error': error})
