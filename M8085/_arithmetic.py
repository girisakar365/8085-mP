from _utils import encode ,filter
class Arithmetic:

    def __init__(self,token:dict):
        self.__memory_address:dict = token['memory']
        self.__register:dict = token['register']
        self.__flag:dict = token['flag']

    def __add(self,r:str):
        if r == 'M':
            self.__register['A'] = encode( filter(self.__register['A']) +  filter(self.__memory_address[self.__rp()]) )
        else: 
            self.__register['A'] = encode( filter(self.__register['A']) +  filter(self.__register[r]) )
        self.__check_flag('C')

    def __adc(self,r:str):
        if r == 'M':
            self.__register['A'] = encode( filter(self.__register['A']) +  filter(self.__memory_address[self.__rp()]) + self.__flag['C'] )
        else:
            self.__register['A'] = encode( filter(self.__register['A']) + filter(self.__register[r]) + self.__flag['C'] )
        self.__check_flag('C')

    def __adi(self,data:str):
        self.__register['A'] = encode(filter(self.__register['A']) +  filter(data))
        self.__check_flag('C')
    
    def __dad(self,rp:str):
        self.__memory_address[self.__rp()] = encode(filter(self.__memory_address[self.__rp()]) +  filter(self.__memory_address[self.__rp(rp)])) 

    def __sub(self,r:str):
        if r == 'M':
            self.__register['A'] = encode( abs(filter(self.__register['A']) -  filter(self.__memory_address[self.__rp()])) )
        else:
            self.__register['A'] = encode( abs(filter(self.__register['A']) -  filter(self.__register[r])) )
    
    def __sbb(self,r:str):
        if r == 'M':
            self.__register['A'] = encode( filter(self.__register['A']) - ( filter(self.__memory_address[self.__rp()]) + self.__flag['C'] ) )
        else:
            self.__register['A'] = encode( filter(self.__register['A']) - ( filter(self.__register[r]) + self.__flag['C'] ) )
    
    def __sui(self,data:str):
        self.__register['A'] = encode(abs(filter(self.__register['A']) -  filter(data)))
    
    def __sbi(self,data:str):
        rawDat = filter(data)
        idat = ((~rawDat + 1) & ((1 << len( bin(rawDat)[2:]) ) - 1)) #2's complement
        self.__register['A'] = encode(filter(self.__register['A']) - ( idat + self.__flag['C'] ))
    
    def __inr(self,r:str):
        if r == 'M':
            self.__lxi('H',encode(filter(self.__rp().replace('H','')) + 1)) 
        else:
            self.__register[r] = encode( filter(self.__register[r]) + 1 ) 
    
    def __inx(self,rp:str):
        self.__memory_address[self.__rp(rp)] = encode(filter(self.__memory_address[self.__rp(rp)]) + 1) 
    
    def __dcx(self,rp:str):
        self.__memory_address[self.__rp(rp)] = encode(filter( self.__memory_address[self.__rp(rp)] ) - 1 ) 
    
    def __dcr(self,r:str):
        if r == 'M':
            self.__lxi('H',encode(filter(self.__rp().replace('H','')) - 1)) 
        else:
            self.__register[r] = encode(filter(self.__register[r]) - 1 ) 

    def get_inst(self):
        return {
            'ADD':self.__add,
            'ADI':self.__adi,
            'ADC':self.__adc,
            'SUB':self.__sub,
            'SUI':self.__sui,
            'SBB':self.__sbb,
            'SBI':self.__sbi,
            'INR':self.__inr,
            'DCR':self.__dcr,
            'INX':self.__inx,
            'DCX':self.__dcx,
            'DAD':self.__dad,
            'DAA':None,
            'INR':self.__inr,
            'INX':self.__inx,
            'DCR':self.__dcr,
            'DCX':self.__dcx,
        }