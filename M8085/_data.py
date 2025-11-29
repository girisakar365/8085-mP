from ._base import Instruction
from ._memory import Memory, Register, decode_rp, encode_rp
from ._utils import encode, decode
from .logs import setup_logger, error

setup_logger()
class Data(Instruction):

    def __init__(self):
        self._memory:Memory = Memory()
        self._register:Register = Register()

    def __mov(self,rd:str,rs:str):
        if rd == 'M':
            self._memory[decode_rp()] =  self._register[rs]
        elif rs == 'M':
            self._register[rd] = self._memory[decode_rp()]
        else:
            self._register[rd] = self._register[rs]

    def __mvi(self,r:str,data:str):
        if r == 'M':
            self._memory[decode_rp()] =  data
        else:
            self._register[r] = data

    def __lxi(self,rp:str,data:str):
        encode_rp(data, rp)

    def __lda(self,ma:str):
        self._register['A'] =  self._memory[ma]
    
    def __sta(self, ma:str):
        self._memory[ma] = self._register['A']    

    def __ldax(self,rp:str):
        if rp == 'B':
            self._register['A'] = self._memory[decode_rp('B')]
        elif rp == 'D':
            self._register['A'] = self._memory[decode_rp('D')]
        else:
            error(f"Invalid Register Pair: {rp}")
    
    def __stax(self,rp:str):
        if rp == 'B':
            self._memory[decode_rp('B')] = self._register['A']
        elif rp == 'D':
            self._memory[decode_rp('D')] = self._register['A']
        else:
            error(f"Invalid Register Pair: {rp}")

    def __lhld(self,ma:str):
        self._register['L'] = self._memory[ma]
        self._register['H'] = self._memory[encode(decode(ma) + 1)]

    def __shld(self,ma:str):
        self._memory[ma] = self._register['L']
        self._memory[encode(decode(ma) + 1)] = self._register['H']
    
    def __xchg(self):
        self._register['D'],self._register['H'] = self._register['H'],self._register['D']
        self._register['E'],self._register['L'] = self._register['L'],self._register['E']

    def get_inst(self):
        return {
            'MOV':self.__mov,
            'MVI':self.__mvi,
            'LXI':self.__lxi,
            'LDA':self.__lda,
            'STA':self.__sta,
            'LDAX':self.__ldax,
            'STAX':self.__stax,
            'LHLD':self.__lhld,
            'SHLD':self.__shld,
            'XCHG':self.__xchg
        }