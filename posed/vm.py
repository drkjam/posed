"""
A simple virtual machine in Python.

Features
--------
- stack based execution model
- basic linear heap memory storage model and pointer access
- expressions
- functions (including local variables)
- blocks (groups of expressions)
- branching (if statements)
- looping

Conditionals
------------
   if (test) { consequence } else { alternative }

   ('block', [
       ('block', [
           test
           ('br_if, 0), # goto 0
           alternative,
           ('br', 1),   # goto 1
       ]), # label : 0
       consequence,
   ]) # label : 1

Loops
-----
   while (test) { body }

   ('block', [
       ('loop', [ # label : 0
           not test
           ('br_if', 1), # goto 1: (break)
           body
           ('br', 0),    # goto 0 (continue)
       ])
   ]) # label : 1

"""
import logging
import operator as op
import struct


def logging_setup(debug=False):
    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")


class VirtualMachineError(Exception):
    pass


class InvalidOpcode(VirtualMachineError):
    pass


class Function:
    def __init__(self, nparams, returns, code):
        self.nparams = nparams
        self.returns = returns
        self.code = code


class ExternalFunction:
    def __init__(self, nparams, returns, call):
        self.nparams = nparams
        self.returns = returns
        self.call = call


class Break(Exception):
    def __init__(self, level):
        self.level = level


class Return(Exception):
    pass


BINARY_OPS = {
    'add': op.add,
    'sub': op.sub,
    'mul': op.mul,
    'div': op.truediv,
    'mod': op.mod,
    'ge': op.ge,
    'gt': op.gt,
    'le': op.le,
    'lt': op.lt,
    'eq': op.eq,
    'ne': op.ne,
}


class VirtualMachine:
    """A simple stack based virtual machine with basic linear memory."""
    def __init__(self, functions, memory_size=65536, debug=False):
        self.functions = functions              # function table
        self.memory = bytearray(memory_size)    # memory
        self.stack = []                         # stack
        self._logger = logging.getLogger(self.__class__.__name__)
        logging_setup(debug=debug)

    def debug(self, msg):
        """Print a debug message."""
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(msg)

    def load(self, addr):
        """Load a value from the specified address."""
        return struct.unpack('<d', self.memory[addr:addr+8])[0]

    def store(self, addr, val):
        """Store a value at the specified address."""
        self.memory[addr:addr+8] = struct.pack('<d', val)

    def push(self, item):
        """Push an instruction onto the call stack."""
        self.stack.append(item)

    def pop(self):
        """Pop an instruction off the call stack."""
        return self.stack.pop()

    def call(self, func, *args):
        """Call a specified function with args."""
        locals_ = dict(enumerate(args))
        if isinstance(func, Function):
            try:
                self.execute(func.code, locals_)
            except Return:
                pass
            if func.returns:
                return self.pop()
        else:
            return func.call(*args)     # External function

    def execute(self, instructions, locals_):
        """Execute instructions."""
        for opcode, *args in instructions:
            self.debug(f'OPCODE: {opcode}, ARGS: {args}')
            if opcode == 'const':
                self.push(args[0])
            elif opcode in BINARY_OPS:
                operator = BINARY_OPS[opcode]
                right = self.pop()
                left = self.pop()
                self.push(operator(left, right))
            elif opcode == 'load':
                addr = self.pop()
                self.push(self.load(addr))
            elif opcode == 'store':
                val = self.pop()
                addr = self.pop()
                self.store(addr, val)
            elif opcode == 'local.get':
                self.push(locals_[args[0]])
            elif opcode == 'local.set':
                locals_[args[0]] = self.pop()
            elif opcode == 'call':
                func = self.functions[args[0]]
                fargs = reversed([self.pop() for _ in range(func.nparams)])
                result = self.call(func, *fargs)
                if func.returns:
                    self.push(result)
            elif opcode == 'br':
                raise Break(args[0]) 
            elif opcode == 'br_if':
                if self.pop():
                    raise Break(args[0])
            elif opcode == 'block':
                try:
                    self.execute(args[0], locals_)
                except Break as b:
                    if b.level > 0:
                        b.level -= 1
                        raise
            elif opcode == 'loop':
                while True:
                    try:
                        self.execute(args[0], locals_)
                        break
                    except Break as b:
                        if b.level > 0:
                            b.level -= 1
                            raise
            elif opcode == 'return':
                raise Return()
            else:
                raise InvalidOpcode(f'Unsupported opcode {opcode}')

            self.debug(f'STACK: {self.stack}')


def main():
    #   1 + 2 * 3 / 4
    instructions = [
        ('const', 1.0),
        ('const', 2.0),
        ('const', 3.0),
        ('mul',),
        ('const', 4.0),
        ('div',),
        ('add',),
    ]

    vm = VirtualMachine(functions=[], debug=True)
    vm.execute(instructions=instructions, locals_=None)
    print(f'result:', vm.pop())


if __name__ == '__main__':
    main()
