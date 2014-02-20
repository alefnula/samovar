from __future__ import print_function

__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'

from samovar.commander import BaseCommand
from samovar import utils


class RepositoryNotFound(Exception):
    def __init__(self, name):
        super(RepositoryNotFound, self).__init__()
        self.name = name


class Command(BaseCommand):
    '''Repository management

    All these commands work on the currently selected workspace:

    repo list                   # Lists all repositories in the current workspace
    repo get NAME               # Prints information about the selected repo
    repo add                    # Add repo to current workspace
    repo del NAME               # Deletes a repo from current workspace

    repo alias                  # List all repository aliases for current workspace
    repo alias get ALIAS        # Prints out the value for selected alias
    repo alias add REPO ALIAS   # Adds an alias with selected value
    repo alias del ALIAS        # Delete an alias
    '''
    # Repo functions
    def repo_wizard(self):
        while True:
            self.ui.message('1. Import from url')
            self.ui.message('2. Add manually')
            self.ui.message('3. Quit')
            answer = self.ui.ask('Select number: ')
            if answer == '3':
                break
            elif answer == '2':
                name = self.ui.ask('Name: ')
                source = self.ui.ask('Source URL: ')
                yield name, {'source': source}
            elif answer == '1':
                for name, source in self.repo_import():
                    yield name, {'source': source}

    def repo_import(self):
        url    = self.ui.ask('Url: ')
        prefix = self.ui.ask('Prefix: ') or None
        username, password = self.config.credentials_for(url)
        repos = utils.get_repos_from_web(self.ui, url, prefix, username, password)
        self.ui.info('Choose repositories:')
        for name, repo in repos:
            answer = self.ui.ask('[Y/n] %s: ' % name)
            if answer.lower() in ('y', ''):
                yield name, repo

    def repo_get(self, name):
        workspace = self.config.active_workspace
        if name not in workspace['repositories']:
            raise RepositoryNotFound(name)
        return name, workspace['repositories'][name]

    def print_repo(self, name, repo):
        self.ui.info('Name:   ', False)
        self.ui.message(name)
        self.ui.info('Source: ', False)
        self.ui.message(repo['source'])
        self.ui.message('')

    # Alias functions
    def print_alias(self, alias, value):
        self.ui.warn(alias, False)
        self.ui.message(' -> ', False)
        self.ui.info(value)

    def handle_alias(self, *args):
        active = self.config.active
        l = len(args)
        if l == 0:
            for alias, value in self.config.get('workspaces.%s.aliases' % active, {}).items():
                self.print_alias(alias, value)
        else:
            cmd = args[0]
            # add
            if cmd == 'add' and l == 3:
                self.config.set('workspaces.%s.aliases.%s' % (active, args[2]), args[1])
            # get
            elif cmd == 'get' and l == 2:
                value = self.config.get('workspaces.%s.aliases.%s' % (active, args[1]))
                self.print_alias(args[1], value)
            # del
            elif cmd == 'del' and l == 2:
                alias = args[1]
                self.config.delete('workspaces.%s.aliases.%s' % (active, args[1]))
            # unknown command
            else:
                print(self.usage())

    def handle(self, *args, **kwargs):
        if len(args) == 0:
            print(self.usage())
        else:
            cmd = args[0]
            if cmd == 'alias':
                self.handle_alias(*args[1:])
            else:
                args = args[1:]
                l    = len(args)
                try:
                    if cmd == 'list' and l == 0:
                        for name, repo in self.config.get('workspaces.%s.repositories' % self.config.active, {}).items():
                            self.print_repo(name, repo)
                    elif cmd == 'get' and l == 1:
                        self.print_repo(*self.repo_get(args[0]))
                    elif cmd == 'add' and l == 0:
                        for name, repo in self.repo_wizard():
                            self.config.set('workspaces.%s.repositories.%s' % (self.config.active, name), repo)
                    elif cmd == 'del' and l == 1:
                        name, _ = self.repo_get(args[0])
                        self.config.delete('workspaces.%s.repositories.%s' % (self.config.active, name))
                    else:
                        print(self.usage())
                except RepositoryNotFound as e:
                    self.ui.error('Repository not found: "%s"' % e.name)
