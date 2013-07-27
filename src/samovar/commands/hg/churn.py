__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = 'Jan 17, 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

from tea.commander import BaseCommand
from ._parsing import HgStyle, HgLexer


class Command(BaseCommand):
    ''' Perform hg churn on all repositories.'''

    option_list = BaseCommand.option_list + (
        ('s, sort',       {'action': 'store_true', 'help': 'Sort by key (default is sort by count)'}),
        ('diffstat',      {'action': 'store_true', 'help': 'Show added/removed lines separately'   }),
        ('c, changesets', {'action': 'store_true', 'help': 'Count rate by number of changesets.'   }),
    )

    Style       = HgStyle
    Lexer       = HgLexer
    LexerConfig = {'parse': True}
    
    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.hg.churn(**kwargs)
            self.ui.report(repo, status, {'output': output, 'error': error})
