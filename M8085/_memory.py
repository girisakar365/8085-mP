from ._utils import encode, decode, operate, INSTRUCTION

_MEMORY = {}
_STACK = {}
_REGISTER = {
    'A':'00H','B':'00H','C':'00H','D':'00H','E':'00H','H':'00H','L':'00H','M':'00H',
    'PC':'0000H','SP':'0000H'
}
_FLAG = {'S':0,'Z':0,'AC':0,'P':0,'C':0}

class Memory:

    def __getitem__(self,address):
        if address in _MEMORY: return _MEMORY[address]
        else:
            addr = decode(address)  # Validate address
            if isinstance(addr, int): return '00H'
            else: return addr

    def __setitem__(self,address, data):
        if data == '00H':
            if address in _MEMORY: _MEMORY.pop(address, None)
        else:
            _MEMORY[address] = data

    def write(self,address, data):
        if data == '00H':
            if address in _MEMORY: _MEMORY.pop(address, None)
        else:
            _MEMORY[address] = data

    def read(self,address):
        if address in _MEMORY: return _MEMORY[address]
    
    def get_used_addresses(self):
        return _MEMORY.keys()
    
    def reset(self):
        _MEMORY.clear()
    

class Register:

    def __getitem__(self,register):
        if register in _REGISTER: return _REGISTER[register]
        else: raise KeyError(f"Register {register} not found.")
    
    def __setitem__(self,register, data):
        self.write(register, data)

    def write(self,register, data):
        if register in _REGISTER:
            _REGISTER[register] = data
    
    def read(self,register):
        if register in _REGISTER:
            return _REGISTER[register]

    def get_all(self):
        return _REGISTER
    
    def reset(self):
        for reg in _REGISTER:
            if reg in ['PC', 'SP']:
                _REGISTER[reg] = '0000H'
            else:
                _REGISTER[reg] = '00H'

class Flag:

    def __getitem__(self,flag):
        if flag in _FLAG: return _FLAG[flag]
        else: raise KeyError(f"Flag {flag} not found.")

    def __setitem__(self,flag, value):
        self.set(flag, value)

    def set(self,flag, value):
        if flag in _FLAG:
            _FLAG[flag] = 1 if value else 0
    
    def get(self,flag):
        if flag in _FLAG:
            return _FLAG[flag]
    
    def get_all(self):
        return _FLAG
    
    def reset(self):
        for flag in _FLAG:
            _FLAG[flag] = 0

class Assembler:

    def pass1(self, line:dict):

        pc = _REGISTER['PC']
        
        if 'label' in line:
            label = line['label']
            _STACK[label] = pc

        if 'code' in line:
            inst = line['inst']
            code = line['code']
            inr = INSTRUCTION[inst]['byte']

            _STACK[pc] = code
            _REGISTER['PC'] = encode(decode(pc) + inr, bit =4)
        
    def pass2(self):
        for pc, code in _STACK.items():
            if not isinstance(code, list):
                continue
            inst = code[0]
            if INSTRUCTION[inst]['param_rule'] == ['l']:
                label = code[1]
                if label not in _STACK:
                    self.reset()
                    return f'Subroutine {label} not defined'
                code[1] = _STACK[label]
                _STACK[pc] = code

        self.reset_pc()

    def reset(self):
        _STACK.clear()
        self.reset_pc()
        self.reset_sp()
    
    def reset_sp(self):
        _REGISTER['SP'] = '0000H'
    
    def reset_pc(self):
        _REGISTER['PC'] = '0000H'

def stack() -> list:
    sck = []
    label_flag = False
    for i in _STACK:
        if isinstance(_STACK[i], str): 
            sck.append([_STACK[i],i])
            label_flag = True
        
        elif isinstance(_STACK[i], list):
            inst, *code = _STACK[i]
            if inst in ['DB','ORG']: continue
            byte = str(INSTRUCTION[inst]['byte'])
        
            if inst == 'MOV':
                param = ','.join(code)
                opcode = INSTRUCTION[inst][param]
            else:
                try:
                    opcode = INSTRUCTION[inst]['op']
                except KeyError:
                    opcode = INSTRUCTION[inst][code[0]]
            
            if label_flag:
                sck[-1].extend( [inst,opcode,byte,'-'] )
                label_flag = False
            else: sck.append( [i,'-',inst,opcode,byte,'-'] )
            if int(byte) == 3:
                ldat, hdat = code[-1][2:], code[-1][:2] + 'H'
                sck.append( [operate(i,1,bit=4)] + ['-'] *4 + [ldat] )
                sck.append( [operate(i,2,bit=4)] + ['-'] *4 + [hdat] )
            elif int(byte) == 2:
                sck.append( [operate(i,1,bit=4)] + ['-'] *4 + [code[-1]] )
            
    return sck

def decode_rp(rp:str = 'H') -> str:
    if rp == 'B': return _REGISTER['B'][:-1] + _REGISTER['C']
    elif rp == 'D': return  _REGISTER['D'][:-1] + _REGISTER['E']
    else: return _REGISTER['H'][:-1] + _REGISTER['L']

def encode_rp(value:str, rp:str = 'H'):
    if rp == 'B':
        _REGISTER['B'] = value[:2] + 'H'
        _REGISTER['C'] = value[2:] 
    elif rp == 'D':
        _REGISTER['D'] = value[:2] + 'H'
        _REGISTER['E'] = value[2:] 
    elif rp == 'H':
        _REGISTER['H'] = value[:2] + 'H'
        _REGISTER['L'] = value[2:]

def check_carry(result:str | int, bit:int=2):
    if isinstance(result, str):
        result = decode(result)
    if bit == 4:
        _FLAG['C'] = int( result > 0xFFFF )
    elif bit == 2: 
        _FLAG['C'] = int( result > 0xFF )

def check_aux_carry(op1:str | int, op2:str | int):
    if isinstance(op1, str): op1 = decode(op1)
    if isinstance(op2, str): op2 = decode(op2)
    low_nibble_sum = (op1 & 0x0F) + (op2 & 0x0F)
    _FLAG['AC'] = int( low_nibble_sum > 0x0F )

def check_parity(result:str | int): 
    if isinstance(result, str): result = decode(result)
    _FLAG['P'] = int( bin(result).count('1') % 2 == 0 )
    
def check_zero(result:str | int):
    if isinstance(result, str): result = decode(result)
    _FLAG['Z'] = int( result == 0 )

def check_sign(result:str | int):
    if isinstance(result, str): result = decode(result)
    _FLAG['S'] = (result >> 7) & 1