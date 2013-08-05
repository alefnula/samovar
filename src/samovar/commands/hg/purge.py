__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

from tea.commander import BaseCommand
from ._parsing import HgStyle, HgLexer


class Command(BaseCommand):
    '''Perform hg purge of all selected repositories'''

    option_list = BaseCommand.option_list + (
        ('all', {
            'action'  : 'store_true',
            'dest'    : 'purge_all',
            'help'    : 'purge ignored files too'
        }),
        ('p, print', {
            'action'  : 'store_true',
            'dest'    : 'only_print',
            'help'    : 'Print filenames instead of deleting them'
        }),
    )

    Style       = HgStyle
    Lexer       = HgLexer
    LexerConfig = {'parse': True}

    def handle(self, purge_all, only_print, *args, **kwargs):
        self.only_print = only_print
        #repo_paths = []
        for repo in self.config.repositories:
            status, output, error = repo.hg.purge(purge_all=purge_all, only_print=only_print)
            self.ui.report(repo, status, {'output': output, 'error': error})
            #repo_paths.append(repo.path)
        # TODO: Finihs removig files that are not part of any repository (e.g. os.path.join(self.config.active_path, 'bin'))
#        if purge_all:
#            dirs_to_delete = []
#            for root, dirs, files in os.walk(self.config.active_path, topdown=True):
#                for d in dirs[:]:
#                    if os.path.isdir(os.path.join(root, d, '.hg')):
#                        dirs.remove(d)
#                for f in files:
#                    file_to_remove = os.path.join(root, f)
#                    if not only_print:
#                        rmfile(file_to_remove)
#                    self.add_result(self.config.active_path, 0, file_to_remove, '')
#                dirs_to_delete.append(root)
#
#            for dir_to_delete in sorted(dirs_to_delete, key=lambda x: len(x), reverse=True):
#                try:
#                    if not only_print:
#                        os.rmdir(dir_to_delete)
#                    self.add_result(self.config.active_path, 0, dir_to_delete, '')
#                except OSError:
#                    # dir not empty
#                    self.add_result(dir_to_delete, 1, '', '')
