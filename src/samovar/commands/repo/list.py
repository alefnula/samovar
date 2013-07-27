__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

# tea imports
from tea.commander import BaseCommand
from tea.parsing import Token

class Command(BaseCommand):
    '''List all repositories'''
    
    LexerConfig = {0: Token.Other}
    
    def handle(self, *args, **kwargs):
        for repo in self.config.repositories:
            self.ui.report(repo, 0)
