from ._utils import encode, decode, Tool
class Arithmetic:

    def __init__(self,token:dict):
        self.__memory_address:dict = token['memory']
        self.__register:dict = token['register']
        self.__flag:dict = token['flag']

    def __add(self,arg:list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = encode( decode(self.__register['A']) +  decode(self.__memory_address[Tool.rp()]) )
        else: 
            self.__register['A'] = encode( decode(self.__register['A']) +  decode(self.__register[r]) )

    def __adc(self,arg:list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = encode( decode(self.__register['A']) +  decode(self.__memory_address[Tool.rp()]) + self.__flags['C'] )
        else:
            self.__register['A'] = encode( decode(self.__register['A']) + decode(self.__register[r]) + self.__flags['C'] )

    def __adi(self,arg:list):
        self.__register['A'] = encode(decode(self.__register['A']) +  decode(arg[0]))
    
    def __dad(self,arg:list):
        rp = arg[0]
        self.__memory_address[Tool.rp()] = encode(decode(self.__memory_address[Tool.rp()]) +  decode(self.__memory_address[Tool.rp(rp)])) 

    def __sub(self,arg:list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = encode( abs(decode(self.__register['A']) -  decode(self.__memory_address[Tool.rp()])) )
        else:
            self.__register['A'] = encode( abs(decode(self.__register['A']) -  decode(self.__register[r])) )
    
    def __sbb(self,arg:list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = encode( decode(self.__register['A']) - ( decode(self.__memory_address[Tool.rp()]) + self.__flags['C'] ) )
        else:
            self.__register['A'] = encode( decode(self.__register['A']) - ( decode(self.__register[r]) + self.__flags['C'] ) )
    
    def __sui(self,arg:list):
        data = arg[0]
        self.__register['A'] = encode(abs(decode(self.__register['A']) -  decode(data)))
    
    def __sbi(self,arg:list):
        data = arg[0]
        rawDat = decode(data)
        idat = ((~rawDat + 1) & ((1 << len( bin(rawDat)[2:]) ) - 1)) #2's complement
        self.__register['A'] = encode(decode(self.__register['A']) - ( idat + self.__flags['C'] ))
    
    def __inr(self,arg:list):
        r = arg[0]
        if r == 'M':
            new = encode(decode(Tool.rp().replace('H','')) + 1)[:-1]
            self.__register['H']  = new[:2]
            self.__register['L']  = new[2:]

        else:
            self.__register[r] = encode( decode(self.__register[r]) + 1 ) 
    
    def __inx(self,arg:list):
        rp = arg[0]
        self.__memory_address[Tool.rp(rp)] = encode(decode(self.__memory_address[Tool.rp(rp)]) + 1) 
    
    def __dcx(self,arg:list):
        rp = arg[0]
        self.__memory_address[Tool.rp(rp)] = encode(decode( self.__memory_address[Tool.rp(rp)] ) - 1 ) 
    
    def __dcr(self,arg:list):
        r = arg[0]
        if r == 'M':
            new = encode(decode(Tool.rp().replace('H','')) - 1)[:-1]
            self.__register['H']  = new[:2]
            self.__register['L']  = new[2:]
         
        else:
            self.__register[r] = encode( decode(self.__register[r]) - 1 ) 

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