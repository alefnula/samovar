__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

from samovar.commander import BaseCommand
from ._parsing import HgStyle, HgLexer, PARSERS


class Command(BaseCommand):
    '''Performs hg diff command on repositories.

    Note that using --rev or --change options does not make sense without --repo option,
    because every repository has different changesets.
    But these options can be useful if used with tag that are present in every repository.
    '''

    option_list = BaseCommand.option_list + (
        ('r, rev',                 {'action': 'store', 'dest': 'revision', 'help': 'Revision.'}),
        ('c, change',              {'action': 'store',      'help': 'Change made by revision.'}),
        ('a, text',                {'action': 'store_true', 'help': 'Treat all files as text.'}),
        ('g, git',                 {'action': 'store_true', 'help': 'Use git extended diff format.'}),
        ('p, show-function',       {'action': 'store_true', 'help': 'Show which function each change is in.'}),
        ('reverse',                {'action': 'store_true', 'help': 'Produce diff that undoes the changes.'}),
        ('w, ignore-all-space',    {'action': 'store_true', 'help': 'Ignore white space when comparing lines'}),
        ('b, ignore-space-change', {'action': 'store_true', 'help': 'Ignore changes in amount of white space.'}),
        ('B, ignore-blank-lines',  {'action': 'store_true', 'help': 'Ignore changes whose lines are all blank.'}),
        ('stat',                   {'action': 'store_true', 'help': 'Output diffstat-style summary of changes.'}),
        ('U, unified', {
            'action'  : 'store',
            'type'    : int,
            'dest'    : 'unified',
            'default' : -1,
            'help'    : 'Number of lines of context to show.'
        }),
    )

    Style = HgStyle
    Lexer = HgLexer
    LexerConfig = {
        'parse'  : True,
        'parser' : PARSERS['diff'],
        'indent' : 0,
    }

    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.diff(**kwargs)
            self.ui.report(repo, status, {'output': output, 'error': error})
