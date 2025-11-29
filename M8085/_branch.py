from ._base import Instruction
from ._memory import Register, Flag
from ._utils import operate

class Branch(Instruction):
    
    def __init__(self):
        self._register = Register()
        self._flag = Flag()

    def __jmp(self,address:str):
        self._register['PC'] = address

    def __jc(self,address:str):
        if self._flag['C'] == 1: self._register['PC'] = address
        else: self._register['PC'] = operate(self._register['PC'], 3, bit=4)

    def __jnc(self,address:str):
        if self._flag['C'] == 0: self._register['PC'] = address
        else: self._register['PC'] = operate(self._register['PC'], 3, bit=4)
    
    def __jz(self,address:str):
        if self._flag['Z'] == 1: self._register['PC'] = address
        else: self._register['PC'] = operate(self._register['PC'], 3, bit=4)

    def __jnz(self,address:str):
        if self._flag['Z'] == 0: self._register['PC'] = address
        else: self._register['PC'] = operate(self._register['PC'], 3, bit=4)
    def __jp(self,address:str):
        if self._flag['S'] == 0: self._register['PC'] = address
        else: self._register['PC'] = operate(self._register['PC'], 3, bit=4)

    def __jm(self,address:str):
        if self._flag['S'] == 1: self._register['PC'] = address
        else: self._register['PC'] = operate(self._register['PC'], 3, bit=4)
    
    def __jpe(self,address:str):
        if self._flag['P'] == 1: self._register['PC'] = address
        else: self._register['PC'] = operate(self._register['PC'], 3, bit=4)
    def __jpo(self,address:str):
        if self._flag['P'] == 0: self._register['PC'] = address
        else: self._register['PC'] = operate(self._register['PC'], 3, bit=4)

    def __call(self,address:str):
        self._register['SP'] = operate(self._register['PC'], 3, bit=4)
        self._register['PC'] = address
    
    def __cc(self,address:str):
        if self._flag['C'] == 1:
            self._register['SP'] = operate(self._register['PC'], 3, bit=4)
            self._register['PC'] = address

    def __cnc(self,address:str):
        if self._flag['C'] == 0:
            self._register['SP'] = operate(self._register['PC'], 3, bit=4)
            self._register['PC'] = address

    def __cz(self,address:str):
        if self._flag['Z'] == 1:
            self._register['SP'] = operate(self._register['PC'], 3, bit=4)
            self._register['PC'] = address
    
    def __cnz(self,address:str):
        if self._flag['Z'] == 0:
            self._register['SP'] = operate(self._register['PC'], 3, bit=4)
            self._register['PC'] = address

    def __cp(self,address:str):
        if self._flag['S'] == 0:
            self._register['SP'] = operate(self._register['PC'], 3, bit=4)
            self._register['PC'] = address

    def __cm(self,address:str):
        if self._flag['S'] == 1:
            self._register['SP'] = operate(self._register['PC'], 3, bit=4)
            self._register['PC'] = address

    def __cpe(self,address:str):
        if self._flag['P'] == 1:
            self._register['SP'] = operate(self._register['PC'], 3, bit=4)
            self._register['PC'] = address
    
    def __cpo(self,address:str):
        if self._flag['P'] == 0:
            self._register['SP'] = operate(self._register['PC'], 3, bit=4)
            self._register['PC'] = address
    
    def __ret(self):
        self._register['PC'] = self._register['SP']
    
    def __rcc(self):
        if self._flag['C'] == 1:
            self._register['PC'] = self._register['SP']
    
    def __rnc(self):
        if self._flag['C'] == 0:
            self._register['PC'] = self._register['SP']
    
    def __rz(self):
        if self._flag['Z'] == 1:
            self._register['PC'] = self._register['SP']

    def __rnz(self):
        if self._flag['Z'] == 0:
            self._register['PC'] = self._register['SP']
    
    def __rp(self):
        if self._flag['S'] == 0:
            self._register['PC'] = self._register['SP']
    
    def __rm(self):
        if self._flag['S'] == 1:
            self._register['PC'] = self._register['SP']
    
    def __rpe(self):
        if self._flag['P'] == 1:
            self._register['PC'] = self._register['SP']
    
    def __rpo(self):
        if self._flag['P'] == 0:
            self._register['PC'] = self._register['SP']
    
    def get_inst(self):
        return {
            'JMP': self.__jmp,
            'JC': self.__jc,
            'JNC': self.__jnc,
            'JZ': self.__jz,
            'JNZ': self.__jnz,
            'JP': self.__jp,
            'JM': self.__jm,
            'JPE': self.__jpe,
            'JPO': self.__jpo,
            'CALL': self.__call,
            'CC': self.__cc,
            'CNC': self.__cnc,
            'CZ': self.__cz,
            'CNZ': self.__cnz,
            'CP': self.__cp,
            'CM': self.__cm,
            'CPE': self.__cpe,
            'CPO': self.__cpo,
            'RET': self.__ret,
            'RCC': self.__rcc,
            'RNC': self.__rnc,
            'RZ': self.__rz,
            'RNZ': self.__rnz,
            'RP': self.__rp,
            'RM': self.__rm,
            'RPE': self.__rpe,
            'RPO': self.__rpo
        }