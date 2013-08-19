__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
from tea import shutil
from tea.commander import BaseCommand
# samovar imports
from . import const
from . import utils
from .dependency_graph import DependencyGraph


class Command(BaseCommand):
    '''Perform hg fetch of all needed repositories'''

    option_list = BaseCommand.option_list + (
        (const.x86, {
            'action'  : 'store_const',
            'dest'    : 'platform',
            'const'   : const.x86,
            'default' : const.x64,
            'help'    : 'build %s platform' % const.x86,
        }),
        (const.x64, {
            'action'  : 'store_const',
            'dest'    : 'platform',
            'const'   : const.x64,
            'default' : const.x64,
            'help'    : 'build %s platform' % const.x64,
        }),
        (const.Debug.lower(), {
            'action'  : 'store_const',
            'dest'    : 'configuration',
            'const'   : const.Debug,
            'default' : const.Release,
            'help'    : 'build in %s configuration' % const.Debug,
        }),
        (const.Release.lower(), {
            'action'  : 'store_const',
            'dest'    : 'configuration',
            'const'   : const.Release,
            'default' : const.Release,
            'help'    : 'build in %s configuration' % const.Release,
        }),
        ('b, build-number',  {
            'action'  : 'store',
            'default' : '0',
            'help'    : 'Set the build number'
        }),
        ('n, no-deps', {'action': 'store_true', 'help': 'do not build dependencies first'}),
        ('d, delete',  {'action': 'store_true', 'help': 'delete the output folder before build'}),
    )

    def save_log(self, project, data):
        logpath = os.path.join(self.config.logdir,
                               project.path.replace(self.config.active_path, '').strip('\\/'),
                               project.id + '.log')
        if not os.path.isdir(os.path.dirname(logpath)):
            shutil.mkdir(os.path.dirname(logpath))
        with open(logpath, 'wb') as f:
            f.write(data)

    def handle(self, platform, configuration, build_number, no_deps, delete, *args, **kwargs):
        repos       = []
        # Build dependency graph, or not
        if no_deps:
            for repo in self.config.repositories:
                b = utils.load_build(repo)
                repos.append(b)
        else:
            all_repos = {}
            for repo in self.config.all_repositories:
                # Remove explicitly skipped
                skipped = self.config.get('options.skipped_repositories') or []
                if repo.name not in skipped:
                    b = utils.load_build(repo)
                    all_repos[b.name] = b
            dg = DependencyGraph(all_repos.values())
            for repo in dg.get_in_order(map(lambda x: all_repos[x.name].id, self.config.repositories), None):
                repos.append(repo)

        config = utils.BuildConfig(self.config, platform, configuration, build_number)

        # if --delete
        if delete and os.path.exists(config.output_path):
            if not shutil.remove(config.output_path):
                self.ui.error('Abort: "%s" could not be deleted' % config.output_path)
                return
        # create output path if not exist
        if not os.path.exists(config.output_path):
            shutil.mkdir(config.output_path)

        # Build
        for repo in repos:
            self.ui.info(str(repo))
            for project in repo.projects:
                status, output, error = project.build(config)
                self.save_log(project, output + '\n\n\n' + error)
                self.ui.report('  %s' % project, status, {'output': output, 'error': error})
