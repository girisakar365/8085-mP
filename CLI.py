from cmd import Cmd
import os
from prettytable import PrettyTable
from mP import Simulator

class Interface(Cmd):
    intro = """
    Welcome to the 8085 Microprocessor Simulator!

    This simulator allows you to interact with an emulated 8085 microprocessor.
    Type 'help' for a list of available commands or 'help <command>' for detailed information.

    Get started by entering commands such as 'MOV A, B' or 'LXI H, 2000H'.
    """
    prompt = "> "
    doc_header = "Avaliable Help"
    ruler = '-'

    def __init__(self):
        super().__init__()
        self.mP = Simulator()
        if os.name == 'nt': os.system('CLS')
        elif os.name == 'posix': os.system('clear')

        self.error_msg = {
            'CommaError':lambda:print('Error: , missing'),
            'SyntaxError': lambda arg,syntax: print(f'Invalid Syntax: {arg}. Should be {syntax}.'),
            'TypeError':lambda:print('TypeError: Argument(s) missing'),
            'AddressError':lambda arg:print(f'AddressError: {arg}. Should be a vaild 16-bit memory location.'),
            'RpError': lambda arg:print(f'RpError: {arg}. Should be a vaild register pair (i.e B,C,D,E,H,L).'),
            'NoArgumentError':lambda inst:print(f'{inst} takes no argument.'),
            'PointerError':lambda pointer:print(f'PointerError: {pointer} is not pointing to any memory address.'),
            'RegisterError':lambda register:print(f'RegisterError: {register} should be a vaild resigster (i.e. A,B,C,D,E,H,L)'),
            'DataError':lambda data:print(f'DataError: {data} should be a valid 8-bit data.'),
            'MemoryError':lambda memory:print(f'MemoryError: {memory} should be a valid 16-bit memory address.'),
            'PortError':lambda port:print(f'PortError: {port} should be a vaild 8-bit port address.')
        }

    def default(self,line):
        print(f"Unknown command: {line}.\nType 'help' for a list of commands.")
    
    def do_quit(self, arg):
        "Quits your program"
        return True

    def do_MOV(self, arg:str):
        """
        Args: register destination, register source

        Raises:
            - If the syntax is incorrect or if the ',' is missing.
            - If there are invalid parameters (should be MOV rd, rs).
            - If 'rd' is not a register.
            - If 'rs' is not a register.

        Notes:
            The expected syntax for the MOV instruction is 'MOV rd, rs',
            where 'rd' is the destination and 'rs' is the source.

        Example:
            > MOV A,B
        """
        status = self.mP.check_param('MOV',arg)

        if status == 'CommaError': self.error_msg[status]()
        elif status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status]('MOV ' + arg,'MOV rd,rs')
        elif status == 'RegisterError': self.error_msg[status]('rd/rs')
        elif status == 'PointerError': self.error_msg[status]('M')
        else:
            rd,rs = status
            self.mP.op_code('MOV')(rd,rs)

    def do_MVI(self, arg:str):
        """
        Execute the MVI instruction to move immediate data into a register.

        Args:
            arg (str): String representing the instruction with register and 8-bit data.

        Raises:
            - If the syntax is incorrect or if the ',' is missing.
            - If there are invalid parameters (should be MVI R, 8 bit data).
            - If 'R' is not a register.
            - If the content is not 8-bit.

        Notes:
            The expected syntax for the MVI instruction is 'MVI R, 8 bit data',
            where 'R' is the destination register, and '8 bit data' is the immediate data.

        Example:
            > MVI A, 42
            Moves the immediate value 42 into register A.
        """
        status = self.mP.check_param('MVI',arg)
        if status == 'CommaError': self.error_msg[status]()
        elif status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](f'MVI {arg}','MVI r,data (8-bit)')
        elif status == 'RegisterError': self.error_msg[status]('r')
        elif status == 'DataError': self.error_msg[status]('data') 
        elif status == 'PointerError': self.error_msg[status]('M')
        else:
            r,data = status
            self.mP.op_code('MVI')(r,data)

    def do_LXI(self, arg:str):
        """
        Execute the LXI instruction to load 16-bit immediate data into a register pair.

        Args:
            arg (str): String representing the instruction with register pair and 16-bit data.

        Raises:
            - If the syntax is incorrect or if the ',' is missing.
            - If there are invalid parameters (should be LXI Rp, 16 bit data).
            - If 'Rp' is not a register pair.
            - If the content is not 16-bit hexadecimal.
            - If the provided memory address is restricted or not a valid memory address.

        Notes:
            The expected syntax for the LXI instruction is 'LXI Rp, 16 bit data',
            where 'Rp' is the register pair, and '16 bit data' is the immediate 16-bit hexadecimal data.

        Example:
            > LXI H, 2000H
            Loads the immediate 16-bit hexadecimal value 2000H into register pair H-L.
        """
        status = self.mP.check_param('LXI',arg)
        if status == 'CommaError': self.error_msg[status]()
        elif status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](f'LXI {arg}','LXI rp,memory address')
        elif status == 'MemoryError': self.error_msg[status]( arg.replace(' ','').split(',')[1] )
        elif status == 'RegisterError' or arg.replace(' ','').split(',')[0] in ['A','M','F']: self.error_msg['RpError'](arg)
        else:
            rp,data = status
            self.mP.op_code('LXI')(rp,data)  

    def do_LDA(self,arg:str):
        """
        Execute the LDA instruction to load data from a memory address into the accumulator.

        Args:
            arg (str): String representing the instruction with the memory address.

        Raises:
            - If there are insufficient parameters (should be LDA 16 bit data (hex)).
            - If the provided memory address is restricted or not a valid memory address.

        Example:
            > LDA 2000H
            Loads the accumulator with the contents stored at the memory address 2000H.
        """
        status = self.mP.check_param('LDA',arg)
        if status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](arg,'LDA 16-bit memory address')
        elif status == 'MemoryError': self.error_msg[status](arg)
        else:
            self.mP.op_code('LDA')(status[0])

    def do_STA(self,arg:str):
        """
        Execute the STA instruction to store the accumulator contents into a memory address.

        Args:
            arg (str): String representing the instruction with the memory address.

        Raises:
            - If there are insufficient parameters (should be STA 16 bit data (hex)).
            - If the provided memory address is restricted or not a valid memory address.

        Example:
            > STA 2000H
            Stores the contents of the accumulator into the memory address 2000H.
        """
        status = self.mP.check_param('STA',arg)
        if status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](arg,'STA 16-bit memory address')
        elif status == 'MemoryError': self.error_msg[status](arg)
        else:
            self.mP.op_code('STA')(status[0])

    def do_LDAX(self,arg:str):
        """
        Execute the LDAX instruction to load the accumulator with data from the specified register pair.

        Args:
            arg (str): String representing the instruction with the register pair.

        Raises:
            - If there are insufficient parameters (should be LDAX register pair (rp)).
            - If 'rp' is not a valid register pair.

        Example:
            > LDAX B
            Loads the accumulator with the contents of the memory location specified by the register pair B.
        """
        status = self.mP.check_param('LDAX',arg)
        if status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](arg,'LDAX register pair (rp)')
        elif status == 'RegisterError' or arg.replace(' ','').split(',')[0] in ['A','M','F']: self.error_msg['RpError'](arg)
        else:
            self.mP.op_code('LDAX')(status[0])

    def do_STAX(self,arg:str):
        """
        Execute the STAX instruction to store the accumulator contents into the memory location specified by the register pair.

        Args:
            arg (str): String representing the instruction with the register pair.

        Raises:
            - If there are insufficient parameters (should be STAX register pair (rp)).
            - If 'rp' is not a valid register pair.

        Example:
            > STAX D
            Stores the contents of the accumulator into the memory location specified by the register pair D.
        """
        status = self.mP.check_param('STAX',arg)
        if status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](arg,'STAX register pair (rp)')
        elif status == 'RegisterError' or arg.replace(' ','').split(',')[0] in ['A','M','F']: self.error_msg['RpError'](arg)
        else:
            self.mP.op_code('STAX')(status[0])

    def do_LHLD(self,arg:str):
        """
        Load HL register pair with data from specified memory address.

        Args:
            arg (str): 16-bit memory location in hexadecimal.

        Raises:
            - If the syntax is incorrect or if the memory location is invalid.

        Example:
            > LHLD 2000H
        """
        status = self.mP.check_param('LHLD',arg)
        if status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](arg,'LHLD 16 bit memory location (hex)')
        elif status == 'MemoryError': self.error_msg[status](arg)
        else:
            self.mP.op_code('LHLD')(status[0])

    def do_SHLD(self,arg:str):
        """
        Store the content of HL register pair at the specified memory address.

        Args:
            arg (str): 16-bit memory location in hexadecimal.

        Raises:
            - If the syntax is incorrect or if the memory location is invalid.

        Example:
            > SHLD 2000H
        """
        status = self.mP.check_param('SHLD',arg)
        if status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](arg,'SHLD 16 bit memory location (hex)')
        elif status == 'MemoryError': self.error_msg[status](arg)
        else:
            self.mP.op_code('SHLD')(status[0])
    
    def do_IN(self,arg:str):
        """
        Input data from the specified 8-bit port location into the accumulator (A).

        Args:
            arg (str): 8-bit port location in hexadecimal.

        Raises:
            - If the syntax is incorrect or if the port location is invalid.

        Example:
            > IN 10H
        """
        status = self.mP.check_param('IN',arg)
        if status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](arg,'IN 8 bit port location')
        elif status == 'DataError': self.error_msg['PortError'](arg)
        else:
            self.mP.op_code('IN')(status[0])

    def do_OUT(self,arg:str):
        """
        Output data from the accumulator (A) to the specified 8-bit port location.

        Args:
            arg (str): 8-bit port location in hexadecimal.

        Raises:
            - If the syntax is incorrect or if the port location is invalid.

        Example:
            > OUT 20H
        """
        status = self.mP.check_param('OUT',arg)
        if status == 'TypeError': self.error_msg[status]()
        elif status == 'SyntaxError': self.error_msg[status](arg,'OUT 8 bit port location')
        elif status == 'DataError': self.error_msg['PortError'](arg)
        else:
            self.mP.op_code('OUT')(status[0])
    
    def do_XCHG(self,arg):
        """
        Exchange the contents of the DE and HL register pairs.

        Args:
            arg (str): Not used.

        Raises:
            - If the command is followed by an argument (XCHG takes no argument).

        Example:
            > XCHG
            DE and HL register pairs after XCHG:
            DE: 12F6   HL: AB78
        """
        status = self.mP.check_param('XCHG',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"XCHG takes no argument")
        elif self.mP.check_pointer('D') or self.mP.check_pointer('H'): self.error_msg['PointerError']('Either H or D')
        else:
            self.mP.op_code('XCHG')()

    def do_ADD(self,arg:str):
        """
        Add the content of the specified register to the accumulator.

        Args:
            arg (str): The register (r) whose content will be added to the accumulator.

        Raises:
            - If the syntax is incorrect or if there are additional parameters.
            - If the specified register (r) is not valid.

        Example:
            > ADD B
        """
        status = self.mP.check_param('ADD',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,'ADD r/m')
        elif status == 'RegisterError': self.error_msg[status](arg,'ADD r/m')
        else:
            self.mP.op_code('ADD')(status[0])
    
    def do_ADC(self, arg:str):
        """
        Args: register_or_memory

        Raises:
            - If the syntax is incorrect or if the ',' is missing.
            - If the parameter is not a register or 'M'.

        Notes:
            The expected syntax for the ADC instruction is 'ADC rd',
            where 'rd' is either a register or 'M' for memory content.

        Example:
            > ADC A       # Adds the content of register A along with carry to register A
            > ADC M       # Adds the content of memory pointed to by HL along with carry to register A
        """
        status = self.mP.check_param('ADC', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status]('ADC ' + arg, 'ADC r')
        elif status == 'RegisterError':
         self.error_msg[status](arg)
        else:
            self.mP.op_code('ADC')(status[0])


    def do_ADI(self, arg:str):
        """
        Args: 8-bit_data

        Raises:
            - If there are insufficient parameters (should be ADI 8-bit data).
            - If the parameter is not a valid 8-bit data.

        Notes:
            The expected syntax for the ADI instruction is 'ADI 8-bit data',
            where '8-bit data' is the immediate 8-bit data to be added to the accumulator.

        Example:
            > ADI 42H
            Adds the immediate value 42 to the accumulator.
        """
        status = self.mP.check_param('ADI', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'ADI 8-bit data')
        elif status == 'DataError':
         self.error_msg[status](arg)
        else:
            self.mP.op_code('ADI')(status)

    def do_DAD(self, arg:str):
        """
        Adds the contents of register pair specified by 'Rp' to register pair H-L.

        Args: register_pair

        Raises:
            - If there are insufficient parameters (should be DAD Rp).
            - If 'Rp' is not a valid register pair.

        Notes:
            The DAD instruction adds the contents of the specified register pair to the H-L register pair.

        Example:
            > DAD B
            Adds the contents of register pair B-C to register pair H-L.
        """
        status = self.mP.check_param('DAD', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'DAD Rp')
        elif status == 'RegisterError' or arg[0] in ['A','H','M','F']:
         self.error_msg['RpError'](arg)
        elif self.mP.check_pointer(arg[0]):
         self.error_msg['PointerError'](arg[0])
        else:
            self.mP.op_code('DAD')(status[0])

    def do_SUB(self, arg:str):
        """
        Subtracts the contents of the specified register or memory address from the accumulator.

        Args: register_or_memory

        Raises:
            - If there are insufficient parameters (should be SUB rd or SUB M).
            - If the parameter is not a valid register or memory address pointer.

        Notes:
            The SUB instruction subtracts the contents of the specified register or memory address from the accumulator.

        Example:
            > SUB B
            Subtracts the content of register B from the accumulator.
            > SUB M
            Subtracts the content of memory pointed to by HL from the accumulator.
        """
        status = self.mP.check_param('SUB', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'SUB r/m')
        elif status == 'RegisterError':
         self.error_msg[status](arg)
        elif self.mP.check_pointer(arg[0]):
         self.error_msg['PointerError'](arg[0])
        else:
            self.mP.op_code('SUB')(status)

    def do_SUI(self, arg:str):
        """
        Subtracts the immediate 8-bit data from the accumulator.

        Args: 8-bit_data

        Raises:
            - If there are insufficient parameters (should be SUI 8-bit data).
            - If the parameter is not a valid 8-bit data.

        Notes:
            The SUI instruction subtracts the immediate 8-bit data from the accumulator.

        Example:
            > SUI 42H
            Subtracts the immediate value 42 from the accumulator.
        """
        status = self.mP.check_param('SUI', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'SUI 8-bit data (hex)')
        elif status == 'DataError':
         self.error_msg[status](arg)
        else:
            self.mP.op_code('SUI')(status[0])
    
    def do_SBI(self, arg:str):
        """
        Subtracts the immediate 8-bit data along with the carry from the accumulator.

        Args: 8-bit_data

        Raises:
            - If there are insufficient parameters (should be SBI 8-bit data).
            - If the parameter is not a valid 8-bit data.

        Notes:
            The SBI instruction subtracts the immediate 8-bit data along with the carry from the accumulator.

        Example:
            > SBI 42H
            Subtracts the immediate value 42 along with the carry from the accumulator.
        """
        status = self.mP.check_param('SBI', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'SBI 8-bit data (hex)')
        elif status == 'DataError':
         self.error_msg[status](arg)
        else:
            self.mP.op_code('SBI')(status[0])

    def do_SBB(self, arg:str):
        """
        Subtracts the contents of the specified register or memory address along with the borrow from the accumulator.

        Args: register_or_memory

        Raises:
            - If there are insufficient parameters (should be SBB rd or SBB M).
            - If the parameter is not a valid register or memory address pointer.

        Notes:
            The SBB instruction subtracts the contents of the specified register or memory address along with the borrow from the accumulator.

        Example:
            > SBB B
            Subtracts the content of register B along with the borrow from the accumulator.
            > SBB M
            Subtracts the content of memory pointed to by HL along with the borrow from the accumulator.
        """
        status = self.mP.check_param('SBB', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'SBB r/m')
        elif status == 'RegisterError':
         self.error_msg[status](arg)
        elif arg[0] == 'M' and self.mP.check_pointer(arg[0]):
         self.error_msg['PointerError'](arg) 
        else:
            self.mP.op_code('SBB')(status[0])

    def do_INR(self, arg:str):
        """
        Increments the contents of the specified register or memory address.

        Args: register_or_memory

        Raises:
            - If there are insufficient parameters (should be INR rd or INR M).
            - If the parameter is not a valid register or memory address pointer.

        Notes:
            The INR instruction increments the contents of the specified register or memory address.

        Example:
            > INR B
            Increments the content of register B.
            > INR M
            Increments the content of memory pointed to by HL.
        """
        status = self.mP.check_param('INR', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'INR r/m')
        elif status == 'RegisterError':
         self.error_msg[status](arg)
        elif self.mP.check_pointer(arg[0]):
         self.error_msg['PointerError'](arg) 
        else:
            self.mP.op_code('INR')(status[0])

    def do_INX(self, arg:str):
        """
        Increments the specified register pair.

        Args: register_pair

        Raises:
            - If there are insufficient parameters (should be INX Rp).
            - If 'Rp' is not a valid register pair.

        Notes:
            The INX instruction increments the specified register pair.

        Example:
            > INX B
            Increments the register pair B-C.
        """
        status = self.mP.check_param('INX', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'INX Rp')
        elif status == 'RegisterError' or arg[0] in ['A','M','F']:
         self.error_msg['RpError'](arg)
        elif self.mP.check_pointer(arg[0]):
         self.error_msg['PointerError'](arg)
        else:
            self.mP.op_code('INX')(status[0])

    def do_DCX(self, arg:str):
        """
        Decrements the specified register pair.

        Args: register_pair

        Raises:
            - If there are insufficient parameters (should be DCX Rp).
            - If 'Rp' is not a valid register pair.

        Notes:
            The DCX instruction decrements the specified register pair.

        Example:
            > DCX B
            Decrements the register pair B-C.
        """
        status = self.mP.check_param('DCX', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'DCX Rp')
        elif status == 'RegisterError' or arg[0] in ['A','M','F']:
         self.error_msg['RpError'](arg)
        elif self.mP.check_pointer(arg[0]):
         self.error_msg['PointerError'](arg)
        else:
            self.mP.op_code('DCX')(status)
    
    def do_DCR(self, arg:str):
        """
        Decrements the contents of the specified register or memory address.

        Args: register_or_memory

        Raises:
            - If there are insufficient parameters (should be DCR rd or DCR M).
            - If the parameter is not a valid register or memory address pointer.

        Notes:
            The DCR instruction decrements the contents of the specified register or memory address.

        Example:
            > DCR B
            Decrements the content of register B.
            > DCR M
            Decrements the content of memory pointed to by HL.
        """
        status = self.mP.check_param('DCR', arg)

        if status == 'TypeError':
         self.error_msg[status]()
        elif status == 'SyntaxError':
         self.error_msg[status](arg, 'DCR rd or DCR M')
        elif status == 'RegisterError':
         self.error_msg[status](arg)
        elif self.mP.check_pointer(arg[0]):
         self.error_msg['PointerError'](arg)
        else:
            self.mP.op_code('DCR')(status)
            
    def do_RRC(self, arg:str):
        """
        Rotate the content of accumulator from right

        Args: No arguments
        
        Example:
            > RRC 
            Rotate the content of register B.
        """
        status = self.mP.check_param('RRC',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"RAR takes no argument")
        else:
            self.mP.op_code('RRC')()
            
    def do_RAR(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('RAR',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"RAR takes no argument")
        else:
            self.mP.op_code('RAR')()
    
    def do_RLC(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('RLC',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"RLC takes no argument")
        else:
            self.mP.op_code('RLC')()
    
    def do_RAL(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('RAL',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"RAL takes no argument")
        else:
            self.mP.op_code('RAL')()
    
    def do_ANI(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('ANI',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"ANI takes no argument")
        if status == 'DataError': self.error_msg[status](arg)
        else:
            self.mP.op_code('ANI')(status[0])
    
    def do_ORI(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('ORI',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"ORI takes no argument")
        if status == 'DataError': self.error_msg[status](arg)
        else:
            self.mP.op_code('ORI')(status[0])
    
    def do_XRI(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('XRI',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"XRI takes no argument")
        if status == 'DataError': self.error_msg[status](arg)
        else:
            self.mP.op_code('XRI')(status[0])
    
    def do_ANA(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('ANA',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"ANA takes no argument")
        if status == 'DataError': self.error_msg[status](arg)
        else:
            self.mP.op_code('ANA')(status[0])
    
    def do_ORA(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('ORA',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"ORA takes no argument")
        if status == 'DataError': self.error_msg[status](arg)
        else:
            self.mP.op_code('ORA')(status[0])
    
    def do_XRA(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > RAR 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('XRA',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"XRA takes no argument")
        if status == 'Register': self.error_msg[status](arg)
        else:
            self.mP.op_code('XRA')(status[0])
    
    def do_CMA(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > CMA 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('CMA',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"CMA takes no argument")
        else:
            self.mP.op_code('CMA')()
    
    def do_STC(self, arg:str):
        """
        Rotate the content of accumulator from right along with the carry flag

        Args: No arguments
        
        Example:
            > STC 
            Rotate the content of register B. Then the carry changes to LSB and MSB becomes carry shifting the content of accumulator.
        """
        status = self.mP.check_param('STC',arg)
        if status == 'SyntaxError': self.error_msg[status](arg,"STC takes no argument")
        else:
            self.mP.op_code('STC')()

    def do_exmin_memory(self,arg:str):
        """
        Display memory addresses and their contents.

        Args:
            arg (str): Comma-separated list of memory addresses.

        Raises:
            KeyError: If the provided memory address is invalid.

        Example:
            > exmin_memory 2000H, 3000H
            +----------------+--------+
            | Memory Address | Content|
            +----------------+--------+
            |     2000H      |   1A   |
            |     3000H      |   FF   |
            +----------------+--------+
        """
        memory_table = PrettyTable(['Memory Address', 'Content'])
        try:
            for i in arg.split(','):
                memory_table.add_row([i.upper(),self.mP.show('M',i.upper())])

        except KeyError: print("Error: Invalid argument!")

        else: print(memory_table)

    def do_exmin_port(self,arg:str):
        """
        Display port addresses and their contents.

        Args:
            arg (str): Comma-separated list of port addresses.

        Raises:
            KeyError: If the provided port address is invalid.

        Example:
            > exmin_port 10H, 20H
            +--------------+---------+
            | Port Address | Content |
            +--------------+---------+
            |     10H      |   0A    |
            |     20H      |   FF    |
            +--------------+---------+
        """
        port_table = PrettyTable(['Port Address', 'Content'])
        try:
            for i in arg.split(','):
                port_table.add_row([i.upper(),self.mP.show('P',i.upper())])

        except KeyError: print("Error: Invalid argument!")

        else: print(port_table)

    def do_exmin_memol(self,arg):
        """
        Display memory and its contents.

        Args: None

        Example:
            > exmin_memol
            +----------------+--------+
            | Memory Address | Content|
            +----------------+--------+
            | 8000H          | 1A     |
            | 8001H          | 2B     |
            | ...            | ...    |
            +----------------+--------+
        """
        memory_table = PrettyTable(['Memory Address', 'Content'])   
        for i in self.mP.show_memory():
            memory_table.add_row([i,self.mP.show('M',i)])
        
        print(memory_table)
    
    def do_exmin_register(self,arg):
        """
        Display registers and their contents.

        Args: None

        Example:
            > exmin_register
            +-----------+--------+
            | Register  | Content|
            +-----------+--------+
            | A         | 1A     |
            | B         | 2B     |
            | ...       | ...    |
            +-----------+--------+
        """
        register_table = PrettyTable(['Register', 'Content'])
        for i in self.mP.show_register():
            if i != 'M' and i != 'F':
                register_table.add_row([i,self.mP.show('R',i)])
        
        print(register_table)
    
    def do_exmin_flag(self,arg):
        """
        Display flags and their contents.

        Args:
            arg (str): Not used.

        Example:
            > exmin_flag
            +---+---+----+---+---+
            | S | Z | AC | P | C |
            +---+---+----+---+---+
            | 0 | 0 | 0  | 0 | 0 |
            +---+---+----+---+---+
        """
        flag_table = PrettyTable([i for i in self.mP.show_flag()])
        flag_table.add_row([self.mP.show('F',i) for i in self.mP.show_flag()])
        
        print(flag_table)
    
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