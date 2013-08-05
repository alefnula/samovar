__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

from tea.commander import BaseCommand
from ._parsing import Token, HgStyle, HgLexer


class Command(BaseCommand):
    '''Perform hg push of all needed repositories'''

    Style = HgStyle
    Lexer = HgLexer
    LexerConfig = {
        'statuses': {
            0 : Token.Ok,
            1 : Token.NoChanges,
        }
    }

    option_list = BaseCommand.option_list + (
        ('new-branch', {'action': 'store_true', 'help': 'allow pushing a new branch'}),
    )

    def handle(self, new_branch, *args, **kwargs):
        for repo in self.config.repositories:
            status, output, error = repo.push(new_branch=new_branch)
            self.ui.report(repo, status, {'output': output, 'error': error})
