import json

class Setup:
    def memory():
        return {hex(i)[2:].upper() + 'H':'0' for i in range(32768,40960)}


    def port():
        port = {}
        for i in range(256):
            if len(hex(i)[2:]) == 1 :port['0' + hex(i)[2:].upper() + 'H'] = '0'
            else: port[hex(i)[2:].upper() + 'H'] = '0'
        
        return port

    def register():
        return {'A':'0','B':'0','C':'0','D':'0','E':'0','F':'0','H':'0','L':'0','M':None}

    def flag():
        return {'S':0,'Z':0,'AC':0,'P':0,'C':0}
    
class Tool:
    TOKEN = None
    PARAM_RULE = {
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


    def check_param(inst:str,arg:str):
        prompt = arg.upper().replace(' ', '').split(',')

        if Tool.PARAM_RULE[inst][0] == 0:
            if len(prompt[0]) >= 1: return 'SyntaxError'

        elif Tool.PARAM_RULE[inst][0] == 1:

            if len(prompt[0]) != Tool.PARAM_RULE[inst][1]: return 'SyntaxError'
            elif len(prompt[0]) == 0: return 'TypeError'
            elif len(prompt[0]) == 1 and prompt[0] not in Tool.TOKEN['register'].keys(): return 'RegisterError'
            elif len(prompt[0]) == 5 and prompt[0] not in Tool.TOKEN['memory'].keys(): return 'MemoryError'
            elif len(prompt[0]) == 3 and prompt[0] not in Tool.TOKEN['port'].keys(): return 'DataError'
            else: return prompt

        else:
            if arg.find(',') == -1: return 'CommaError' 
            elif any([len(prompt[0]) != Tool.PARAM_RULE[inst][1],
                  len(prompt[1]) != Tool.PARAM_RULE[inst][2]]): return 'SyntaxError'
            elif len(prompt[0]) == 0 or len(prompt[1]) == 0: return 'TypeError'
            else:
                if any([len(prompt[0]) == 1  and prompt[0] == 'M' and Tool.check_pointer(prompt[0]),
                        len(prompt[1]) == 1 and prompt[1] == 'M' and Tool.check_pointer(prompt[0])]
                ): return 'PointerError'

                if any(
                    [len(prompt[0]) == 1 and prompt[0] not in Tool.TOKEN['register'].keys(),
                     len(prompt[1]) == 1 and prompt[1] not in Tool.TOKEN['register'].keys()]
                ): return 'RegisterError'
                elif any(
                    [len(prompt[0]) == 5 and prompt[0] not in Tool.TOKEN['memory'].keys(),
                     len(prompt[1]) == 5 and prompt[1] not in Tool.TOKEN['memory'].keys()]
                ): return 'MemoryError'
                elif len(prompt[1]) == 3 and prompt[1] not in Tool.TOKEN['port'].keys(): return 'DataError'
                else: return prompt
    
    def check_pointer(rp:str) -> bool:
        if rp == 'M': rp = 'H'
        if len(Tool.rp(rp)) != 5 and Tool.rp(rp) in Tool.TOKEN['port'].keys(): return True
        else: return False

    def rp(rp:str = 'H') -> str:
        if rp == 'B': return Tool.TOKEN["register"]['B'] + Tool.TOKEN["register"]['C'] + 'H'
        elif rp == 'D': return  Tool.TOKEN["register"]['D'] + Tool.TOKEN["register"]['E'] + 'H'
        else: return Tool.TOKEN["register"]['H'] + Tool.TOKEN["register"]['L'] + 'H'


def get_token():
    with open("M8085/memory.json","r") as load:
        return json.load(load)

def load_memory(arg,flag=True):
    with open("M8085/memory.json","w") as dump:
        if flag:
            json.dump(arg,dump,indent=4)

        else:
            data = {
                "memory":Setup.memory(),
                "register":Setup.register(),
                "flag":Setup.flag(),
                "port":Setup.port(),
            }
            json.dump(data,dump,indent=4)

def decode(arg:str, conversion:int = 16):
    return int(arg.replace('H',''),conversion)

def encode(arg:int | bool, flag:str = 'hex'):
    if flag == 'bin':
        return bin(arg)
    elif flag == 'bool':
        return int(arg)
    elif flag == 'hex':
        return hex(arg)[2:].upper() + 'H'