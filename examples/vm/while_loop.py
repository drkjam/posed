import logging

from posed.vm import VirtualMachine, ExternalFunction


def main():
    #   x = 0
    #   while x < 10
    #       x = x + 1

    x_addr = 42
    program = [
        ('block', [
            #   assign counter
            ('const', x_addr),
            ('const', 0.0),
            ('store',),
            ('loop', [
                #   check condition
                ('const', 10.0),
                ('const', x_addr),
                ('load',),
                ('le',),
                ('br_if', 1),   # break

                #   body
                ('const', x_addr),
                ('load',),
                ('call', 0),

                ('const', x_addr),
                ('const', x_addr),
                ('load',),
                ('const', 1.0),
                ('add',),
                ('store',),

                ('br', 0),      # continue
            ]
             ),
        ]
         ),
    ]

    def show_value(x):
        logging.info(f'PRINT: {x}')

    functions = [
        ExternalFunction(nparams=1, returns=False, call=show_value),
    ]

    vm = VirtualMachine(functions=functions, debug=False)
    vm.execute(instructions=program, locals_=None)


main()
