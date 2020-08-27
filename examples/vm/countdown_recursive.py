import logging

from posed.vm import VirtualMachine, Function, ExternalFunction


def main():
    # fun countdown(x)
    #     print(x)
    #     if x <= 0:
    #         return x
    #     else:
    #         countdown(x - 1)

    countdown = Function(nparams=1, returns=False, code=[
        ('local.get', 0),
        ('call', 0),
        ('block', [
            ('block', [
                #   test
                ('const', 1.0),
                ('local.get', 0),
                ('le',),

                ('br_if', 0),
                #   alternative
                ('br', 1),
            ]),
            #   consequence
            ('local.get', 0),
            ('const', 1.0),
            ('sub',),
            ('call', 1)
        ]),
    ])

    program = [
        ('const', 10.0),
        ('call', 1),
    ]

    def show_value(x):
        logging.info(f'PRINT: {x}')

    functions = [
        ExternalFunction(nparams=1, returns=False, call=show_value),
        countdown,
    ]

    vm = VirtualMachine(functions=functions, debug=False)
    vm.execute(instructions=program, locals_=None)


main()
