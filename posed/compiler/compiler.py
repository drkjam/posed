"""A simple compiler targeting the instruction set for the VM."""

from posed.compiler.ast import BinaryOp, Constant, Add, Sub, Mul, Div
from posed.compiler.lexer import Lexer
from posed.compiler.parser import Parser
from posed.vm import VirtualMachine


class Compiler:
    def compile(self, expr, instructions=None):
        """Converts an AST into a set of executable VM instructions."""
        if instructions is None:
            instructions = []
        if isinstance(expr, Constant):
            instructions.append(('const', expr.value))
        elif isinstance(expr, Add):
            instructions.append(('add',))
        elif isinstance(expr, Sub):
            instructions.append(('sub',))
        elif isinstance(expr, Mul):
            instructions.append(('mul',))
        elif isinstance(expr, Div):
            instructions.append(('div',))
        elif isinstance(expr, BinaryOp):
            self.compile(expr.left, instructions)
            self.compile(expr.right, instructions)
            self.compile(expr.op, instructions)
        return instructions


def main():
    lexer = Lexer()
    parser = Parser(lexer)
    compiler = Compiler()

    program = '1 + 2 * 3 / 4'
    print(f'expr: {program!r}')

    ast = parser.parse(program)
    print(f'ast: {ast!r}')

    program = compiler.compile(ast)
    print(f'program: {program!r}')

    vm = VirtualMachine(functions=[], debug=True)
    vm.execute(instructions=program, locals_=None)
    print(f'result:', vm.pop())


if __name__ == '__main__':
    main()
