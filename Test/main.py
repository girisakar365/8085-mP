# from pathlib import Path

# PATH = Path(__file__).parent / 'Programs'

# with open(PATH / 'program4.asm', 'r') as file:
#     program1 = file.read()

#     print(program1)

from M8085 import Parser, _STACK, Assembler, Processor, Register, Memory, Flag, Message
program1 = """
; ========================================================
; Bubble Sort Program for 10 numbers in memory (C050H)
; ========================================================

        LXI H, C050H      ; HL points to start of array
        MVI C, 0AH        ; Counter for 10 elements

; Initialize array (example values)
INIT_ARRAY:
        MVI A, 09H
        MOV M, A
        INX H
        MVI A, 02H
        MOV M, A
        INX H
        MVI A, 04H
        MOV M, A
        INX H
        MVI A, 06H
        MOV M, A
        INX H
        MVI A, 01H
        MOV M, A
        INX H
        MVI A, 08H
        MOV M, A
        INX H
        MVI A, 03H
        MOV M, A
        INX H
        MVI A, 05H
        MOV M, A
        INX H
        MVI A, 07H
        MOV M, A
        INX H
        MVI A, 00H
        MOV M, A

; --------------------------------------------------------
; Bubble Sort Routine
; --------------------------------------------------------
SORT:
        LXI H, C050H      ; HL points to start of array
        MVI D, 09H        ; Outer loop counter (n-1 passes)

OUTER_LOOP:
        LXI H, C050H      ; Reset HL for each pass
        MVI E, 09H        ; Inner loop counter (n-1 comparisons)

INNER_LOOP:
        MOV A, M          ; Load current element
        INX H
        CMP M             ; Compare with next element
        JC NO_SWAP
        MOV B, M          ; Swap
        MOV M, A
        DCX H
        MOV M, B
        INX H

NO_SWAP:
        DCR E
        JNZ INNER_LOOP

        DCR D
        JNZ OUTER_LOOP

HLT                     ; Halt processor

"""
parser = Parser(program1)
parsed_program1 = parser.parse()
if isinstance(parsed_program1,Message):
    print("Error:",parsed_program1.as_dict())
pc = Assembler()
pc.pass2()
print(_STACK)

process = Processor(program1)

print(process.execute())
print(Register().get_all())
# print(Flag().get_all())
print(Memory().get_used_addresses())