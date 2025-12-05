"""M8085 - Intel 8085 Microprocessor Simulator.

Main entry point: Processor class accepts assembly code and executes it.

Example:
    result = Processor(code).as_dict()
"""

from ._parser import Parser
from ._utils import Message, operate, INSTRUCTION
from ._arithmetic import Arithmetic
from ._data import Data
from ._logical import Logical
from ._peripheral import Peripheral
from ._stack import Stack
from ._branch import Branch
from ._timing import TimingDiagram
from ._memory import Memory, Register, Flag, Assembler
from .logs import setup_logger, info

RUNTIME = 10000
setup_logger()
class Processor:
    """Main simulator class. Parses, assembles, and executes 8085 code.
    
    Execution flow:
    1. Parse assembly code (syntax validation)
    2. Assemble (label resolution, pass2)
    3. Execute instructions until HLT
    4. Return final processor state
    """

    def __init__(self,input:str):

        self.__arithmetic = Arithmetic()
        self.__data = Data()
        self.__logical = Logical()
        self.__peripheral = Peripheral()
        self.__stack = Stack()
        self.__branch = Branch()
        self.__parser = Parser(input)
        self.__pc = Assembler()
        self.__register = Register()
        self.__memory = Memory()
        self.__flag = Flag()
        self.__input = input
        self.inst = {}
        self.__inst_set()

        self.__rt = 0
        self.__cp = None

    def __inst_set(self):
        for inst in [
            self.__arithmetic,
            self.__branch,
            self.__data,
            self.__logical,
            self.__peripheral,
            self.__stack
        ]:
            self.inst.update(inst.get_inst())

    @property
    def input(self):
        return self.__input
    
    def execute(self):

        result = self.__parser.parse()

        if isinstance(result, Message):
            self.__cp = "parse"
            return result
        
        result = self.__pc.pass2()
        if isinstance(result, Message):
            self.__cp = "assemble/pass2"
            return result
        
        stack = self.__pc.get_stack()
        
        while True:

            if self.__rt > RUNTIME:
                self.__cp = "runtime"
                return Message("Runtime exceeded")

            try: # Handle No Return cases
                pc = self.__register['PC']
                inst , *code = stack[pc]
                info(f"{pc} {inst} {code}")
            
            except KeyError:
                self.__cp = "infinite_loop"
                return Message('Infinite Loop Detected. No return instruction found!')
            
            else:
                inst , *code = stack[pc]

                if inst == 'HLT':
                    break

                self.inst[inst]( *code )

                if isinstance(self.inst[inst].__self__, Branch):
                    self.__rt += 1
                    info(f"{pc} {inst} {code}")
                    continue

                else:
                    inr = INSTRUCTION[inst]['byte']
                    self.__register['PC'] = operate(self.__register['PC'], inr, bit=4)                
                self.__rt += 1
            
            info(f"{pc} {inst} {code}")
        
        self.__rt = 0
        return 0

    def as_dict(self) -> dict:
        result = self.execute()
        if isinstance(result, Message):
            return {
                "success": False,
                "checkpoint": f"execute/{self.__cp}",
                "error": result.as_dict()
            }
        return {
            "success": True,
            "checkpoint": "execute",
            "newState": {
                "registers": self.__register.get_all(),
                "flags": self.__flag.get_all(),
                "memory": self.__memory.get_all()
            }
        }

__all__ = [
    "Processor","Memory","Register","Flag","Message", "Assembler","stack"
]