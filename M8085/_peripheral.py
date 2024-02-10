class Peripheral:

    def __init__(self,token:dict):
        self.__port:dict = token['port']
        self.__register:dict = token['register']

    def __in(self, port: list):
        self.__register['A'] = port[0]

    def __out(self, port: list):
        self.__port[port[0]] = self.__register['A']

    def get_inst(self):
        return {
            'IN':self.__in,
            'OUT':self.__out,
        }