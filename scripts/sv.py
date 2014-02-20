#!/usr/bin/env python
from __future__ import print_function

__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
import sys
import time

PREFIX = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.extend([
    os.path.join(PREFIX, 'tea',     'src'),
    os.path.join(PREFIX, 'samovar', 'src'),
])

from tea import shell
from tea.utils.six.moves import input
from tea.system import platform
if platform.is_a(platform.WINDOWS):
    get_time = time.clock
else:
    get_time = time.time

# FIXME: Read from existing commands and their options (aliases, repositories...)
commands = {
    'branch'     : [],
    'branches'   : [],
    'churn'      : ['--sort', '--diffstat', '--changesets'],
    'clone'      : ['--delete'],
    'commit'     : ['--addremove', '--message', '--amend', '--user'],
    'diff'       : ['--rev', '--change', '--show-functions', '--reverse', 
                    '--ignore-all-space', '--ignore-blank-lines', '--unified', 
                    '--stat'],
    'fetch'      : [],
    'heads'      : [],
    'incoming'   : [],
    'log'        : ['--limit', '--folow', '--copies', '--graph', 
                    '--user', '--branch'],
    'outgoing'   : [],
    'pull'       : [],
    'purge'      : ['--all', '--print'],
    'push'       : [],
    'revert'     : [],
    'status'     : ['--all', '--modified', '--added', '--removed', '--deleted', 
                    '--clean', '--unknown', '--ignored', '--no-status', '--copies'],
    'tag'        : ['--local', '--message', '--user'],
    'update'     : ['--clean', '--rev'],
    'build'      : ['--x86', '--x64', '--debug', '--release', '--no-deps', 
                    '--delete'],
    'open'       : ['--console', '--file-manager', '--tortoise-hg'],
    'shell'      : [],
    'credentials': ['set', 'list'],
    'list'       : [],
    'workspace'  : ['switch', 'export', 'import', 'list', 'get', 'add', 'del'],
}

def setup_readline():
    try:
        import readline     
        def completer(text, state):
            # FIXME: Support more then two levels
            parts = readline.get_line_buffer().split()
            try:
                if len(parts) == 1 and parts[0] not in commands:
                    complete_from = commands.keys()
                else:
                    complete_from = commands[parts[0]]
                return [i for i in complete_from if i.startswith(text)][state]
            except KeyError:
                return None

        readline.rl.read_inputrc(os.path.join(os.path.dirname(__file__), 'svreadline.ini'))
        readline.parse_and_bind('tab: complete')
        readline.set_completer(completer)
    except:
        pass


if __name__ == '__main__':
    if len(sys.argv) > 1:
        from samovar.main import main
        sys.exit(main(sys.argv))
    else:
        try:
            while True:
                import subprocess
                setup_readline()
                command = input('> ').strip()
                if command in ('exit', 'quite'):
                    break
                if command != '':
                    timeit = False
                    if command.startswith('timeit '):
                        command = command.replace('timeit ', '', 1)
                        timeit = True
                    start_time = get_time()
                    subprocess.call([sys.executable, os.path.abspath(__file__)] + shell.split(command), shell=False)
                    if timeit:
                        print('Duration: %.4fs', get_time() - start_time)
        except KeyboardInterrupt:
            print()
