from M8085 import Arithmetic, Register, Data, Memory, Logical, Peripheral


arithmetic = Arithmetic()
data = Data()
register = Register()
peripheral = Peripheral()
logical = Logical()
memory = Memory()

arithmetic_inst = arithmetic.get_inst()

arithmetic_inst['ADD']('B')
print(register.read('A'))  # Expected output: 90H


data_inst = data.get_inst()
data_inst['MVI'](['B', '15H'])
print(register.get_all())  # Expected output: 15H

logical_inst = logical.get_inst()
logical_inst['ANA']('B')
print(register.read('A'))  # Expected output: 10H

peripheral_inst = peripheral.get_inst()
peripheral_inst['IN']('01H')
print(register.read('A'))  # Expected output: 01H