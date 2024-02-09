from _utils import encode, filter, get_token


class Stack:
    def __init__(self, token:dict):
        self.__memory_address:dict = token['memory']
        self.__register:dict = token['register']
        self.__flag:dict = token['flag']
        self.stack_dict = {}
    
    def add_ins(self, param: str):
        self.stack_dict[encode(filter(self.__register['PC']))] = param
        self.__register['PC'] += 1

    def get_stack(self):
        return self.stack_dict
    
    def __push(self,rp:str):
        self.__register['SP'] = encode(filter(self.__register['SP']) - 2)
        if rp == 'B':
            self.__memory_address[self.__register['SP']] = self.__register['B'] 
            self.__memory_address[encode(filter(self.__register['SP'])-1)] = self.__register['C']  
        elif rp == 'D':
            self.__memory_address[self.__register['SP']] = self.__register['D'] 
            self.__memory_address[encode(filter(self.__register['SP'])-1)] = self.__register['E'] 
        elif rp == 'H':
            self.__memory_address[self.__register['SP']] = self.__register['H'] 
            self.__memory_address[encode(filter(self.__register['SP'])-1)] = self.__register['L'] 
        
    def __pop(self,rp:str):
        if rp == 'B':
            self.__register['C'] = self.__memory_address[self.__register['SP']]
            self.__register['B'] = self.__memory_address[encode(filter(self.__register['SP']) + 1)]
            
        elif rp == 'D':
            self.__register['E'] = self.__memory_address[self.__register['SP']]
            self.__register['D'] = self.__memory_address[encode(filter(self.__register['SP']) + 1)]
            
        elif rp == 'H':
            self.__register['L'] = self.__memory_address[self.__register['SP']]
            self.__register['H'] = self.__memory_address[encode(filter(self.__register['SP']) + 1)]
        self.__register['SP'] = encode(filter(self.__register['SP']) - 2)   
    
    def __xthl(self):
        temp = self.__register['H']
        self.__register['H'] = self.__memory_address[self.__register['SP']]
        self.__memory_address[self.__register['SP']] = temp
        temp = self.__register['L']
        self.__register['L'] = self.__memory_address[encode(filter(self.__register['SP']) + 1)]
        self.__memory_address[encode(filter(self.__register['SP']) + 1)] = temp

    def __sphl(self):
        self.__register['SP'] = self.__register['H'][:-1] + self.__register['L']
    
    def __pchl(self):
        self.__register['PC'] = self.__register['H'][:-1] + self.__register['L']
            
    def get_inst(self):
        return{
            'PUSH' : self.__push,
            'POP' : self.__pop,
            'XTHL': self.__xthl,
            'SPHL': self.__sphl,
            'PCHL': self.__pchl       
        }
    def test(self):
        self.__register['H'] = '12H'
        self.__register['L'] = '34H'
        self.__register['SP'] = '2000H'
        self.__register['PC'] = '0010H'
        self.__memory_address['2000H'] = 'FFH'
        self.__memory_address['2001H'] = 'EEH'
        self.__pchl()
        print(self.__register['H'],self.__register['L'],self.__register['SP'],self.__memory_address['2000H'],self.__memory_address['2001H'] )

s1 = Stack(get_token())
s1.test()