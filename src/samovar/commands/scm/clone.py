__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os

from tea import shell
from samovar.commander import BaseCommand
from ._parsing import HgStyle, HgLexer


class Command(BaseCommand):
    '''Perform hg clone of all needed repositories'''

    option_list = BaseCommand.option_list + (
        ('d, delete', {'action': 'store_true', 'help': 'delete workspace before checkouting'}),
    )

    Style = HgStyle
    Lexer = HgLexer

    def handle(self, delete=False, *args, **kwargs):
        if delete and os.path.exists(self.config.active_path):
            shell.remove(self.config.active_path)
        for repo in self.config.repositories:
            status, output, error = repo.clone()
            self.ui.report(repo, status, {'output': output, 'error': error})
