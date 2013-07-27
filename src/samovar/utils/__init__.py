__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '02 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

import json
from .other import *


def humanize(time):
    time = int(time)
    if time < 60:
        return '00:00:%02d' % time
    elif time < 3600:
        return '00:%02d:%02d' % (time / 60, time % 60)
    elif time < 86400:
        return '%02d:%02d:%02d' % (time / 3600, (time % 3600) / 60, (time % 3600) % 60)
    else:
        return '%s days %s' % (time / 86400, humanize(time % 86400))

def indent(text, indent=2):
    return '\n'.join(['%s%s' % (indent*' ', line) for line in text.splitlines()])


def serial_json(data):
    decoder = json.JSONDecoder()
    items   = []
    while len(data) > 0:
        try:
            item, offset = decoder.raw_decode(data)
            items.append(item)
            data = data[offset:]
        except ValueError: break 
    return items, data
