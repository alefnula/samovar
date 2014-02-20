__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

from samovar.commander import BaseCommand
from ._parsing import HgStyle, HgLexer, PARSERS


class Command(BaseCommand):
    '''Prints heads in repositories'''

    Style = HgStyle
    Lexer = HgLexer
    LexerConfig = {
        'parse'  : True,
        'parser' : PARSERS['changeset'],
    }

    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.heads()
            self.ui.report(repo, status, {'output': output, 'error': error})
