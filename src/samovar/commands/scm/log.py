__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

from samovar.commander import BaseCommand
from ._parsing import HgStyle, HgLexer, PARSERS


class Command(BaseCommand):
    '''Prints log from all repositories.'''

    option_list = BaseCommand.option_list + (
        ('l, limit', {
            'action'  : 'store',
            'type'    : int,
            'default' : 1,
            'help'    : 'Number of changesets to show.'
        }),
        ('f, follow', {'action': 'store_true', 'help': 'Follow changeset history, or file history across copies and renames'}),
        ('C, copies', {'action': 'store_true', 'help': 'Show copies files'}),
        ('G, graph',  {'action': 'store_true', 'help': 'Show revision graph'}),
        ('u, user',   {'action': 'append', 'type': str, 'help': 'Revisions committed by user'}),
        ('b, branch', {'action': 'append', 'type': str, 'help': 'Show changesets from given namebranch'}),
    )

    Style = HgStyle
    Lexer = HgLexer
    LexerConfig = {
        'parse'  : True,
        'parser' : PARSERS['changeset']
    }

    def handle(self, limit, follow, copies, graph, user, branch, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.log(limit, follow, copies, graph, user, branch)
            self.ui.report(repo, status, {'output': output, 'error': error})
