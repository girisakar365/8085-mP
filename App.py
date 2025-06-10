import streamlit as st
from prettytable import PrettyTable
from json import load
from M8085 import Control_Unit, Tool, get_token, Docs, TimingDiagram
from M8085._utils import get_dict
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

    def _execute_compiled_code_dict(self, code_blocks, warnings):
        """Simulates execution using the get_dict block structure."""
        if not code_blocks:
            st.chat_message("assistant").write("Parsing resulted in no code blocks.")
            self.history("assistant", "Parsing resulted in no code blocks.")
            return

        # Display warnings from parsing
        if warnings:
            st.chat_message("assistant").write("Parser Warnings/Info:")
            self.history("assistant", ["Parser Warnings/Info:"] + warnings)

        # --- Determine Start Point ---
        current_label = "START"
        if current_label not in code_blocks:
            # Find the first label in the dict if START is missing
            first_label = next(iter(code_blocks), None)
            if first_label:
                 current_label = first_label
                 st.chat_message("assistant").write(f"Warning: No 'START' block found. Starting execution from first block: '{current_label}'.")
                 self.history("assistant", f"Warning: No 'START' block found. Starting execution from first block: '{current_label}'.")
            else: # Should be covered by empty check above, but safety
                 st.chat_message("assistant").write("Error: No 'START' block and no other blocks found.")
                 self.history("assistant", "Error: No 'START' block and no other blocks found.")
                 return

        current_index = 0
        program_stack = [] # Use a Python list to simulate the address stack for CALL/RET
        max_stack_depth = 100 # Prevent excessive recursion/stack usage

        # --- Execution Loop ---
        execution_steps = 0
        max_steps = 10000 # Safety break

        while execution_steps < max_steps:
            execution_steps += 1

            # Get current block and instruction
            current_block = code_blocks.get(current_label)
            if not current_block:
                st.chat_message("assistant").write(f"Execution Error: Jumped to unknown label '{current_label}'.")
                self.history("assistant", f"Execution Error: Jumped to unknown label '{current_label}'.")
                break

            if current_index >= len(current_block):
                # Reached end of block without explicit jump/ret/hlt
                # get_dict doesn't define fall-through, so this is an ambiguous end
                st.chat_message("assistant").write(f"Execution Halted: Reached end of block '{current_label}' without HLT, RET, or JMP.")
                self.history("assistant", f"Execution Halted: Reached end of block '{current_label}' without HLT, RET, or JMP.")
                break

            instruction_line = current_block[current_index]

            # Parse instruction line (already cleaned by get_dict)
            parts = instruction_line.split(maxsplit=1)
            inst = parts[0].upper()
            param_str = parts[1] if len(parts) > 1 else ""

            # --- Validate parameters ---
            validated_param = Tool.check_param(inst, param_str)

            if isinstance(validated_param, str) and 'Error' in validated_param: # More robust error check
                error_func = self.error_msg.get(validated_param.split(':')[0] if ':' in validated_param else validated_param) # Extract error type
                if error_func:
                    # Display error (simplified)
                    st.chat_message("assistant").write(f"Execution Error in block '{current_label}', index {current_index} ('{instruction_line}'): {validated_param}")
                    self.history("assistant", f"Execution Error in block '{current_label}', index {current_index} ('{instruction_line}'): {validated_param}")
                else:
                    st.chat_message("assistant").write(f"Execution Error in block '{current_label}', index {current_index} ('{instruction_line}'): Unknown validation error '{validated_param}'")
                    self.history("assistant", f"Execution Error in block '{current_label}', index {current_index} ('{instruction_line}'): Unknown validation error '{validated_param}'")
                break

            # --- Execute Instruction via Control Unit ---
            try:
                # Execute and get flow control result
                flow_result = self.cu.execute_instruction(inst, validated_param)

                # Default: move to next instruction within the same block
                next_label = current_label
                next_index = current_index + 1

                # Process flow control result
                if flow_result == "HLT":
                    st.chat_message("assistant").write(f"Execution Halted by {inst} in block '{current_label}', index {current_index}.")
                    self.history("assistant", f"Execution Halted by {inst} in block '{current_label}', index {current_index}.")
                    next_label = None # Signal stop
                elif isinstance(flow_result, str): # JMP or CALL taken, flow_result is target label
                    target_label = flow_result
                    if inst.startswith("CALL") or inst.startswith("C"): # Handle CALL/Ccc
                        if len(program_stack) >= max_stack_depth:
                             st.chat_message("assistant").write(f"Execution Error: Stack overflow during {inst}!")
                             self.history("assistant", f"Execution Error: Stack overflow during {inst}!")
                             next_label = None # Stop
                        else:
                            # Push return address (LABEL and INDEX+1 of instruction AFTER call)
                            return_point = (current_label, current_index + 1)
                            program_stack.append(return_point)
                            next_label = target_label
                            next_index = 0 # Start at beginning of target block
                    else: # Handle JMP/Jcc
                        next_label = target_label
                        next_index = 0 # Start at beginning of target block

                    # Validate target label exists
                    if next_label not in code_blocks:
                        st.chat_message("assistant").write(f"Execution Error: Invalid jump/call target label '{next_label}' from instruction '{instruction_line}'.")
                        self.history("assistant", f"Execution Error: Invalid jump/call target label '{next_label}' from instruction '{instruction_line}'.")
                        next_label = None # Stop

                elif flow_result is True: # RET or Rcc taken
                    if not program_stack:
                        st.chat_message("assistant").write(f"Execution Error: Stack underflow during {inst}!")
                        self.history("assistant", f"Execution Error: Stack underflow during {inst}!")
                        next_label = None # Stop
                    else:
                        return_point = program_stack.pop()
                        next_label, next_index = return_point # Restore label and index

                        # Validate popped label exists
                        if next_label not in code_blocks:
                           st.chat_message("assistant").write(f"Execution Error: Invalid return label '{next_label}' popped from stack.")
                           self.history("assistant", f"Execution Error: Invalid return label '{next_label}' popped from stack.")
                           next_label = None # Stop

                # Else (flow_result is None): Conditional jump/call/ret not taken, or normal instruction.
                # next_label and next_index are already set to continue sequentially.

            except Exception as e:
                st.chat_message("assistant").write(f"Runtime Error during execution in block '{current_label}', index {current_index} ('{instruction_line}'): {e}")
                self.history("assistant", f"Runtime Error during execution in block '{current_label}', index {current_index} ('{instruction_line}'): {e}")
                next_label = None # Stop on runtime error

            # --- Update state for next iteration ---
            if next_label is None: # Check for stop signal
                break
            current_label = next_label
            current_index = next_index

        # --- End of Loop ---
        if execution_steps >= max_steps:
            st.chat_message("assistant").write(f"Execution stopped: Maximum step limit ({max_steps}) reached. Potential infinite loop?")
            self.history("assistant", f"Execution stopped: Maximum step limit ({max_steps}) reached. Potential infinite loop?")
        elif next_label is not None: # Loop finished normally but without HLT signal
             # This case might indicate reaching the end of the final block if it doesn't HLT/RET/JMP
              st.chat_message("assistant").write("Execution finished.")
              self.history("assistant", "Execution finished.")


        # Optionally display final state
        st.chat_message("assistant").write("Final state:")
        self.history("assistant","Final state:")
        self._display_state()

    def scrap(self,prompt:str):
        prompt_chunk = prompt.split(" ")
        inst,param = prompt_chunk[0], ''.join(prompt_chunk[1:])

        # if inst in ['JMP','JC','JNZ', 'JZ', 'JNC', 'JP', 'JM', 'JPE', 'JPO', 'CALL', 'CC', 'CNC', 'CZ', 'CNZ', 'CP', 'CM', 'CPE', 'CPO']:
        #     st.chat_message("assistant").write("NotAllowed: Branch instructions are under construction.")
        #     self.history("assistant","NotAllowed: Branch instructions are under construction.")
            
        if inst in self.cu.inst_list():
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
        
        elif prompt_chunk[0].lower() == 'compile':
            assembly_code = ' '.join(prompt_chunk[1:])
            if not assembly_code:
                 msg = "Usage: compile <assembly code>"
                 st.chat_message("assistant").write(msg)
                 self.history("assistant", msg)
                 return

            msg = "Parsing code using get_dict..."
            st.chat_message("assistant").write(msg)
            self.history("assistant", msg)

            # --- Reset State ---
            # try:
            #     self.cu.reset() 
            #     msg = "(Processor state reset before execution)"
            #     st.chat_message("assistant").write(msg)
            #     self.history("assistant", msg)
            # except Exception as e:
            #      msg = f"Error during reset: {e}"
            #      st.error(msg)
            #      self.history("assistant", msg)
            #      return

            # --- Parse and Execute ---
            try:
                # Use get_dict which cleans lines and gives block structure
                code_blocks, warnings = get_dict(assembly_code)
                # Execute using the block-based simulation method
                self._execute_compiled_code_dict(code_blocks, warnings)
            except Exception as e:
                 st.error(f"Error during compilation/execution process: {e}")
                 self.history("assistant", f"Error during compilation/execution process: {e}")


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