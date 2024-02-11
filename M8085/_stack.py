from ._utils import encode,decode,Tool

class Stack:
    def __init__(self,token):
        self.__stack = token['stack']
        self.__register = token['register']
        Tool.TOKEN = token

    def push(self, rp:str):
        if rp == 'B':
            self.__stack[self.__register['SP']] = self.__register['B']  + self.__register['C']

        elif rp == 'D':
            self.__stack[self.__register['SP']] = self.__register['D']  + self.__register['E']

        elif rp == 'H':
            self.__stack[self.__register['SP']] = self.__register['H']  + self.__register['L']

        self.__register['SP'] = encode(decode(self.__register['SP'])-1)

    def pop(self,rp:str):
        self.__register['SP'] = encode(decode(self.__register['SP'])+1)
        if rp == 'B':
            self.__register['B'] = self.__register['SP'][:2] 
            self.__register['C'] = self.__register['SP'][2:]

        elif rp == 'D':
            self.__register['D'] = self.__register['SP'][:2] 
            self.__register['E'] = self.__register['SP'][2:]

        elif rp == 'H':
            self.__register['H'] = self.__register['SP'][:2] 
            self.__register['L'] = self.__register['SP'][2:]

        self.__register['SP'] = encode(decode(self.__register['SP'])+1)

    def __xthl(self):
        data = self.__register['H'] + self.__register['L']
        data, self.__stack['SP'] = self.__stack['SP'], data

        self.__register['H'] = data[:2]
        self.__register['L'] = data[2:]

    def __sphl(self):
        self.__register['SP'] = self.__register['H'] + self.__register['L']
    
    def __pchl(self):
        self.__register['PC'] = self.__register['H'] + self.__register['L']
    
    def get_inst(self):
        return {
            "PUSH": self.push,
            "POP": self.pop,
            "XTHL": self.__xthl,
            "SPHL": self.__sphl,
            "PCHL": self.__pchl,
        }

