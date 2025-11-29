from pathlib import Path

import yaml

from M8085 import Parser
from M8085._parser import INSTRUCTION
from M8085 import Processor

PATH = Path(__file__).parent

with open(PATH / 'example.yml', 'r') as file:  
    f = yaml.safe_load(file)

    parser = Parser(f['test2'])

    struct = parser.structure

void = Processor(f['test0'])


prev_label = 'START'

def execute(stack:list):
    for instr in stack:

        mnemonic, operands = instr[0], instr[1:]
        print(f'Executing: {mnemonic} {operands}')

        if mnemonic == 'HLT':
            return 'HLT'

        if mnemonic == 'CALL':
            return operands[0]

        if mnemonic == 'RET':
            return 1

        if operands == []:
            try:
                void.inst[mnemonic]()
            except KeyError:
                pass
        else:
            try:
                void.inst[mnemonic](*operands)
            except KeyError:
                pass
    
    return 0

print(struct)

# labels = list(struct.keys())
# index = -1

# while True:

#     if not output:
#         label = labels.pop(0)

#     if index >= 0:
#         stack = struct[label][index:]
#     else:
#         stack = struct[label]

#     output = execute(stack)

#     if output == 'HLT':
#         break

#     if output:
#         if output == 'RET':
#             index = struct[prev_label].index(['CALL', label])
#             label = prev_label
        
#         else:
#             prev_label, label = label, output
