import logging

from posed.vm import VirtualMachine, Function, ExternalFunction


def main():
    #   fun countdown(x)
    #       while x >= 0:
    #           print(x)
    #           x = x - 1

    countdown = Function(nparams=1, returns=False, code=[
        ('block', [
            ('loop', [          # label : 0
                ('local.get', 0),
                ('call', 0),

                #   test
                ('const', 0.0),
                ('local.get', 0),
                ('ge',),
                ('br_if', 1),   # break

                # body
                ('local.get', 0),
                ('const', 1.0),
                ('sub',),
                ('local.set', 0),

                ('br', 0),      # continue
            ]),
        ]),                     # label : 1
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
