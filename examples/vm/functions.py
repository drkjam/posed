from posed.vm import VirtualMachine, Function


def main():
    #   fun add(x, y):
    #       return x + y
    add = Function(nparams=2, returns=True, code=[
        ('local.get', 0),   # x
        ('local.get', 1),   # y
        ('add',),
    ])

    mul = Function(nparams=2, returns=True, code=[
        ('local.get', 0),   # x
        ('local.get', 1),   # y
        ('mul',),
    ])

    div = Function(nparams=2, returns=True, code=[
        ('local.get', 0),   # x
        ('local.get', 1),   # y
        ('div',),
    ])

    functions = [
        add,
        mul,
        div,
    ]

    #   div(mul(add(1.0, 2.0), 5.0), 3.0)
    program = [
        ('const', 1.0),
        ('const', 2.0),
        ('call', 0),
        ('const', 5.0),
        ('call', 1),
        ('const', 3.0),
        ('call', 2),
    ]

    vm = VirtualMachine(functions=functions, debug=False)
    vm.execute(instructions=program, locals_=None)
    print(f'result:', vm.pop())


main()
