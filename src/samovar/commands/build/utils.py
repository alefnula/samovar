__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
import sys
import json
import string
import logging
from datetime import datetime
# tea imports
from tea import shutil
from tea.process import execute_in_environment

from .dependency_graph import DependencyGraph as DG

logger = logging.getLogger(__name__)


class Step(object):
    MSBUILD = 'msbuild'
    SHELL   = 'shell'
    
    def __init__(self, project, data):
        self.project     = project
        self.type        = data.get('type')
        self.working_dir = data.get('working_dir', None)
        if self.type == Step.MSBUILD:
            self.sln = data.get('sln')
        elif self.type == Step.SHELL:
            # Get success exit codes
            success = data.get('success', [0])
            if isinstance(success, basestring): 
                self.success = map(int, success.split(','))
            elif isinstance(success, int):
                self.success = [success]
            else:
                self.success = success
            # Get command
            if 'command' in data:
                self.commands = [data['command']]
            else:
                self.commands = data['commands']
             
        else:
            logger.error('Invalid project type: %s' % self.type)

    def _msbuild(self, config):
        command = [
            config.executables['msbuild'],
            '/p:Configuration=%s'  % config.configuration,
            '/p:Platform=%s'       % config.platform,
            '/p:PlatFormTarget=%s' % config.platform,
            '/p:OutputPath=%s'     % config.output_path,
            '/t:%s' %  os.path.normpath(self.project.id.replace('.', '_')),
            self.sln,
        ]
        return execute_in_environment(config.environment, *command)

    def _command(self, config):
        status, output, error = (0, '', '') 
        for command in self.commands:
            if isinstance(command, basestring):
                command = shutil.split(string.Template(command).safe_substitute(**config.environment))
            else:
                command = map(lambda part: string.Template(part).safe_substitute(**config.environment), command)
            s, o, e = execute_in_environment(config.environment, *command)
            status += 0 if s in self.success else 1
            output += o
            error  += e
            if status != 0: break
        return status, output, error
    
    def run(self, config):
        # Calculate the working dir
        working_dir = self.project.path if self.working_dir is None else os.path.join(self.project.path, self.working_dir) 
        with shutil.goto(working_dir) as ok:
            if not ok:
                error = 'Could not change directory to "%s"!' % working_dir
                logger.error(error)
                return 1, error, ''
            if self.type == Step.MSBUILD:
                return self._msbuild(config)
            elif self.type == Step.SHELL:
                return self._command(config)
            else:
                error = 'Don\'t know how to build %s projects!' % self.type
                logger.error(error)
                return 1, error, ''


class Project(object):
    def __init__(self, repo, id, config):
        self.path  = repo.path
        self.id    = id
        self.name  = id
        self.deps  = config.get('deps',  [])
        self.steps = [Step(self, data) for data in config.get('steps', [])]
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return 'Project <%s>' % self.name
    
    def __serialize__(self):
        return {
            'name' : self.name,
            'type' : 'Project',
            'path' : self.path,
        } 

    def build(self, config):
        status, output, error = 0, '', ''
        for step in self.steps:
            s, o, e = step.run(config)
            status += s
            output += o
            error  += e
            if s != 0: break
        return status, output, error


class BuildRepo(object):
    def __init__(self, repo, sv):
        self.path  = repo.path
        self.name  = repo.name 
        self.id    = sv['id']
        if 'build' in sv:
            self.deps     = sv['build'].get('deps', [])
            self.projects = DG([Project(self, id, data) for id, data in sv['build'].get('projects', {}).items()]).get_in_order()
        else:
            self.deps     = []
            self.projects = []

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return 'BuildRepo <%s>' % self.name


class BuildConfig(object):
    def __init__(self, config, platform, configuration, build_number):
        self.config        = config
        self.platform      = platform
        self.configuration = configuration
        self.timestamp     = datetime.now()
        self.timestamp_fmt = '%Y%m%d_%H%M'
        self.build_number  = build_number

    @property
    def output_path(self):
        '''Get the build output path'''
        return os.path.join(self.config.active_path, 'bin', self.platform, self.configuration)

    @property
    def executables(self):
        return self.config.executables

    @property
    def environment(self):
        '''Get environment variables'''
        d = datetime.now()
        # FIXME: Hack for Minor and build
        return {
            'PYTHONPATH'     : os.pathsep.join(sys.path),
            'IRONPYTHONPATH' : os.pathsep.join(sys.path),
            'OutputPath'     : self.output_path,
            'Configuration'  : self.configuration,
            'Timestamp'      : self.timestamp.strftime(self.timestamp_fmt),
            'python'         : sys.executable,
            'Minor'          : str(((d.year-2000) << 4) + d.month), 
            'Build'          : str((d.day << 11) + (d.hour << 6) + d.minute),
            'BuildNumber'    : str(self.build_number)
        }



def load_build(repo):
    samovar = os.path.join(repo.path, 'samovar.json')
    try:
        if os.path.isfile(samovar):
            sv = {}
            with open(samovar, 'rb') as f:
                sv = json.load(f)
            # Load projects
            return BuildRepo(repo, sv)
    except:
        logger.exception('Error while parsing: %s' % samovar)
    return BuildRepo(repo, {'id': os.path.basename(repo.path)})
