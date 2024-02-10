from ._utils import Tool
class Data:

    def __init__(self,token:dict):
        self.__memory_address:dict = token['memory']
        self.__register:dict = token['register']

    def __mov(self,arg:list):
        rd,rs = arg
        if rd == 'M':
            self.__memory_address[Tool.rp()] =  self.__register[rs]
        elif rs == 'M':
            self.__register[rd] = self.__memory_address[Tool.rp()]
        else:
            self.__register[rd] = self.__register[rs]

    def __mvi(self,arg:list):
        r,data = arg
        if r == 'M':
            self.__memory_address[Tool.rp()] =  data
        else:
            self.__register[r] = data

    def __lxi(self,arg:list):
        rp,data = arg
        if rp == 'B':
            self.__register[rp] = data[:2]
            self.__register['C'] = data[2:-1]
        
        elif rp == 'D':
            self.__register[rp] = data[:2]
            self.__register['E'] = data[2:-1]
        
        elif rp == 'H':
            self.__register[rp] = data[:2]
            self.__register['L'] = data[2:-1]

    def __lda(self,arg:list):
        ma = arg[0]
        self.__register['A'] =  self.__memory_address[ma]
    
    def __sta(self, arg:list):
        ma = arg[0]
        self.__memory_address[ma] = self.__register['A']    

    def __ldax(self,arg:list):
        rp = arg[0]
        if rp == 'B':
            self.__register['A'] = self.__memory_address[Tool.rp('B')]
        elif rp == 'D':
            self.__register['A'] = self.__memory_address[Tool.rp('D')]
        else:
            self.__register['A'] = self.__memory_address[Tool.rp()]
    
    def __stax(self,arg:list):
        rp = arg[0]
        if rp == 'B':
            self.__memory_address[Tool.rp('B')] = self.__register['A']
        elif rp == 'D':
            self.__memory_address[Tool.rp('D')] = self.__register['A']
        else:
            self.__memory_address[Tool.rp()] = self.__register['A']

    def __lhld(self,arg:list):
        ma = arg[0]
        self.__register['L'] = self.__memory_address[ma]
        self.__register['H'] = self.__memory_address[str(int(ma[:-1]) + 1) + 'H']

    def __shld(self,arg:list):
        ma = arg[0]
        self.__memory_address[ma] = self.__register['L'] 
        self.__memory_address[str(int(ma[:-1]) + 1) + 'H'] = self.__register['H']
    
    def __xchg(self):
        self.__register['D'],self.__register['H'] = self.__register['H'],self.__register['D']
        self.__register['E'],self.__register['L'] = self.__register['L'],self.__register['E']

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