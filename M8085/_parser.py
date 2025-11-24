import pyparsing as pp

from ._utils import encode, decode, INSTRUCTION
from ._memory import Assembler

IDENTIFIER = pp.Word(pp.alphas + "_", pp.alphanums + "_")  # label
HEX_ADDRESS = pp.Regex(r'[0-9A-F]+H') # e.g. 2000H
REGISTER = pp.Word("ABCDEHLM", exact=1) | pp.Literal("SP") | pp.Literal("PSW") | pp.Literal('PC')
MNEMONICS =  pp.MatchFirst(
map(lambda m:pp.Keyword(m), INSTRUCTION.keys())
) ('inst')
MEMORY_RANGE:range = range(65536)
PORT_RANGE:range = range(256)

class Message:
    def __init__(
        self, msg=None, inst=None, pos=None, line=None, tag=None, format=None
        ) -> str:
        self.msg = msg
        self.inst = inst
        self.pos = pos
        self.line = line
        self.format = format
        self.tag = tag
        self.general = ''
        # self.general = f'{self.msg} for {self.inst} at {self.pos} -> {self.line}'

    def __tag_map(self) -> str:

        msg = {
        'm:8': '8-bit Memory Address is reserved or out of range',
        'm:16': '16-bit Memory Address is reserved or out of range',
        'r': 'Invalid Register Used',
        'rp': 'Invalid Register Pair Used',
        'l': 'Undefined Label Reference',
        'db': 'Invalid integer value'
        }

        self.general = f'{msg.get(self.tag)}.'

    def __str__(self) -> str:
        if self.msg:
            self.general = f'{self.msg}.'
        elif self.tag:
            self.__tag_map()

        if self.inst:
            self.general += f' Instruction: {self.inst}.'
        if self.pos:
            self.general += f' at {self.pos}.'
        if self.line:
            self.general += f' -> {self.line}.'
        if self.format:
            self.general += f'\nHint: {self.format}'

        return self.general
    
    def as_dict(self):
        self.__str__()
        return {
            "error":True,
            "message": self.msg,
            "details":{
                "instruction": self.inst,
                "position": self.pos,
                "line": self.line,
                "tag": self.tag,
                "hint": self.format,
            }
        }
    
    def __iter__(self):
        self.__str__()
        yield from self.general

class Parser:

    def __init__(self,code:str):
        # Label definition: LABEL:
        label = pp.Combine(IDENTIFIER + pp.Suppress(":")) ('label')
        #operands
        operand = IDENTIFIER | HEX_ADDRESS
        #instruction
        instruction = (
        MNEMONICS + pp.Optional(operand('op1') + pp.Optional(pp.Suppress(",") + operand('op2')))
        )('code')
        # Comment: ; rest of line
        comment = pp.Group(pp.Suppress(";") + pp.restOfLine) ('comment')

        self._rules = (
            label + instruction + comment |
            label + instruction |
            label + comment |
            instruction + comment |
            label |
            instruction |
            comment
        )

        self._code = code.upper()
        self._operand = {
        'm:8': self.__check_addr8,
        'm:16': self.__check_addr16,
        'r': self.__check_register,
        'l': self.__check_reference,
        'rp': self.__check_rp,
        'db': self.__check_db
        }

        self.__halt = False

        self.__pc = Assembler()

    def __preprocess(self):
        return filter(lambda line: line.strip() != '', self._code.splitlines())

    def __add_line_info(self,parsed:dict, line:str, idx:int):
        parsed['pos'] = f"line: {idx}"
        parsed['line'] = line.strip()
        return parsed

    def parse(self):
        for idx, line in enumerate(self.__preprocess(), start=1):
            try:
                parsed = self._rules.parseString(line)
                wrapped = self.__add_line_info(parsed.asDict(), line, idx)
                result = self._param_check(wrapped)
                if isinstance(result,Message):
                    return result
            except pp.ParseException as p:
                key = p.found[1:-1] # p.found is in quotes by default. Removed them.
                if key in map(lambda m:m, INSTRUCTION.keys()):
                    expected = INSTRUCTION[key]['syntax']
                    return Message('Invalid Syntax',key,f'line: {idx}',p.line,format=expected)
                else:
                    return Message('Invalid Syntax',p.found,f'{idx}',p.line)
        
        if not self.__halt: return Message('Infinite Execution Detected. No HLT instruction found.')

    def _param_check(self,line:dict[str:str]):
        if 'inst' in line:
            if line['inst'] == 'HLT': self.__halt = True

            inst = line['inst']
            code = line['code']
            param_rule = INSTRUCTION[inst]['param_rule']

            if param_rule:
                if len(code[1:]) != len(param_rule):
                    return Message('Invalid Operand',inst,line['pos'],line['line'],
                        format=INSTRUCTION[inst]['syntax']
                    )

                for i in range(len(param_rule)):
                    operand = code[i+1]
                    rule = param_rule[i]
                    result = self._operand.get( rule )( operand )
                    if not result:
                        syntax = INSTRUCTION[inst]['syntax']
                        return Message('Invalid',inst,line['pos'],line['line'],tag=rule,format=syntax)
            
            if code[0] == 'DB':
                result = self._operand.get('db')(line['line'])
                if isinstance(result, Message): return result
                else:
                    line['inst'], line['code'] = result
        
        self.__pc.pass1(line)

    def __check_addr8(self,operand:str): 
        if len(operand) == 3 and operand.endswith('H'):
            return decode(operand) in PORT_RANGE
        return False

    def __check_addr16(self,operand:str): 
        if len(operand) == 5 and operand.endswith('H'):
            return decode(operand) in MEMORY_RANGE
        return False

    def __check_register(self,operand:str): 
        try:
            REGISTER.parseString(operand,parseAll=True)
            return True
        except pp.ParseException: return False

    def __check_reference(self,operand:str): return self._code.find(operand) != -1

    def __check_rp(self,operand:str): return operand in ['B','D','H']

    def __check_db(self,operand:str):
        line = operand
        split = operand.split(' ')
        inst, operand = split[0], split[1:]
        try:
            operand = [int(_) for _ in operand[0].split(',')]
        except ValueError:
            return Message('Invalid Input',inst,line=line,
                    tag='db',format=INSTRUCTION['DB']['syntax']
                )
        else: return inst, [inst] + [encode(_) for _ in operand if 0 <= _ <= 255] 