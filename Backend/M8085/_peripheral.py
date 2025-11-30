from ._base import Instruction
from ._memory import Memory, Register

class Peripheral(Instruction):

    def __init__(self):
        self._port:Memory = Memory()
        self._register:Register = Register()

    def __in(self, port:str):
        self._register['A'] = port

    def __out(self, port: str):
        self._port[port] = self._register['A']

    def get_inst(self):
        return {
            'IN':self.__in,
            'OUT':self.__out,
        }