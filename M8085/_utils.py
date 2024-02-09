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