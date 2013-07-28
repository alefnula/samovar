__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
from tea.system import platform
from tea.process import execute
from tea.commander import BaseCommand
from tea.console.color import cprint, Color


class Command(BaseCommand):
    '''Open a console or explorer window in the product folder

    If only one repository is provided with --repo filter, then
    the application will be opened in that repository.
    '''

    option_list = BaseCommand.option_list + (
        ('c, console', {'action': 'store_const', 'dest': 'what', 'const': 'cmd', 'default': 'cmd', 'help': 'open console window'}),
        ('f, file-manager', {'action': 'store_const', 'dest': 'what', 'const': 'fm', 'default': 'cmd', 'help': 'open file manager window'}),
        ('t, tortoise-hg', {'action': 'store_const', 'dest': 'what', 'const': 'thg', 'default': 'cmd', 'help': 'open TortoiseHg for specified repository.'}),
        (None, {'action': 'store', 'dest': 'repository', 'nargs': '?'})
    )

    def open(self, what, path):
        path = os.path.abspath(path)
        if what == 'cmd':
            if platform.is_a(platform.WINDOWS):
                os.system('start cmd /k cd /d "%s"' % path)
            elif platform.is_a(platform.DARWIN):
                result = os.system('open -a iTerm "%s"' % path)
                if result != 0:
                    os.system('open -a Terminal "%s"' % path)
        elif what == 'fm':
            import webbrowser
            if platform.is_a(platform.DARWIN):
                webbrowser.open('file://' % path)
            else:
                webbrowser.open(path)
        elif what == 'thg':
            executable = self.config.executables[what]
            status, output, _ = execute(executable, '--repository', path)
            if status != 0:
                cprint('Unable to opet tortoiseHg.\n', Color.red)
                cprint('%s' % output)

    def handle(self, what, repository, *args, **kwargs):
        if repository is not None:
            for repo in self.config.repositories:
                if repo.name == repository:
                    self.open(what, repo.path)
                    return
            else:
                self.ui.error('Repository "%s" not found.' % repository)
        else:
            self.open(what, self.config.active_path)
