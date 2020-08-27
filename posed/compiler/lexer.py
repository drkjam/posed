import ply.lex as lex


class Lexer:
    def __init__(self, **kwargs):
        self._lexer = lex.lex(module=self, **kwargs)

    # List of token names
    tokens = (
        'NUMBER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
    )

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+\.?\d?'
        t.value = float(t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    #   Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def analyse(self, data):
        """Test the lexer on some input data."""
        self._lexer.input(data)
        while True:
            tok = self._lexer.token()
            if not tok:
                break
            print(tok)
            # print(tok.type, tok.value, tok.lineno, tok.lexpos)


if __name__ == '__main__':
    # Build the lexer
    lexer = Lexer()
    lexer.analyse('1 + 2 * 3 / 4')
