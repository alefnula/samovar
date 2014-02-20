__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
import sys
import logging

from tea import system
from samovar.commander import Application
from tea.logger import configure_logging


def main(args):
    configure_logging(stdout_level=logging.ERROR)

    from samovar import options
    from samovar.config import Configuration
    from samovar.styles import StatusStyle, StatusLexer

    class Samovar(Application):
        def __init__(self):
            super(Samovar, self).__init__(args, ['samovar.commands'], {
                'description'        : 'Samovar',
                'options'            : options.OPTIONS,
                'defaults'           : options.DEFAULTS,
                'check_and_set_func' : options.check_and_set_func,
            }, os.path.join(system.get_appdata(), 'Samovar', 'Samovar.json'),
            Configuration)
            self._ui.formatter.style = StatusStyle
            self._ui.formatter.lexer = StatusLexer()

        # HACK: This is a hack for configuring the logging after the
        #       options and configuration file is loaded. Should be
        #       changed somehow :-/
        def preparse(self, *args, **kwargs):
            parser, args, config = super(Samovar, self).preparse(*args, **kwargs)
            logfile = config.get('logfile', config.get('options.logfile'))
            if logfile:
                configure_logging(logfile, initial_file_message='Starting Samovar',
                                  level=logging.INFO, stdout_level=logging.CRITICAL)
            else:
                configure_logging(stdout_level=logging.WARNING)
            return parser, args, config

    app = Samovar()
    app.execute()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
