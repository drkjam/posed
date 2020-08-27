from posed.vm import VirtualMachine


def example1():
    #   expressions

    #   2 + 3
    program = [
        ('const', 2.0),
        ('const', 3.0),
        ('mul',),
    ]

    m = VirtualMachine(functions=[], debug=True)
    m.execute(instructions=program, locals_=None)
    print(f'result:', m.pop())


def example2():
    #   variable assignment

    #   x = 2 + 3
    x_addr = 0
    program = [
        ('const', x_addr),
        ('const', 2.0),
        ('const', 3.0),
        ('add',),
        ('store',),
    ]

    vm = VirtualMachine(functions=[], debug=True)
    vm.execute(instructions=program, locals_=None)
    print(f'result:', vm.load(x_addr))


example1()
example2()