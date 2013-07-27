__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

# tea imports
from tea.commander import BaseCommand


class Command(BaseCommand):
    '''Executes python or IPython shell with some predefined environment injected'''
    
    def handle(self, *args, **kwargs):
        imported_objects = {
            'config' : self.config,
        }
        try:
            # Try IPython imports
            from IPython.frontend.terminal.interactiveshell import TerminalInteractiveShell
            from IPython.config.loader import Config

            cfg = Config()
            shell = TerminalInteractiveShell(config=cfg, user_ns=imported_objects)
            shell.mainloop(display_banner='\n  Samovar  \n')
        except:
            import code
            code.InteractiveConsole(locals=imported_objects).interact()
