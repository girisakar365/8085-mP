from pathlib import Path

from M8085 import Parser

from M8085._utils import decode, INSTRUCTION
from M8085._memory import _STACK, Assembler, stack

PATH = Path(__file__).parent.parent / 'Programs'

with open(PATH / 'test_db.asm', 'r') as file:
    test = file.read()
    print(test)
    parser = Parser(test)

    print(parser.parse())

    # print(_STACK)
    pc = Assembler()
    pc.pass2()

    print(stack())
