__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

from tea.commander import BaseCommand
from ._parsing import HgStyle, HgLexer


class Command(BaseCommand):
    '''Updates repositories.

    Note that using --rev with explicit changeset has no meaning without --repo option
    because every repository has different changesets.
    --rev options should be used to update to tag or branch that is present in every repository.
    If --rev is not provided repositories will be updated to latest revision of current branch.
    '''

    option_list = BaseCommand.option_list + (
        ('C, clean', {'action': 'store_true', 'help': 'Discard uncommitted changed (no backup)'}),
        ('r, rev',   {
            'action'  : 'store',
            'type'    : str,
            'default' : 'tip',
            'help'    : 'Revision to update to. '
        }),
    )

    Style = HgStyle
    Lexer = HgLexer

    def handle(self, clean, rev, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.update(revision=rev, clean=clean)
            self.ui.report(repo, status, {'output': output, 'error': error})
