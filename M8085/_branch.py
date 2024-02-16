from _utils import encode , decode , Tool

class Branch:
    def __init__(self,token:dict):
        Tool.TOKEN = token
        self.__memory_address:dict = token['memory']
        self.__register:dict = token['register']
        self.__flag:dict = token['flag']
        
    def __jmp(self,kywrd:str):
        return Tool.INST_ADDRESS[kywrd] 
    
    def __jc(self, kywrd:str):    
        return Tool.INST_ADDRESS[kywrd] if self.__flag['C'] else 0
        
    def __jnc(self, kywrd:str):
        return Tool.INST_ADDRESS[kywrd] if not self.__flag['C'] else 0
    
    def __jz(self, kywrd:str):
        return Tool.INST_ADDRESS[kywrd] if self.__flag['Z'] else 0
        
    def __jnz(self, kywrd:str):
        return Tool.INST_ADDRESS[kywrd] if not self.__flag['Z'] else 0
    
    def __jpe(self, kywrd:str):
        return Tool.INST_ADDRESS[kywrd] if self.__flag['P'] else 0
        
    def __jpo(self, kywrd:str):
        return Tool.INST_ADDRESS[kywrd] if not self.__flag['P'] else 0
    
    def __jm(self, kywrd:str):
        return Tool.INST_ADDRESS[kywrd] if self.__flag['S'] else 0
        
    def __jp(self, kywrd:str):
        return Tool.INST_ADDRESS[kywrd] if not self.__flag['S'] else 0
    
    def get_inst(self):
        return {
            'JMP':self.__jmp,
            'JC':self.__jc,
            'JNC':self.__jnc,
            'JZ':self.__jz,
            'JNZ':self.__jnz,
            'JPE':self.__jpe,
            'JPO':self.__jpo,
            'JM':self.__jm,
            'JP':self.__jp
        }
            


