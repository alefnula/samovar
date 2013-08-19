from __future__ import print_function

__author__    = 'Bojan Delic <bojan@delic.in.rs>'
__date__      = 'Jan 11, 2013'
__copyright__ = 'Copyright (c) 2013 Bojan Delic'


class DependencyGraphException(Exception):
    pass


class Node(object):
    ''' Represents single node in graph '''
    
    def __init__(self, item):
        if isinstance(item, dict):
            self.id    = item['id']
            self.deps  = item['deps']
            self.group = item.get('group', None)
        else:
            self.id    = item.id
            self.deps  = item.deps
            self.group = getattr(item, 'group', None)
        self.item      = item
        self.dependant = set()
        self.requires  = set()
            
    def __str__(self):
        return "<Id: %s, Group: %s>" % (self.id, self.group)
    
    __repr__ = __str__


class NodeGroup(object):
    ''' Represents a group of nodes that form single graph '''
    
    def __init__(self, name, nodes):
        self.name  = name  
        self.nodes = {n.id:n for n in nodes}
        self._resolve_dependencies()
        self.levels = self._populate_levels()
    
    def _add_node(self, id, nodes):
        node = self.nodes[id]
        nodes.append(node)
        for req in node.requires:
            self._add_node(req.id, nodes)
    
    def get_in_order(self, ids=None):
        if ids is None:
            ids = self.nodes.keys()
        dupl = []
        for id in ids:
            self._add_node(id, dupl)
        nodes  = []
        for node in dupl[::-1]:
            if node not in nodes:
                nodes.append(node)
        return map(lambda node: node.item, nodes)

    def __iter__(self):
        return self.levels.__iter__()
    
    def __getitem__(self, key):
        return self.levels[key]
    
    def _populate_levels(self):
        levels = []
        nodes = self.nodes.values()
        while len(nodes) > 0:
            if len(levels) == 0:
                first_level = set(filter(lambda n: len(n.requires) == 0, nodes))
                if len(first_level) == 0:
                    raise DependencyGraphException('No root nodes - probably circular dependencies')
                levels.append(first_level)
            else:
                next_level = filter(lambda n: n.requires.issubset(reduce(set.union, levels)), nodes)
                levels.append(set(next_level))
            map(nodes.remove, levels[-1])
        return levels
    
    def _resolve_dependencies(self):
        for  node in self.nodes.values():
            for dep in node.deps:
                try:
                    node.requires.add(self.nodes[dep])
                    self.nodes[dep].dependant.add(node)
                except KeyError as e:
                    raise DependencyGraphException(e.message)
        
    def __str__(self):
        return '<Group: %s, Nodes: [%s]>' % (self.name, ', '.join(self.nodes))
    
    __repr__ = __str__


class DependencyGraph(object):
    ''' Dependency graph of nodes. '''
    
    def __init__(self, items):
        nodes = map(Node, items)
        group_names = set((n.group for n in nodes))
        self.groups = {}
        for group in group_names:
            self.groups[group] = NodeGroup(group, filter(lambda n: n.group == group, nodes))
        self.nodes = {n.id:n for n in nodes}
    
    def get_in_order(self, ids=None, group=None):
        return self.groups[group].get_in_order(ids)
        
    def __getitem__(self, group):
        return self.groups[group]

    def __iter__(self):
        return self.groups.values().__iter__()
    
    
def main():
    import pprint
    
    projects = [
        {'id': 'p4', 'deps': ['p2', 'p3'], 'group': 'g1'},
        {'id': 'p1', 'deps': [], 'group': 'g1'},
        {'id': 'p2', 'deps': ['p1'], 'group': 'g1'},
        {'id': 'p3', 'deps': ['p1'], 'group': 'g1'},
        {'id': 'p2', 'deps': [], 'group': 'g2'},
    ]
    g = DependencyGraph(projects)
    print(g['g1'])
    for group in g:
        print(group.name.upper())
        for levels in group:
            pprint.pprint(levels)
    
if __name__ == '__main__':
    main()
