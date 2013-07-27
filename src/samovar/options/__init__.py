__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import os
import re

from tea.logger import * #@UnusedWildImport

# autotest imports
from .options import OPTIONS
from .defaults import DEFAULTS


def check_and_set_func(o):
    return o
