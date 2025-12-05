class Simulator:
    def __init__(self):
        self.__memory_address = {hex(i)[2:].upper() + 'H':'0' for i in range(32768,40960)}
        self.__port = {}
        for i in range(256):
            if len(hex(i)[2:]) == 1 :self.__port['0' + hex(i)[2:].upper() + 'H'] = '0'
            else: self.__port[hex(i)[2:].upper() + 'H'] = '0'
        self.__registers = {'A':'0','B':'0','C':'0','D':'0','E':'0','F':'0','H':'0','L':'0','M':None}
        self.__flags = {'S':0,'Z':0,'AC':0,'P':0,'C':0}
        self.__op_code = {
            'MOV':self.__mov,
            'MVI':self.__mvi,
            'LXI':self.__lxi,
            'LDA':self.__lda,
            'STA':self.__sta,
            'LDAX':self.__ldax,
            'STAX':self.__stax,
            'LHLD':self.__lhld,
            'SHLD':self.__shld,
            'XCHG':self.__xchg,
            'IN':self.__in,
            'OUT':self.__out,
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
            'RRC':self.__rrc,
            'RAR':self.__rar,
            'RLC':self.__rlc,
            'RAL':self.__ral,
            'ANI':self.__ani,
            'XRI':self.__xri,
            'ORI':self.__ori,
            'ANA':self.__ana,
            'ORA':self.__ora,
            'XRA':self.__xra,
            'CMA':self.__cma,
            'CPI':self.__cpi,
            'CMC':self.__cmc,
            'STC':self.__stc
            
        }

        self.__param_rule = {
            'MOV':(2,1,1),
            'MVI':(2,1,3),
            'LXI':(2,1,5),
            'LDA':(1,5),
            'STA':(1,5),
            'LDAX':(1,1),
            'STAX':(1,1),
            'LHLD':(1,5),
            'SHLD':(1,5),
            'XCHG':(0,0),
            'IN':(1,3),
            'OUT':(1,3),
            'ADD':(1,1),
            'ADI':(1,3),
            'ADC':(1,1),
            'SUB':(1,1),
            'SUI':(1,3),
            'SBB':(1,1),
            'SBI':(1,3),
            'INR':(1,1),
            'DCR':(1,1),
            'INX':(1,1),
            'DCX':(1,1),
            'DAD':(1,1),
            'DAA':None,
            'RRC':(0,0),
            'RAR':(0,0),
            'RLC':(0,0),
            'RAL':(0,0),
            'ANI':(1,3),
            'XRI':(1,3),
            'ORI':(1,3),
            'ANA':(1,1),
            'ORA':(1,1),
            'XRA':(1,1),
            'CMA':(0,0),
            'CPI':(1,3),
            'CMC':(0,0),
            'STC':(0,0)
        }
        
    def check_param(self,inst:str,arg:str):
        prompt = arg.upper().replace(' ', '').split(',')
        check_list = self.param()

        if check_list[inst][0] == 0:
            if len(prompt[0]) >= 1: return 'SyntaxError'

        elif check_list[inst][0] == 1:

            if len(prompt[0]) != check_list[inst][1]: return 'SyntaxError'
            elif len(prompt[0]) == 0: return 'TypeError'
            elif len(prompt[0]) == 1 and prompt[0] not in self.show_register().keys(): return 'RegisterError'
            elif len(prompt[0]) == 5 and prompt[0] not in self.show_memory().keys(): return 'MemoryError'
            elif len(prompt[0]) == 3 and prompt[0] not in self.show_port().keys(): return 'DataError'
            else: return prompt

        else:
            if arg.find(',') == -1: return 'CommaError' 
            elif any([len(prompt[0]) != check_list[inst][1],
                  len(prompt[1]) != check_list[inst][2]]): return 'SyntaxError'
            elif len(prompt[0]) == 0 or len(prompt[1]) == 0: return 'TypeError'
            else:
                if any([len(prompt[0]) == 1  and prompt[0] == 'M' and self.check_pointer(prompt[0]),
                        len(prompt[1]) == 1 and prompt[1] == 'M' and self.check_pointer(prompt[0])]
                ): return 'PointerError'

                if any(
                    [len(prompt[0]) == 1 and prompt[0] not in self.show_register().keys(),
                     len(prompt[1]) == 1 and prompt[1] not in self.show_register().keys()]
                ): return 'RegisterError'
                elif any(
                    [len(prompt[0]) == 5 and prompt[0] not in self.show_memory().keys(),
                     len(prompt[1]) == 5 and prompt[1] not in self.show_memory().keys()]
                ): return 'MemoryError'
                elif len(prompt[1]) == 3 and prompt[1] not in self.show_port().keys(): return 'DataError'
                else: return prompt
    
    def op_code(self,code:str):
        return self.__op_code[code]
    
    def param(self):return self.__param_rule

    def show(self,exmin:str,address:str):
        if exmin == 'M': return self.__memory_address[address]
        
        elif exmin == 'R': return self.__registers[address]

        elif exmin == 'F': return self.__flags[address]

        elif exmin == 'P': return self.__port[address]
        
        else: return False
    
    def show_memory(self):
        return self.__memory_address

    def show_register(self):
        return self.__registers
    
    def show_flag(self):
        return self.__flags
    
    def show_port(self):
        return self.__port
    
    def show_op_code(self):
        return [i for i in self.__op_code]

    def check_pointer(self,rp:str) -> bool:
        if rp == 'M': rp = 'H'
        if len(self.__rp(rp)) != 5 and self.__rp(rp) in self.__port.keys(): return True
        else: return False

    def __check_flag(self,flag):
        if flag == 'C':
            if len(self.__registers['A']) > 3:
                self.__flags['C'] = 1
                self.__registers['A'] = self.__registers['A'][1:]
            
    def __filter(self,arg:str, conversion:int = 16):
        return int(arg.replace('H',''),conversion)

    def __encode(self,arg:int | bool, flag:str = 'hex'):
        if flag == 'bin':
            return bin(arg)
        elif flag == 'bool':
            return int(arg)
        elif flag == 'hex':
            return hex(arg)[2:].upper() + 'H'

    def __rp(self,rp:str = 'H') -> str:
        if rp == 'B': return self.__registers['B'] + self.__registers['C'] + 'H'
        elif rp == 'D': return  self.__registers['D'] + self.__registers['E'] + 'H'
        else: return self.__registers['H'] + self.__registers['L'] + 'H'

    def __mov(self,rd:str,rs:str):
        if rd == 'M':
            self.__memory_address[self.__rp()] =  self.__registers[rs]
        elif rs == 'M':
            self.__registers[rd] = self.__memory_address[self.__rp()]
        else:
            self.__registers[rd] = self.__registers[rs]

    def __mvi(self,r:str,data:str):
        if r == 'M':
            self.__memory_address[self.__rp()] =  data
        else:
            self.__registers[r] = data

    def __lxi(self,rp:str,data:str):
        if rp == 'B':
            self.__registers[rp] = data[:2]
            self.__registers['C'] = data[2:-1]
        
        elif rp == 'D':
            self.__registers[rp] = data[:2]
            self.__registers['E'] = data[2:-1]
        
        elif rp == 'H':
            self.__registers[rp] = data[:2]
            self.__registers['L'] = data[2:-1]

    def __lda(self,ma:str):
        self.__registers['A'] =  self.__memory_address[ma]
    
    def __sta(self, ma:str):
        self.__memory_address[ma] = self.__registers['A']    

    def __ldax(self,rp:str):
        if rp == 'B':
            self.__registers['A'] = self.__memory_address[self.__rp('B')]
        elif rp == 'D':
            self.__registers['A'] = self.__memory_address[self.__rp('D')]
        else:
            self.__registers['A'] = self.__memory_address[self.__rp()]
    
    def __stax(self,rp:str):
        if rp == 'B':
            self.__memory_address[self.__rp('B')] = self.__registers['A']
        elif rp == 'D':
            self.__memory_address[self.__rp('D')] = self.__registers['A']
        else:
            self.__memory_address[self.__rp()] = self.__registers['A']

    def __lhld(self,ma:str):
        self.__registers['L'] = self.__memory_address[ma]
        self.__registers['H'] = self.__memory_address[str(int(ma[:-1]) + 1) + 'H']

    def __shld(self,ma:str):
        self.__memory_address[ma] = self.__registers['L'] 
        self.__memory_address[str(int(ma[:-1]) + 1) + 'H'] = self.__registers['H']
    
    def __xchg(self):
        self.__registers['D'],self.__registers['H'] = self.__registers['H'],self.__registers['D']
        self.__registers['E'],self.__registers['L'] = self.__registers['L'],self.__registers['E']
    
    def __in(self,port:str):
        self.__registers['A'] = port
    
    def __out(self,port:str):
        self.__port[port] = self.__registers['A']
    
    def __add(self,r:str):
        if r == 'M':
            self.__registers['A'] = self.__encode( self.__filter(self.__registers['A']) +  self.__filter(self.__memory_address[self.__rp()]) )
        else: 
            self.__registers['A'] = self.__encode( self.__filter(self.__registers['A']) +  self.__filter(self.__registers[r]) )
        self.__check_flag('C')

    def __adc(self,r:str):
        if r == 'M':
            self.__registers['A'] = self.__encode( self.__filter(self.__registers['A']) +  self.__filter(self.__memory_address[self.__rp()]) + self.__flags['C'] )
        else:
            self.__registers['A'] = self.__encode( self.__filter(self.__registers['A']) + self.__filter(self.__registers[r]) + self.__flags['C'] )
        self.__check_flag('C')

    def __adi(self,data:str):
        self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) +  self.__filter(data))
        self.__check_flag('C')
    
    def __dad(self,rp:str):
        self.__memory_address[self.__rp()] = self.__encode(self.__filter(self.__memory_address[self.__rp()]) +  self.__filter(self.__memory_address[self.__rp(rp)])) 

    def __sub(self,r:str):
        if r == 'M':
            self.__registers['A'] = self.__encode( abs(self.__filter(self.__registers['A']) -  self.__filter(self.__memory_address[self.__rp()])) )
        else:
            self.__registers['A'] = self.__encode( abs(self.__filter(self.__registers['A']) -  self.__filter(self.__registers[r])) )
    
    def __sbb(self,r:str):
        if r == 'M':
            self.__registers['A'] = self.__encode( self.__filter(self.__registers['A']) - ( self.__filter(self.__memory_address[self.__rp()]) + self.__flags['C'] ) )
        else:
            self.__registers['A'] = self.__encode( self.__filter(self.__registers['A']) - ( self.__filter(self.__registers[r]) + self.__flags['C'] ) )
    
    def __sui(self,data:str):
        self.__registers['A'] = self.__encode(abs(self.__filter(self.__registers['A']) -  self.__filter(data)))
    
    def __sbi(self,data:str):
        rawDat = self.__filter(data)
        idat = ((~rawDat + 1) & ((1 << len( bin(rawDat)[2:]) ) - 1)) #2's complement
        self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) - ( idat + self.__flags['C'] ))
    
    def __inr(self,r:str):
        if r == 'M':
            self.__lxi('H',self.__encode(self.__filter(self.__rp().replace('H','')) + 1)) 
        else:
            self.__registers[r] = self.__encode( self.__filter(self.__registers[r]) + 1 ) 
    
    def __inx(self,rp:str):
        self.__memory_address[self.__rp(rp)] = self.__encode(self.__filter(self.__memory_address[self.__rp(rp)]) + 1) 
    
    def __dcx(self,rp:str):
        self.__memory_address[self.__rp(rp)] = self.__encode(self.__filter( self.__memory_address[self.__rp(rp)] ) - 1 ) 
    
    def __dcr(self,r:str):
        if r == 'M':
            self.__lxi('H',self.__encode(self.__filter(self.__rp().replace('H','')) - 1)) 
        else:
            self.__registers[r] = self.__encode( self.__filter(self.__registers[r]) - 1 ) 
            
    def __rrc(self):
        accumulator_value = bin(self.__filter(self.__registers['A']))[2:].zfill(8)
        self.__flags['C'] = int(accumulator_value[-1])
        rotated_value = accumulator_value[-1] + accumulator_value[:-1]
        self.__registers['A'] = self.__encode(int(rotated_value,2))
        
    def __rar(self):
        accumulator_value = bin(self.__filter(self.__registers['A']))[2:].zfill(8)
        rotated_value = str(self.__flags['C']) + accumulator_value[:-1]
        self.__flags['C'] = int(accumulator_value[-1])
        self.__registers['A'] = self.__encode(int(rotated_value,2))
    
    def __rlc(self):
        accumulator_value = self.__encode(self.__filter(self.__registers['A']),'bin')[2:].zfill(8)
        rotated_value = accumulator_value[1:] + accumulator_value[0]
        self.__flags['C'] = int(accumulator_value[0])
        self.__registers['A'] = self.__encode(int(rotated_value,2))
        
    def __ral(self):
        accumulator_value = self.__encode(self.__filter(self.__registers['A']),'bin')[2:].zfill(8)
        rotated_value = accumulator_value[1:] + str(self.__flags['C'])
        self.__flags['C'] = self.__filter(accumulator_value[0],2)
        self.__registers['A'] = self.__encode(self.__filter(rotated_value,2))
        
    def __ani(self,data:str):
        self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) & self.__filter(data)) 
        self.__flags['C'] , self.__flags['AC'] = 0, 1
        
    def __xri(self,data:str):
        self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) ^ self.__filter(data))
        self.__flags['C'] , self.__flags['AC'] = 0, 0
        
    def __ori(self,data:str):
        self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) | self.__filter(data))
        self.__flags['C'] , self.__flags['AC'] = 0, 0

    def __ana(self, r:str):   
        if r == 'M':
            self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) & self.__filter(self.__memory_address[self.__rp()]))
        else:
            self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) & self.__filter(self.__registers[r]))
        self.__registers['AC'] , self.__registers['C'] = 1, 0
        
    def __ora(self, r:str):   
        if r == 'M':
            self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) | self.__filter(self.__memory_address[self.__rp()]))
        else:
            self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) | self.__filter(self.__registers[r]))
        self.__registers['AC'] , self.__registers['C'] = 0, 0  
        
    def __xra(self, r:str):   
        if r == 'M':
            self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) ^ self.__filter(self.__memory_address[self.__rp()]))
        else:
            self.__registers['A'] = self.__encode(self.__filter(self.__registers['A']) ^ self.__filter(self.__registers[r]))
        self.__registers['AC'] , self.__registers['C'] = 0, 0         
        
    def __cma(self):
        self.__registers['A'] = self.__encode(~self.__filter(self.__registers['A']) & 0xFF)
    
    def __cpi(self, data:str):
        a_value = self.__filter(self.__registers['A'])
        data_value = self.__filter(data)
        if a_value < data_value:
            self.__flags['C'], self.__flags['Z'] = 1, 0
        elif a_value == data_value:
            self.__flags['C'], self.__flags['Z'] = 0, 1
        else:
            self.__flags['C'], self.__flags['Z'] = 0, 0
    
    def __cmc(self):
        self.__flags['C'] = self.__encode(not self.__flags['C'], 'bool')

    def __stc(self):
        self.__flags['C'] = 1