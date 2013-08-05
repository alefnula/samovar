__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

# tea imports
from tea.commander import BaseCommand
from ._parsing import HgStyle, HgLexer, Token, PARSERS


class Command(BaseCommand):
    '''Perform hg incoming on all required repositories'''

    Style = HgStyle
    Lexer = HgLexer
    LexerConfig = {
        'statuses' : {
            0: Token.Changed,
            1: Token.NoChanges,
           -1: Token.Changed,  # new repository
        },
        'parse'  : True,
        'parser' : PARSERS['changeset']
    }

    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.hg.incoming()
            self.ui.report(repo, status, {'output': output, 'error': error})
