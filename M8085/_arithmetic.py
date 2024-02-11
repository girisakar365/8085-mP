from ._utils import encode, decode, Tool
class Arithmetic:

    def __init__(self,token:dict):
        Tool.TOKEN = token
        self.__memory_address:dict = token['memory']
        self.__register:dict = token['register']
        self.__flag:dict = token['flag']

    def __add(self,r:str):
        if r == 'M':
            self.__register['A'] = encode( decode(self.__register['A']) +  decode(self.__memory_address[Tool.rp()]) )
        else: 
            self.__register['A'] = encode( decode(self.__register['A']) +  decode(self.__register[r]) )
        
        if len(self.__register['A']) > 3:
            self.__flag['C'] = 1
            self.__register['A'] = self.__register['A'][1:]
        
        Tool.check_parity(self.__register['A']) 
        Tool.check_zero(self.__register['A']) 
        Tool.check_sign(self.__register['A']) 

    def __adc(self,r:str):
        if r == 'M':
            self.__register['A'] = encode( decode(self.__register['A']) +  decode(self.__memory_address[Tool.rp()]) + self.__flags['C'] )
        else:
            self.__register['A'] = encode( decode(self.__register['A']) + decode(self.__register[r]) + self.__flags['C'] )
        
        if len(self.__register['A']) > 3:
            self.__flag['C'] = 1
            self.__register['A'] = self.__register['A'][1:]

        Tool.check_parity(self.__register['A'])
        Tool.check_zero(self.__register['A'])         
        Tool.check_sign(self.__register['A'])         
        
    def __adi(self,arg:list):
        self.__register['A'] = encode(decode(self.__register['A']) +  decode(arg[0]))

        if len(self.__register['A']) > 3:
            self.__flag['C'] = 1
            self.__register['A'] = self.__register['A'][1:]
        
        Tool.check_parity(self.__register['A'])  
        Tool.check_zero(self.__register['A']) 
        Tool.check_sign(self.__register['A']) 
    
    def __dad(self,rp:str):
        self.__memory_address[Tool.rp()] = encode(decode(self.__memory_address[Tool.rp()]) +  decode(self.__memory_address[Tool.rp(rp)]))

        if len(self.__memory_address[Tool.rp()]) > 3:
            self.__flag['C'] = 1
            self.__memory_address[Tool.rp()] = self.__memory_address[Tool.rp()][1:]
        
        Tool.check_parity(self.__memory_address[Tool.rp()]) 
        Tool.check_zero(self.__memory_address[Tool.rp()])  
        Tool.check_sign(self.__memory_address[Tool.rp()])  

    def __sub(self,r:str):

        if r == 'M':
            if decode(self.__memory_address[Tool.rp()]) > decode(self.__register['A']):
                self.__flag['C'] = 1  
            self.__register['A'] = encode( decode(self.__register['A'] -  decode(self.__memory_address[Tool.rp()])) )
        else:
            if decode(self.__register[r]) > decode(self.__register['A']):
                self.__flag['C'] = 1
            self.__register['A'] = encode( decode(self.__register['A']) -  decode(self.__register[r]) )
        
            Tool.check_parity(self.__register['A'])  
            Tool.check_zero(self.__register['A'])  
            Tool.check_sign(self.__register['A'])  

    def __sbb(self,r:str):

        if r == 'M':
            if decode(self.__memory_address[Tool.rp()]) + self.__flags['C'] > decode(self.__register['A']):
                self.__flag['C'] = 1
            self.__register['A'] = encode( decode(self.__register['A']) - ( decode(self.__memory_address[Tool.rp()]) + self.__flags['C'] ) )
        else:
            if decode(self.__register[r]) + self.__flags['C'] > decode(self.__register['A']):
                self.__flag['C'] = 1
            self.__register['A'] = encode( decode(self.__register['A']) - ( decode(self.__register[r]) + self.__flags['C'] ) )
        
            Tool.check_parity(self.__register['A'])  
            Tool.check_zero(self.__register['A'])  
            Tool.check_sign(self.__register['A'])  

    def __sui(self,data:str):
        if decode(data) > decode(self.__register['A']):
            self.__flag['C'] = 1
        self.__register['A'] = encode(decode(self.__register['A']) -  decode(data))

        Tool.check_parity(self.__register['A'])  
        Tool.check_zero(self.__register['A'])  
        Tool.check_sign(self.__register['A'])  
    
    def __sbi(self,data:str):
        rawDat = decode(data)
        idat = ((~rawDat + 1) & ((1 << len( bin(rawDat)[2:]) ) - 1)) #2's complement
        if idat + self.__flags['C'] > decode(self.__register['A']):
            self.__flag['C'] = 1
        self.__register['A'] = encode(decode(self.__register['A']) - ( idat + self.__flags['C'] ))

        Tool.check_parity(self.__register['A'])
        Tool.check_zero(self.__register['A']) 
        Tool.check_sign(self.__register['A']) 

    def __inr(self,r:str):

        if r == 'M':
            new = encode(decode(Tool.rp().replace('H','')) + 1)[:-1]
            self.__register['H']  = new[:2]
            self.__register['L']  = new[2:]
            Tool.check_parity(new)
            Tool.check_zero(new)
            Tool.check_sign(new)

        else:
            self.__register[r] = encode( decode(self.__register[r]) + 1 )
            Tool.check_parity(self.__register[r])
            Tool.check_zero(self.__register[r])
            Tool.check_sign(self.__register[r])
    
    def __inx(self,rp:str):
        self.__memory_address[Tool.rp(rp)] = encode(decode(self.__memory_address[Tool.rp(rp)]) + 1)
             
    def __dcx(self,rp:str):
        self.__memory_address[Tool.rp(rp)] = encode(decode( self.__memory_address[Tool.rp(rp)] ) - 1 ) 
    
    def __dcr(self,r:str):

        if r == 'M':
            new = encode(decode(Tool.rp().replace('H','')) - 1)[:-1]
            self.__register['H']  = new[:2]
            self.__register['L']  = new[2:]
            Tool.check_parity(new)
            Tool.check_zero(new)
            Tool.check_sign(new)
        else:
            self.__register[r] = encode( decode(self.__register[r]) - 1 )
            Tool.check_parity(self.__register[r])
            Tool.check_zero(self.__register[r]) 
            Tool.check_sign(self.__register[r]) 

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