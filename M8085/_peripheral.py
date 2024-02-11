class Peripheral:

    def __init__(self,token:dict):
        self.__port:dict = token['port']
        self.__register:dict = token['register']

    def __in(self, port:str):
        self.__register['A'] = port

    def __out(self, port: str):
        self.__port[port] = self.__register['A']

    def get_inst(self):
        return {
            'IN':self.__in,
            'OUT':self.__out,
        }