from __future__ import print_function

__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import json
# tea imports
from tea.commander import BaseCommand
# samovar imports
from samovar import utils



class WorkspaceNotFound(Exception):
    def __init__(self, name):
        super(WorkspaceNotFound, self).__init__()
        self.name = name


class RepositoryNotFound(Exception):
    def __init__(self, name):
        super(RepositoryNotFound, self).__init__()
        self.name = name
        


class Command(BaseCommand):
    '''Workspaces management
    
    Commands:
    
    workspace switch                      # switch the currently active workspace
    workspace export NAME workspace.json  # Export selected workspcae to workspace.json 
    workspace import workspace.json       # Import a workspace from workspace.json
    workspace list                        # Prints out a list of all workspaces
    workspace get [NAME]                  # Prints information about the selected workspace
    workspace add [NAME]                  # Creates a new workspaces
    workspace del NAME                    # Deletes a workspace
    '''

    def workspace_wizard(self, name=None):
        if name is None:
            name = self.ui.ask('Name: ')
        workspace = {
            'path': self.ui.ask('Path: '),
            'repositories': {},
        }
        return name, workspace

    def workspace_print(self, name, workspace):
        self.ui.info('Name: ', False)
        self.ui.message(name)
        self.ui.info('Path: ', False)
        self.ui.message(workspace['path'])
        self.ui.info('Repositories:')
        for repo in sorted(workspace.get('repositories', {})):
            self.ui.message('  %s' % repo)
    
    def workspace_get(self, name):
        workspace = self.config.get('workspaces.%s' % name)
        if workspace is None:
            raise WorkspaceNotFound(name)
        return name, workspace

    def handle(self, *args, **kwargs):
        utils.setup_readline()
        try:
            l = len(args)
            if l == 0:
                print(self.usage())
                return
            cmd  = args[0]
            args = args[1:]
            l    = len(args)
            
            # Switch
            if cmd == 'switch' and l == 1:
                name, _ = self.workspace_get(args[0])
                self.config.set('active', name)
            # Export
            elif cmd == 'export' and l == 2:
                name, workspace = self.workspace_get(args[0])
                with open(args[1], 'wb') as f:
                    json.dump({
                        'name'      : name,
                        'workspace' : workspace,
                    }, f, indent=4)
            # Import
            elif cmd == 'import' and l == 1:
                with open(args[0], 'rb') as f:
                    data = json.load(f)
                    self.config.set('workspaces.%s' % data['name'], data['workspace'])
            # List
            elif cmd == 'list' and l == 0:
                active = self.config.active
                for name in self.config.get('workspaces', {}):
                    if name == active:
                        self.ui.warn(name)
                    else:
                        self.ui.info(name)
            # Get
            elif cmd == 'get' and l in (0, 1):
                if l == 0:
                    self.workspace_print(self.config.active, self.config.active_workspace)
                else:
                    self.workspace_print(*self.workspace_get(args[0]))
            # Add
            elif cmd == 'add' and l in (0, 1):
                name = args[0] if l == 1 else None
                name, workspace = self.workspace_wizard(name)
                self.config.set('workspaces.%s' % name, workspace)
                # If this is the only product set it as current
                if len(self.config.get('workspaces')) == 1:
                    self.config.set('active', name)
            # Del
            elif cmd == 'del' and l == 1:
                name, workspace = self.workspace_get(args[0])
                self.config.delete('workspaces.%s' % name)
                # if it was current set the next one to be current
                if self.config.active == name:
                    if len(self.config.get('workspaces')) > 0:
                        self.config.set('active', self.config.get('workspaces').keys()[0])
                    else:
                        self.config.delete('active')
            else:
                print(self.usage())
        except WorkspaceNotFound as e:
            self.ui.error('Workspace not found: "%s"' % e.name)
