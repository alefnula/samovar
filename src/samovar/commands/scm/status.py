__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

from samovar.commander import BaseCommand
from ._parsing import HgStyle, HgLexer, Token, PARSERS


class Command(BaseCommand):
    '''Perform hg status of all selected repositories.'''

    option_list = BaseCommand.option_list + (
        ('A, all', {
            'action'  : 'store_true',
            'dest'    : 'show_all',
            'help'    : 'Show status of all files'
        }),
        ('m, modified',  {'action': 'store_true', 'help': 'Show only modified files'}),
        ('a, added',     {'action': 'store_true', 'help': 'Show only added files'}),
        ('r, removed',   {'action': 'store_true', 'help': 'Show only removed files'}),
        ('d, deleted',   {'action': 'store_true', 'help': 'Show only deleted files'}),
        ('c, clean',     {'action': 'store_true', 'help': 'Show only files without changes'}),
        ('u, unknown',   {'action': 'store_true', 'help': 'Show only unknown (not tracked) files'}),
        ('i, ignored',   {'action': 'store_true', 'help': 'Show only ignored files'}),
        ('n, no-status', {'action': 'store_true', 'help': 'Hide status prefix'}),
        ('C, copies',    {'action': 'store_true', 'help': 'Show source of copied files.'}),
    )

    Style = HgStyle
    Lexer = HgLexer
    LexerConfig = {
        'statuses' : {
            0: Token.NoChanges,
            1: Token.Changed,
        },
        'parse'  : True,
        'parser' : PARSERS['status']
    }

    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.status(**kwargs)
            self.ui.report(repo, status, {'output': output, 'error': error})
