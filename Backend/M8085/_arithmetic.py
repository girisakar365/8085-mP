from ._base import Instruction
from ._utils import decode, operate
from ._memory import *

class Arithmetic(Instruction):

    def __init__(self):
        self._memory:Memory = Memory()
        self._register:Register = Register()
        self._flag:Flag = Flag()

    def __add(self,r:str):
        if r == 'M':
            op2 = self._memory[decode_rp()]
        else:
            op2 = self._register[r]

        result = operate(self._register['A'], op2)
        self._register['A'] = encode(decode(result) & 0xFF)

        check_carry(result)
        check_aux_carry(self._register['A'], op2)
        check_sign(self._register['A'])
        check_parity(self._register['A']) 
        check_zero(self._register['A']) 

    def __adc(self,r:str):
        if r == 'M':
            op2 = self._memory[decode_rp()]
        else:
            op2 = self._register[r]
        
        result = operate(self._register['A'], op2, flag=self._flag['C'])
        self._register['A'] = encode(decode(result) & 0xFF)

        check_carry(result)
        check_aux_carry(self._register['A'], op2)
        check_sign(self._register['A'])
        check_parity(self._register['A']) 
        check_zero(self._register['A'])                
        
    def __adi(self,data:str):
        result = operate(self._register['A'], data, flag=self._flag['C'])
        self._register['A'] = encode(decode(result) & 0xFF)

        check_carry(result)
        check_aux_carry(self._register['A'], data)
        check_sign(self._register['A'])
        check_parity(self._register['A']) 
        check_zero(self._register['A'])  
    
    def __dad(self,rp:str):
        result = operate(self._memory[decode_rp()], self._memory[decode_rp(rp)])
        self._memory[decode_rp()] = encode(decode(result) & 0xFFFF, bit=4)
        check_carry(result, bit=4)

    def __sub(self,r:str):

        if r == 'M':
            complement = ( (~decode(self._memory[decode_rp()]) + 1) & 0xFF ) # ~B + 1 = 2's complement; & 0xFF to keep it within 8 bits 

        else:
            complement = ( (~decode(self._register[r]) + 1) & 0xFF ) # ~B + 1 = 2's complement; & 0xFF to keep it within 8 bits

        result = operate(self._register['A'], encode(complement))
        self._register['A'] = encode(decode(result) & 0xFF)

        check_carry(result)
        check_aux_carry(self._register['A'], encode(complement))
        check_parity(self._register['A'])
        check_zero(self._register['A'])
        check_sign(self._register['A'])  

    def __sbb(self,r:str):

        if r == 'M':
            complement = ( (~decode(self._memory[decode_rp()]) + 1) & 0xFF ) # ~B + 1 = 2's complement; & 0xFF to keep it within 8 bits
        else:
            complement = ( (~decode(self._register[r]) + 1) & 0xFF ) # ~B + 1 = 2's complement; & 0xFF to keep it within 8 bits

        result = operate(self._register['A'], encode(complement), flag=self._flag['C'])
        self._register['A'] = encode(decode(result) & 0xFF)
        check_carry(result)
        check_aux_carry(self._register['A'], encode(complement))
        check_parity(self._register['A'])  
        check_zero(self._register['A'])  
        check_sign(self._register['A'])  

    def __sui(self,data:str):
        complement = ( (~decode(data) + 1) & 0xFF ) # ~B + 1 = 2's complement; & 0xFF to keep it within 8 bits
        result = operate(self._register['A'], encode(complement))
        self._register['A'] = encode(decode(result) & 0xFF)
        
        check_carry(result)
        check_aux_carry(self._register['A'], encode(complement))
        check_parity(self._register['A'])  
        check_zero(self._register['A'])  
        check_sign(self._register['A'])  
    
    def __sbi(self,data:str):
        operand = (decode(data) + self._flag['C']) & 0xFF
        complement = ( ~(operand) + 1 ) & 0xFF  # ~B + 1 = 2's complement; & 0xFF to keep it within 8 bits
        
        result = operate(self._register['A'], encode(complement))
        self._register['A'] = encode(decode(result) & 0xFF)

        check_carry(result)
        check_aux_carry(self._register['A'], encode(complement))
        check_parity(self._register['A'])
        check_zero(self._register['A']) 
        check_sign(self._register['A']) 

    def __inr(self,r:str):

        if r == 'M':
            result = operate(self._memory[decode_rp()], '01H') # Adding 0xFF is equivalent to subtracting 1
            masked = encode(decode(result) & 0xFF) # 8-bit masking
            encode_rp(masked)
            check_aux_carry(self._memory[decode_rp()], '01H')
        
        else:
            result = operate(self._register[r], '01H') # Adding 0xFF is equivalent to subtracting 1
            masked = encode(decode(result) & 0xFF) # 8-bit masking
            self._register[r] = masked
            check_aux_carry(self._register[r], '01H')
        
        check_parity(masked)
        check_zero(masked)
        check_sign(masked)
    
    def __inx(self,rp:str):
        value = operate(decode_rp(rp), 1, bit=4)
        encode_rp(value, rp=rp)
             
    def __dcx(self,rp:str):
        value = operate(self._memory[decode_rp(rp)], 'FFFFH', bit=4)
        encode_rp(value,rp=rp)

    def __dcr(self,r:str):

        if r == 'M':
            result = operate(self._memory[decode_rp()], 'FFH') # Adding 0xFF is equivalent to subtracting 1
            masked = encode(decode(result) & 0xFF) # 8-bit masking
            encode_rp(masked)
            check_aux_carry(self._memory[decode_rp()], 'FFH')
        
        else:
            result = operate(self._register[r], 'FFH') # Adding 0xFF is equivalent to subtracting 1
            masked = encode(decode(result) & 0xFF) # 8-bit masking
            self._register[r] = masked
            check_aux_carry(self._register[r], 'FFH')
        
        check_parity(masked)
        check_zero(masked) 
        check_sign(masked)
        
    def __daa(self):
        num = decode(self._register['A'])

        if (num & 0x0F) > 9 or self._flag['AC'] == 1:
            num += 0x06
            self._flag['AC'] = 1

        # Upper nibble adjustment
        if (num >> 4) > 9 or self._flag['CY'] == 1:
            num += 0x60
            self._flag['CY'] = 1
        
        self._register['A'] = encode(num & 0xFF)
        check_sign(self._register['A'])
        check_parity(self._register['A'])
        check_zero(self._register['A'])

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
            'DAA':self.__daa,
            'INR':self.__inr,
            'INX':self.__inx,
            'DCR':self.__dcr,
            'DCX':self.__dcx,
        }    
