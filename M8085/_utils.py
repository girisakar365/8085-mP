from pathlib import Path
import yaml
from .logs import setup_logger, warn
setup_logger()

PATH = Path(__file__).parent

with open(f"{PATH}/commands_property.yml", "r") as f:
    INSTRUCTION:dict = yaml.safe_load(f)

def decode(arg:str) -> int | None:
    arg = arg[:-1]  # Remove 'H' at the end
    try:
        return int(arg,16)
    except ValueError:
        warn(f"Invalid Address: {arg}")

def encode(arg:int, bit:int=2) -> str:

    addr = hex(arg)[2:].upper()

    if len(addr) < bit:
        return '0' * (bit - len(addr)) + addr + 'H'
    
    return addr + 'H'

def operate(op1: str | int, op2: str | int, flag: int = 0, bit: int = 2) -> str:
    if isinstance(op1, str):
        op1 = decode(op1)
    
    if isinstance(op2, str):
        op2 = decode(op2)

    return encode(op1 + op2 + flag, bit=bit)


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

    def __iter__(self):
        self.__str__()
        yield from self.general
    
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
