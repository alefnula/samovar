__author__ = 'Viktor Kerkez <alefnula@gmail.com>'
__date__ = '20 October 2010'
__copyright__ = 'Copyright (c) 2010 Viktor Kerkez'

import io
from distutils.core import setup

setup(
    name='samovar',
    version='0.0.1',
    description='samovar is a workspace management tool',
    long_description=io.open('README.rst', 'r', encoding='utf-8').read(),
    platforms=['Windows', 'POSIX', 'MacOS'],
    author='Viktor Kerkez',
    author_email='alefnula@gmail.com',
    maintainer='Viktor Kerkez',
    maintainer_email='alefnula@gmail.com',
    url='https://bitbucket.org/alefnula/samovar',
    license='BSD',
    packages=[
        'samovar',
        'samovar.commander',
        'samovar.commands',
        'samovar.commands.build',
        'samovar.commands.hg',
        'samovar.commands.other',
        'samovar.commands.repo',
        'samovar.options',
        'samovar.parsing',
        'samovar.scm'
        'samovar.utils',
    ],
    package_dir={'': 'src'},
    scripts=[
        'scripts/sv.py',
    ],
    install_requires=[
        'tea >= 0.0.3',
    ]
)
