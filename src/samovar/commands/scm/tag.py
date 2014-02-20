__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

from samovar.commander import BaseCommand
from ._parsing import HgStyle, HgLexer


class Command(BaseCommand):
    '''Adds tag to repositories.

    Tag name is required.
    '''

    option_list = BaseCommand.option_list + (
        ('l, local',   {'action': 'store_true', 'help': 'Make the tag local'}),
        ('m, message', {'action': 'store',      'help': 'Commit message.'}),
        ('u, user',    {'action': 'store',      'help': 'Record specified user as committer'}),
    )

    Style = HgStyle
    Lexer = HgLexer

    def handle(self, tag, local, message, user):
        for repo in self.config.repositories:
            status, output, error = repo.tag(tag, local=local, message=message, user=user)
            self.ui.report(repo, status, {'output': output, 'error': error})
