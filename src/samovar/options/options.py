__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

OPTIONS = [
('Repository options', {
    'options': [
        ('repo', {
            'dest'    : 'selected_repositories',
            'action'  : 'append',
            'type'    : str,
            'help'    : 'Use only these repositories.      [ ALL ]',
        }),
        ('skip', {
            'dest'    : 'skipped_repositories',
            'action'  : 'append',
            'type'    : str,
            'help'    : 'Skip these repositories.          [ none ]',
        })
    ]
}),

]
