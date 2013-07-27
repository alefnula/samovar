from __future__ import print_function

__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import re
from datetime import datetime
# tea imports
from tea.cron import Cron
from tea.commander import BaseCommand

pattern = re.compile('^(?P<year>[^\|]+)\|(?P<month>[^\|]+)\|(?P<day>[^\|]+)\|(?P<day_of_week>[^\|]+)\|(?P<hour>[^\|]+)\|(?P<minute>[^\|]+)\|(?P<second>.+)$')

def cronparse(s):
    match = pattern.match(s)
    if match is not None:
        print(match.groupdict())
        return Cron(**match.groupdict())
    return None

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if args:
            a = args[0]
        else:
            a = '*|*|*|*|*|*|*'
        ct = cronparse(a)
        print(ct)
        if ct is not None:
            print(ct.get_next_fire_time(datetime.now()))
