"""Stack and control instructions: PUSH, POP, XTHL, SPHL, PCHL, ORG, DB, HLT, RST."""

from ._base import Instruction
from ._utils import encode,decode
from ._memory import Flag, Memory, Register, decode_rp, encode_rp

class Stack(Instruction):
    """Implements stack operations and assembler directives (ORG, DB)."""
    def __init__(self):
        self._stack:Memory = Memory()
        self._register:Register = Register()
        self._flag:Flag = Flag()

    def __push(self, rp:str):
        self._register['SP'] = encode(decode(self._register['SP'])-1, bit=4)
        self._stack[self._register['SP']] = decode_rp(rp=rp)

    def __pop(self,rp:str):
        encode_rp(value=self._stack[self._register['SP']], rp=rp)
        self._register['SP'] = encode(decode(self._register['SP'])+1, bit=4)

    def __xthl(self):
        data = decode_rp(rp='H')
        data, self._register['SP'] = self._register['SP'], data
        encode_rp(data,rp='H')

    def __sphl(self):
        self._register['SP'] = decode_rp(rp='H')
    
    def __pchl(self):
        self._register['PC'] = decode_rp(rp='H')

    def __org(self,addr):
        self._stack['IDX'] = addr
    
    def __db(self,*arg):
        if self._stack['IDX'] == '00H':
            self._stack['IDX'] = 'C000H'
        for num in arg:
            curr = self._stack['IDX']
            self._stack[curr] = num
            self._stack['IDX'] = encode( ( decode(curr) + 1 ) & 0xffff, bit=4 )
    
    def __hlt(self):
        pass
    
    def __rst55(self):
        self._stack.reset()
        self._register.reset()
        self._flag.reset()
                
        return {
            "success": True,
            "checkpoint": "reset",
            "message": "Components reset to default values",
            "defaultState": {
                "registers": self._register.get_all(),
                "flags": self._flag.get_all(),
                "memory": self._stack.get_all()
            }
        }

    def get_inst(self):
        return {
            "PUSH": self.__push,
            "POP": self.__pop,
            "XTHL": self.__xthl,
            "SPHL": self.__sphl,
            "PCHL": self.__pchl,
            "ORG": self.__org,
            "DB": self.__db,
            "HLT": self.__hlt,
            "RST5.5": self.__rst55,
        }