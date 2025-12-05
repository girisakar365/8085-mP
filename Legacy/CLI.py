from cmd import Cmd
import time
import os
from json import load
from prettytable import PrettyTable
from M8085 import Control_Unit, Tool, Docs, get_token
from Ai import Assistant

class Interface(Cmd):
    intro = """
    Welcome to the 8085 Microprocessor Simulator!

    This simulator allows you to interact with an emulated 8085 microprocessor.
    Type 'help' for a list of available commands or 'help <command>' for detailed information.

    Get started by entering commands such as 'MOV A, B' or 'LXI H, 8000H'.
    """
    prompt = "> "
    doc_header = "Avaliable Help"
    ruler = '-'

    command_docs = Docs.command_docs

    def __init__(self):
        super().__init__()
        self.cu = Control_Unit(get_token())
        Tool.TOKEN = self.cu.get_token()
        if os.name == 'nt': os.system('CLS')
        elif os.name == 'posix': os.system('clear')

        self.session = {"messages":[]}

        self.error_msg = {
            'CommaError':lambda:self.response('Error: , missing'),
            'SyntaxError': lambda arg,syntax: self.response(f'Invalid Syntax: {arg}. Should be {syntax}.'),
            'TypeError':lambda:self.response('TypeError: Argument(s) missing'),
            'RpError': lambda arg:self.response(f'RpError: {arg}. Should be a vaild register pair (i.e H,B,D).'),
            'RpNotAllowedError': lambda :self.response(f'RpNotAllowedError: HL pair is not allowed. Should be a vaild register pair (i.e B,D).'),
            'NoArgumentError':lambda inst:self.response(f'NoArgumentError: {inst} takes no argument.'),
            'RegisterError':lambda register:self.response(f'RegisterError: {register} should be a vaild resigster (i.e. A,B,C,D,E,H,L)'),
            'DataError':lambda data:self.response(f'DataError: {data} should be a valid 8-bit data.'),
            'MemoryError':lambda memory:self.response(f'MemoryError: {memory} should be a valid 16-bit memory address.'),
            'PortError':lambda port:self.response(f'PortError: {port} should be a vaild 8-bit port address.')
        }

        with open("Syntax.json", "r") as errordict:
            self.specify_msg = load(errordict)

    def default(self,prompt):
        prompt_chunk = prompt.split(" ")
        inst,param = prompt_chunk[0], ''.join(prompt_chunk[1:])

        if inst in ['JMP','JC','JNZ', 'JZ', 'JNC', 'JP', 'JM', 'JPE', 'JPO', 'CALL', 'CC', 'CNC', 'CZ', 'CNZ', 'CP', 'CM', 'CPE', 'CPO']:
            self.response("NotAllowed: Branch instructions are under construction.")

        elif inst in self.cu.inst_list():
            status = Tool.check_param(inst,param)
            if status == 'CommaError' or status == 'TypeError':self.error_msg[status]()
            elif status == 'SyntaxError':self.error_msg[status](prompt,self.specify_msg[inst]['Syntax'])
            elif status == 'MemoryError':self.error_msg[status](prompt)
            elif status == 'RegisterError':self.error_msg[status](prompt)
            elif status == 'PortError':self.error_msg[status](prompt)
            elif status == 'DataError':self.error_msg[status](prompt)
            elif status == 'RpError':self.error_msg[status](param[0])
            elif status == 'RpNotAllowedError':self.error_msg[status]()
            elif status == 'NoArgumentError': self.error_msg[status](inst)
            else:
                self.cu.cycle(inst,status)
                if inst == 'HLT':
                    print(self.cu.assemble())
                    self.cu.reset()
                    self.mode = 1             
        elif prompt_chunk[0] == 'exam':

            if prompt_chunk[1] == 'memory': 
                memory_list = ''.join(prompt_chunk[2:])
                memory_table = PrettyTable(['Memory Address', 'Content'])
                try:
                    for i in memory_list.split(','):
                        memory_table.add_row([i.upper(),self.cu.show_memory()[i.upper()]])

                except KeyError:
                    self.response('Error: TypeError: Parameter not fulfilled. Should be exam memory (memory address, ...)')

                else:
                    print(memory_table)

            elif prompt_chunk[1] == 'register':
                register_table = PrettyTable(['Register','Content'])
                for i in self.cu.show_register():
                    if i != 'M':
                        register_table.add_row([i, self.cu.show_register()[i]])
                print(register_table)
            
            elif prompt_chunk[1] == 'flag':
                flag_table = PrettyTable(['Flag', 'Content'])
                for i in self.cu.show_flag():
                    flag_table.add_row([i,self.cu.show_flag()[i]])
                print(flag_table)
            
            elif prompt_chunk[1] == 'port':
                port_list = ''.join(prompt_chunk[2:])
                port_table = PrettyTable(['Port Address', 'Content'])
                try:
                    for i in port_list.split(','):
                        port_table.add_row([i.upper(),self.cu.show_port()[i.upper()]])

                except KeyError:
                    self.response('Error: TypeError: Parameter not fulfilled. Should be exam memory (port address, ...)')

                else:
                    print(port_table)

            else:
                self.response(f"Unknown command: {prompt}.Type 'help' for a list of commands.")
    
        elif prompt_chunk[0] == "@ask":
            self.history("user",' '.join(prompt_chunk[1:]))
            try:
                response:str = Assistant.generate(' '.join(prompt_chunk[1:]))
            except Exception:
                self.response("Opps! Something went wrong please try again.")
                self.history("assistant","Opps! Something went wrong please try again.")
            else:
                self.response(response)
                self.history("assistant",response)

        else:
            self.response(f"Unknown command: {prompt}.Type 'help' for a list of commands.")

    def do_quit(self, arg):
        "Quits your program"
        return True
        
    def do_assemble(self,arg):
        print(self.cu.assemble())

    def response(self,string:str, delay=0.018):
        for char in string:
            print(char, end ='', flush=True)
            time.sleep(delay)
        print('\n')

    def history(self, role:str, content:str):
        self.session["messages"].append({"role":role,"content":content})
    
    def do_help(self, arg: str):
        remove_space = ''.join(arg.split(' '))
        for i in remove_space.split(','):
            try:
                self.response("="*100 + f"\n{i}:\n" + "="*100,0.003)
                self.response(Interface.command_docs[i],0.003)
                self.response("="*100,0.003)
            except KeyError:
                self.response(f"Unknown command: {arg}.Type 'help <command name>' for a list of commands.")

    def do_clear(self,arg):
        """
        Clear the console screen.

        Args:None

        Example:
            > clear
            Console screen cleared.
        """
        if os.name == 'nt': os.system('CLS')
        elif os.name == 'posix': os.system('clear')

    do_cls = do_clear

if __name__ == "__main__":
    run = Interface()
    run.cmdloop()