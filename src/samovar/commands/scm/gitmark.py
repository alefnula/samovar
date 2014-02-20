__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

from samovar.commander import BaseCommand

from ._parsing import HgStyle, HgLexer


class Command(BaseCommand):
    '''Creates a bookmark for pushing to a git repository using hg-git.
    '''

    Style       = HgStyle
    Lexer       = HgLexer
    LexerConfig = {'parse': True}

    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.scm._hgr('bookmark', '-r', 'default', 'master')
            self.ui.report(repo, status, {'output': output, 'error': error})
