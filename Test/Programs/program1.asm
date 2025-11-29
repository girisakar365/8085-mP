; ----------------------------------------------------
; STEP 1: Insert array values 9, 2, 4, 6, 1 into C050–C054
; ----------------------------------------------------

    LXI H, C050H        ; HL = C050 (start of array)

    MVI A, 09H
    MOV M, A            ; C050 = 9
    INX H

    MVI A, 02H
    MOV M, A            ; C051 = 2
    INX H

    MVI A, 04H
    MOV M, A            ; C052 = 4
    INX H

    MVI A, 06H
    MOV M, A            ; C053 = 6
    INX H

    MVI A, 01H
    MOV M, A            ; C054 = 1


; ----------------------------------------------------
; STEP 2: Min–Max algorithm (20 elements originally)
; Modified to 5 elements for your array
; ----------------------------------------------------

    MVI C, 05H          ; Array size = 5
    LXI H, C050H        ; HL points to first element

    MOV B, M            ; B = largest so far
    MOV D, M            ; D = smallest so far

    INX H               ; Move to next element
    DCR C               ; 1 element processed, now C = 4

READ:
    MOV A, M            ; A = current element

    CMP B               ; Compare with largest
    JNC LARGEST         ; If A > B then update largest

    CMP D               ; Compare with smallest
    JC SMALLEST         ; If A < D then update smallest

    JMP SKIP

LARGEST:
    MOV B, M            ; Update largest
    JMP SKIP

SMALLEST:
    MOV D, M            ; Update smallest

SKIP:
    INX H               ; Move to next element
    DCR C               ; decrease count
    JNZ READ            ; Loop until done


; ----------------------------------------------------
; STEP 3: Store results: smallest → C070, largest → C071
; ----------------------------------------------------

    MOV A, D            ; Smallest value
    STA C070H

    MOV A, B            ; Largest value
    STA C071H

    HLT
