START:  LXI H, 3000H      ; Load starting address of data
MVI C, 0AH         ; Counter = 10 (10 bytes to add)
MVI A, 00H         ; Clear accumulator (for sum)
CALL ADD_LOOP      ; Call subroutine to add bytes
CALL STORE_RESULT  ; Store the result at 3050H
HLT                ; Stop execution

ADD_LOOP: 
MOV B, M           ; Load memory data into B
ADD B              ; Add B to accumulator
INX H              ; Move to next memory location
DCR C              ; Decrease counter
JNZ ADD_LOOP       ; Continue until counter = 0
RET                ; Return to main program

STORE_RESULT:
LXI H, 3050H       ; Load result memory address
MOV M, A           ; Store final sum
RET                ; Return to main program