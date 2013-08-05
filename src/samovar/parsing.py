__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '19 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

from tea.utils import six
from tea.parsing import Lexer, Token, Style


class StatusStyle(Style):
    styles = {
        Token.Ok      : '#00ff00',
        Token.Failed  : '#ff0000',
        Token.Unknown : '#ffff00',
        Token.Other   : '#0000ff',
    }


class StatusLexer(Lexer):
    config = {
        0: Token.Ok,
    }

    def lex(self, data):
        text   = u'%s\n' % six.text_type(data['object']).strip('\n\r')
        status = data['status']
        if status in self.config:
            yield self.config[status], text
        else:
            yield Token.Failed, text
