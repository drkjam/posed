from posed.compiler.lexer import Lexer
from posed.compiler.parser import Parser
from posed.compiler.compiler import Compiler
from posed.vm import VirtualMachine


class REPL:
    """An interactive REPL (read evaluate print loop)."""
    def __init__(self):
        self._lexer = Lexer()
        self._parser = Parser(self._lexer)
        self._compiler = Compiler()
        self._vm = VirtualMachine(functions=[], debug=False)

    def start(self, prompt='> '):
        """Start the REPL."""
        while True:
            try:
                text = input(prompt)
            except EOFError:
                break
            if not text:
                continue
            ast = self._parser.parse(text)
            program = self._compiler.compile(ast)
            self._vm.execute(instructions=program, locals_=None)
            print(self._vm.pop())


def main():
    repl = REPL()
    repl.start()


if __name__ == '__main__':
    main()
