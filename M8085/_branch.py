class Branch:
    def __init__(self,token:dict):
        self.__flag:dict = token['flag']

    def __jmp(self, target_label:str):
        return target_label

    def __jc(self, target_label:str):
        return target_label if self.__flag['C'] else None

    def __jnc(self, target_label:str):
        return target_label if not self.__flag['C'] else None

    def __jz(self, target_label:str):
        return target_label if self.__flag['Z'] else None

    def __jnz(self, target_label:str):
        return target_label if not self.__flag['Z'] else None

    def __jpe(self, target_label:str):
        return target_label if self.__flag['P'] else None

    def __jpo(self, target_label:str):
        return target_label if not self.__flag['P'] else None

    def __jm(self, target_label:str):
        return target_label if self.__flag['S'] else None

    def __jp(self, target_label:str):
        return target_label if not self.__flag['S'] else None

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