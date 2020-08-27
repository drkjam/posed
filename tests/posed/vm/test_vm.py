import pytest

from posed.vm import VirtualMachine, Function, InvalidOpcode, ExternalFunction


def test_vm():
    vm = VirtualMachine(functions=[])
    assert vm.stack == []
    assert len(vm.memory) == 65536
    assert vm.functions == []


def test_vm_load_and_store():
    mem_size = 16
    vm = VirtualMachine(functions=[], memory_size=mem_size)
    assert vm.memory == b'\x00' * mem_size

    vm.store(0, 1024.0)
    vm.store(8, 42.0)
    assert vm.load(0) == 1024.0
    assert vm.load(8) == 42.0
    assert len(vm.memory) == mem_size


def test_vm_stack_operations():
    vm = VirtualMachine(functions=[])
    assert vm.stack == []
    vm.push(1.0)
    vm.push(2.0)
    vm.push(3.0)
    assert vm.stack == [1.0, 2.0, 3.0]
    assert vm.pop() == 3.0
    assert vm.pop() == 2.0
    assert vm.pop() == 1.0

    with pytest.raises(IndexError):
        assert vm.pop()


def test_vm_function_call_with_return_value():
    add = Function(nparams=2, returns=True, code=[
        ('local.get', 0),
        ('local.get', 1),
        ('sub',),
    ])

    vm = VirtualMachine(functions=[add])
    vm.execute(instructions=[
        ('const', 2.0),
        ('const', 3.0),
        ('call', 0),
    ], locals_=None)
    assert vm.pop() == -1.0


def test_vm_function_call_without_return_value():
    x_addr = 0
    save = Function(nparams=0, returns=False, code=[
        ('const', x_addr),
        ('const', 42.0),
        ('store',),
        ('return',),    # Optional
    ])

    vm = VirtualMachine(functions=[save])
    vm.execute(instructions=[
        ('call', 0),
    ], locals_=None)
    assert vm.load(x_addr) == 42.0
    assert vm.stack == []


def test_vm_external_function_call():
    value = 42.0

    def inc_value():
        nonlocal value
        value += 1

    py_inc_value = ExternalFunction(nparams=0, returns=False, call=inc_value)

    assert value == 42.0

    vm = VirtualMachine(functions=[py_inc_value])
    vm.execute(instructions=[
        ('call', 0),
        ('call', 0),
        ('call', 0),
    ], locals_=None)

    assert value == 45.0
    assert vm.stack == []


@pytest.mark.parametrize("x, y, opcode, expected_result", [
    (2.0, 3.0, 'add', 5.0),
    (2.0, 3.0, 'mul', 6.0),
    (2.0, 3.0, 'sub', -1.0),
    (6.0, 2.0, 'div', 3.0),
    (1.0, 2.0, 'le', True),
    (2.0, 2.0, 'le', True),
    (2.0, 1.0, 'le', False),
    (1.0, 2.0, 'ge', False),
    (2.0, 2.0, 'ge', True),
    (2.0, 1.0, 'ge', True),
])
def test_vm_execute_binary_expr(x, y, opcode, expected_result):
    vm = VirtualMachine(functions=[])
    program = [
        ('const', x),
        ('const', y),
        (opcode,),
    ]
    assert vm.stack == []
    vm.execute(instructions=program, locals_=None)
    assert vm.stack == [expected_result]
    assert vm.pop() == expected_result
    assert vm.stack == []


def test_vm_execute_load_store():
    vm = VirtualMachine(functions=[])
    program = [
        ('const', 0),
        ('const', 42.0),
        ('store',),
        ('const', 0),
        ('load',),
    ]
    assert vm.stack == []
    vm.execute(instructions=program, locals_=None)
    assert vm.pop() == 42.0
    assert vm.stack == []


def test_vm_execute_while_loop():
    #   x = 10
    #   while x >= 5
    #       x = x - 1
    x_addr = 0
    program = [
        ('const', x_addr),
        ('const', 10.0),
        ('store',),
        ('block', [
            ('loop', [    # label : 0
                # CONDITION
                ('const', 5.0),
                ('const', x_addr),
                ('load',),
                ('ge',),
                ('br_if', 1),     # goto 1: (break)
                # BODY
                ('const', x_addr),
                ('const', x_addr),
                ('load',),
                ('const', 1.0),
                ('sub',),
                ('store',),
                ('br', 0),        # goto 0 (continue)
            ]),
        ]),     # label : 1
    ]

    vm = VirtualMachine(functions=[])
    vm.execute(instructions=program, locals_=None)
    assert vm.load(x_addr) == 5.0
    assert vm.stack == []


def test_vm_invalid_opcode():
    vm = VirtualMachine(functions=[])

    with pytest.raises(InvalidOpcode):
        vm.execute(instructions=[('foo',),], locals_=None)
