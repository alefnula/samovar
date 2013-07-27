__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

# tea imports
from tea.commander import BaseCommand
from ._parsing import HgStyle, HgLexer

class Command(BaseCommand):
    '''Perform hg revert on all requested repositories'''
    
    Style = HgStyle
    Lexer = HgLexer
    
    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.hg.revert()
            self.ui.report(repo, status, {'output': output, 'error': error})
