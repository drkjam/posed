import ply.yacc as yacc

from posed.compiler.lexer import Lexer
from posed.compiler.ast import BinaryOp, Add, Sub, Mul, Div, Constant


class Parser:
    def __init__(self, lexer, **kwargs):
        self.tokens = lexer.tokens
        self._parser = yacc.yacc(module=self, **kwargs)

    def p_expression_plus(self, p):
        'expression : expression PLUS term'
        p[0] = BinaryOp(op=Add(), left=p[1], right=p[3])

    def p_expression_minus(self, p):
        'expression : expression MINUS term'
        p[0] = BinaryOp(op=Sub(), left=p[1], right=p[3])

    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]

    def p_term_times(self, p):
        'term : term TIMES factor'
        p[0] = BinaryOp(op=Mul(), left=p[1], right=p[3])

    def p_term_div(self, p):
        'term : term DIVIDE factor'
        p[0] = BinaryOp(op=Div(), left=p[1], right=p[3])

    def p_term_factor(self, p):
        'term : factor'
        p[0] = p[1]

    def p_factor_num(self, p):
        'factor : NUMBER'
        p[0] = Constant(p[1])

    def p_factor_expr(self, p):
        'factor : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_error(self, p):
        """Error rule for syntax errors."""
        print("Syntax error in input!")

    def parse(self, data):
        """Generate an AST for the specified program."""
        return self._parser.parse(data)


def main():
    lexer = Lexer()
    parser = Parser(lexer)
    program = '1 + 2 * 3 / 4'
    print(f'expr: {program!r}')

    ast = parser.parse(program)
    print(f'ast: {ast!r}')


if __name__ == '__main__':
    main()
