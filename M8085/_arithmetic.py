class Arithmetic:

    def __init__(self,token:dict):
        self.__memory_address:dict = token['memory']
        self.__register:dict = token['register']
        self.__flag:dict = token['flag']

    def __add(self,arg:str):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = self.__encode( self.__filter(self.__register['A']) +  self.__filter(self.__memory_address[self.__rp()]) )
        else: 
            self.__register['A'] = self.__encode( self.__filter(self.__register['A']) +  self.__filter(self.__register[r]) )
        self.__check_flag('C')

    def __adc(self, arg: list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = self.__encode(self.__filter(self.__register['A']) + self.__filter(self.__memory_address[self.__rp()]) + self.__flag['C'])
        else:
            self.__register['A'] = self.__encode(self.__filter(self.__register['A']) + self.__filter(self.__register[r]) + self.__flag['C'])
        self.__check_flag('C')

    def __sub(self, arg: list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = self.__encode(abs(self.__filter(self.__register['A']) - self.__filter(self.__memory_address[self.__rp()])))
        else:
            self.__register['A'] = self.__encode(abs(self.__filter(self.__register['A']) - self.__filter(self.__register[r])))

    def __sbb(self, arg: list):
        r = arg[0]
        if r == 'M':
            self.__register['A'] = self.__encode(self.__filter(self.__register['A']) - (self.__filter(self.__memory_address[self.__rp()]) + self.__flag['C']))
        else:
            self.__register['A'] = self.__encode(self.__filter(self.__register['A']) - (self.__filter(self.__register[r]) + self.__flag['C']))

    def __sui(self, arg: list):
        self.__register['A'] = self.__encode(abs(self.__filter(self.__register['A']) - self.__filter(arg[0])))

    def __sbi(self, arg: list):
        rawDat = self.__filter(arg[0])
        idat = ((~rawDat + 1) & ((1 << len(bin(rawDat)[2:])) - 1))  # 2's complement
        self.__register['A'] = self.__encode(self.__filter(self.__register['A']) - (idat + self.__flag['C']))

    def __dcr(self, arg: list):
        r = arg[0]
        if r == 'M':
            self.__lxi('H', self.__encode(self.__filter(self.__rp().replace('H', '')) - 1))
        else:
            self.__register[r] = self.__encode(self.__filter(self.__register[r]) - 1)


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