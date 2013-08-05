__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__date__      = '19 January 2013'
__copyright__ = 'Copyright (c) 2013 Viktor Kerkez'

from tea.utils import six
from tea.parsing import Token, Style, Lexer, RegexLexer
from samovar.utils import indent


class HgStyle(Style):
    styles = {
        Token.Text       : '',
        Token.NoChanges  : '#0000ff',
        Token.Changed    : '#ffff00',
        Token.Ok         : '#00ff00',
        Token.Failed     : '#ff0000',

        # Color tokens
        Token.Normal     : '',
        Token.White      : '#ffffff',
        Token.Red        : '#ff0000',
        Token.DarkRed    : '#800000',
        Token.Green      : '#00ff00',
        Token.DarkGreen  : '#008000',
        Token.DarkBlue   : '#000080',
        Token.DarkYellow : '#808000',
        Token.Cyan       : '#00ffff',
        Token.DarkCyan   : '#008080',
        Token.DarkPurple : '#800080',
        Token.DarkGray   : '#707070',
    }


class HgLexer(Lexer):
    config = {
        'statuses' : {
            0: Token.Ok
        }
    }

    def lex(self, data):
        # Merge statuses into config
        if 'statuses' not in self.config:
            self.config['statuses'] = HgLexer.config['statuses']
        text   = u'%s\n' % six.text_type(data['object']).strip('\n\r')
        status = data['status']
        if status in self.config['statuses']:
            token = self.config['statuses'][status]
        else:
            token = Token.Failed
        yield token, text
        if token not in (Token.Ok, Token.NoChanges, Token.Changed):
            error = data['data']['error'].strip()
            if error:
                yield Token.Text, indent(error) + '\n'
        elif self.config.get('parse', False):
            output = data['data']['output'].strip()
            if output:
                indent_size = self.config.get('indent', 2)
                if 'parser' in self.config:
                    lexer = RegexLexer()
                    lexer.push_config(self.config['parser'])
                    for token, text in lexer.tokenize(indent(output, indent_size) + '\n'):
                        yield token, text
                else:
                    yield Token.Text, indent(output) + '\n'


PARSERS = {
    'changeset': {
        'root': [
            (r'\schangeset:.*$', Token.DarkYellow, 'root'),
            (r'\suser:\s+',      Token.DarkYellow, 'user'),
        ],
        'user': [
            (r'.*$',               Token.DarkCyan,   'root'),
        ],
    },
    'diff': {
        'root': [
            (r'^diff.*$',          Token.White,      'root'),
            (r'^--- .*$',          Token.Red,        'root'),
            (r'^\+\+\+ .*$',       Token.Green,      'root'),
            (r'^\+[^\+].*$',       Token.DarkGreen,  'root'),
            (r'^-[^-].*$',         Token.DarkRed,    'root'),
            (r'^@@.*$',            Token.DarkPurple, 'root'),
            (r'^new file mode.*$', Token.Cyan,       'root'),
        ]
    },
    'status': {
        'root': [
            (r'\s*M.*$',           Token.DarkBlue,   'root'),
            (r'\s*A.*$',           Token.DarkGreen,  'root'),
            (r'\s*R.*$',           Token.DarkRed,    'root'),
            (r'\s*C.*$',           Token.Normal,     'root'),
            (r'\s*I.*$',           Token.DarkGray,   'root'),
            (r'\s*\?.*$',          Token.DarkPurple, 'root'),
            (r'\s*!.*$',           Token.DarkCyan,   'root'),
        ]
    }
}
