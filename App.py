import streamlit as st
from prettytable import PrettyTable
from json import load
from M8085 import Control_Unit, Tool, get_token, Docs, TimingDiagram
from Ai import Assistant

st.set_page_config(page_title="8085 Simulator",page_icon="assets/icon.png")
st.title('Welcome to 8085 Simulator')
st.markdown("""
This simulator allows you to interact with an emulated 8085 microprocessor.

Get started by entering commands such as 'MOV A, B' or 'LXI H, 8000H'.""")

class App():
    def __init__(self):

        self.error_msg = {
            'CommaError':lambda:[st.chat_message("assistant").write('Error: , missing'),
                self.history('assistant','Error: , missing')],
            'SyntaxError': lambda arg,syntax: [st.chat_message("assistant").write(f'Invalid Syntax: {arg}. Should be {syntax}.'),
                self.history('assistant',f'Invalid Syntax: {arg}. Should be {syntax}.')],
            'TypeError':lambda:[st.chat_message("assistant").write('TypeError: Argument(s) missing'),
                self.history('assistant','TypeError: Argument(s) missing')],
            'RpError': lambda arg:[st.chat_message("assistant").write(f'RpError: {arg}. Should be a vaild register pair (i.e B,D,H).'),
                self.history('assistant',f'RpError: {arg}. Should be a vaild register pair (i.e B,C,D,E,H,L).')],
            'RpNotAllowedError': lambda arg:[st.chat_message("assistant").write(f'RpNotAllowedError: HL pair is not allowed. Should be a vaild register pair (i.e B,D).'),
                self.history('assistant',f'RpNotAllowedError: HL pair is not allowed. Should be a vaild register pair (i.e B,D).')],
            'NoArgumentError':lambda inst:[st.chat_message("assistant").write(f'{inst} takes no argument.'),
                self.history('assistant',f'{inst} takes no argument.')],
            'PointerError':lambda pointer:[st.chat_message("assistant").write(f'PointerError: {pointer} is not pointing to any memory address.'),
                self.history('assistant',f'PointerError: {pointer} is not pointing to any memory address.')],
            'RegisterError':lambda register:[st.chat_message("assistant").write(f'RegisterError: {register} should be a vaild resigster (i.e. A,B,C,D,E,H,L)'),
                self.history('assistant',f'RegisterError: {register} should be a vaild resigster (i.e. A,B,C,D,E,H,L)')],
            'DataError':lambda data:[st.chat_message("assistant").write(f'DataError: {data} should be a valid 8-bit data.'),
                self.history('assistant',f'DataError: {data} should be a valid 8-bit data.')],
            'MemoryError':lambda memory:[st.chat_message("assistant").write(f'MemoryError: {memory} should be a valid 16-bit memory address.'),
                self.history('assistant',f'MemoryError: {memory} should be a valid 16-bit memory address.')],
            'PortError':lambda port:[st.chat_message("assistant").write(f'PortError: {port} should be a vaild 8-bit port address.'),
                self.history('assistant',f'PortError: {port} should be a vaild 8-bit port address.')]
        }
        with open("Syntax.json", "r") as errordict:
            self.specify_msg = load(errordict)

        if 'token' not in st.session_state:
            st.session_state['token'] =  get_token()
        if 'cu' not in st.session_state:
            st.session_state['cu'] = Control_Unit(st.session_state.token)
        
        self.cu = st.session_state.cu
        Tool.TOKEN = st.session_state.token
        self.display()

    def display(self):

        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        for message in st.session_state["messages"]:
            st.chat_message(message["role"]).write(message["content"])

        if prompt := st.chat_input("Command here . . ."):
            st.chat_message("user").write(prompt)
            self.history("user",prompt)
            self.scrap(prompt)

    def history(self,role:str,content:str):
        st.session_state["messages"].append({"role":role,"content":content})

    def scrap(self,prompt:str):
        prompt_chunk = prompt.split(" ")
        inst,param = prompt_chunk[0], ''.join(prompt_chunk[1:])

        if inst in ['JMP','JC','JNZ', 'JZ', 'JNC', 'JP', 'JM', 'JPE', 'JPO', 'CALL', 'CC', 'CNC', 'CZ', 'CNZ', 'CP', 'CM', 'CPE', 'CPO']:
            st.chat_message("assistant").write("NotAllowed: Branch instructions are under construction.")
            self.history("assistant","NotAllowed: Branch instructions are under construction.")
            
        elif inst in self.cu.inst_list():
            inst,param = prompt_chunk[0], ''.join(prompt_chunk[1:])
            status = Tool.check_param(inst,param)
            if status == 'CommaError' or status == 'TypeError':self.error_msg[status]()
            elif status == 'SyntaxError':self.error_msg[status](prompt,self.specify_msg[inst]['Syntax'])
            elif status == 'MemoryError':self.error_msg[status](prompt)
            elif status == 'RegisterError':self.error_msg[status](prompt)
            elif status == 'PortError':self.error_msg[status](prompt)
            elif status == 'DataError':self.error_msg[status](prompt)
            elif status == 'RpError': self.error_msg[status](prompt[0])
            elif status == 'RpNotAllowedError':self.error_msg[status]()
            elif status == 'NoArgumentError': self.error_msg['NoArgumentError'](inst)
            else:
                self.cu.cycle(inst,status)
                if not self.cu.mode and inst == 'HLT':
                    print(self.cu.assemble())
                    self.cu.reset()
                    self.mode = 1

        elif prompt_chunk[0] == 'exam':
            if prompt_chunk[1] == 'memory': 
                memory_list = ''.join(prompt_chunk[2:])
                memory_table = PrettyTable(['Memory Address', 'Content'])
                try:
                    for i in memory_list.split(','):
                        memory_table.add_row([i.upper(),st.session_state.token["memory"][i.upper()]])

                except KeyError:
                    st.chat_message('assistant').write('Error: TypeError: Parameter not fulfilled. Should be exam memory (memory address, ...)')
                    self.history('assistant','TypeError: Parameter not fulfilled. Should be exam memory (memory address, ...)')

                else:
                    st.chat_message('assistant').write(memory_table)
                    self.history('assistant',memory_table)

            elif prompt_chunk[1] == 'register':
                register_table = PrettyTable(['Register', 'Content'])
                for i in self.cu.show_register():
                    if i != 'M':
                        register_table.add_row([i,st.session_state.token["register"][i]])
                st.chat_message('assistant').write(register_table)
                self.history('assistant',register_table)
            
            elif prompt_chunk[1] == 'flag':
                flag_table = PrettyTable(['Flag', 'Content'])
                for i in self.cu.show_flag():
                    flag_table.add_row([i,st.session_state.token["flag"][i]])
                st.chat_message('assistant').write(flag_table)
                self.history('assistant',flag_table)
            
            elif prompt_chunk[1] == 'port':
                port_list = ''.join(prompt_chunk[2:])
                port_table = PrettyTable(['Port Address', 'Content'])
                try:
                    for i in port_list.split(','):
                        port_table.add_row([i.upper(),st.session_state.token['port'][i.upper()]])

                except KeyError:
                    st.chat_message('assistant').write('Error: TypeError: Parameter not fulfilled. Should be exam memory (port address, ...)')
                    self.history('assistant','TypeError: Parameter not fulfilled. Should be exam memory (port address, ...)')

                else:
                    st.chat_message('assistant').write(port_table)
                    self.history('assistant',port_table)
            
            else:
                st.chat_message("assistant").write(f"Unknown command: {prompt}.\nType 'help' for a list of commands.")
                self.history("assistant",f"Unknown command: {prompt}.\nType 'help' for a list of commands.")
            
        elif prompt_chunk[0] == 'assemble':
            table = self.cu.assemble()
            st.chat_message("assistant").write(table)
            self.history("assistant",table)

        elif prompt_chunk[0].lower() == 'timing':
            try:
                timing_graph = TimingDiagram().plot_full(prompt_chunk[1])
                st.chat_message("assistant").pyplot(timing_graph)
                self.history("assistant",timing_graph)
            except Exception:
                st.chat_message('assistant').write('Error: TypeError: Parameter not fulfilled. Should be timing instruction (instruction name)')
                self.history('assistant','TypeError: Parameter not fulfilled. Should be timing instruction (instruction name)')

        # elif prompt_chunk[0] == 'help':
            #     remove_space = ''.join(arg.split(' '))
            #     for i in remove_space.split(','):
            #         try:
            #             st.chat_message('assistant').write(f'### {i}:')
            #             st.chat_message('assistant').write(Docs.command_docs[i])
            #         except KeyError:
            #             st.chat_message('assistant').write(f"Unknown command: {prompt}.Type 'help <command name>' for a list of commands.")
            
        elif prompt_chunk[0] == "@ask":
            try:
                response:str = Assistant.generate(' '.join(prompt_chunk[1:]))
            except Exception:
                st.chat_message("assistant").write("Opps! Something went wrong please try again.")
                self.history("assistant","Opps! Something went wrong please try again.")
            else:
                st.chat_message("assistant").write(response)
                self.history("assistant",response)

        else:
            st.chat_message("assistant").write(f"Unknown command: {prompt}.\nType 'help' for a list of commands.")
            self.history("assistant",f"Unknown command: {prompt}.\nType 'help' for a list of commands.")
            
if __name__ == "__main__":
    app = App()