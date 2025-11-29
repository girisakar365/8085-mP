START:  LXI H,8000H    ; Load H-L pair with 2000H
        MVI C, 0AH      ; Initialize counter C with 10
        CALL INIT_VALUES; Call subroutine to initialize memory
        CALL SORT       ; Call subroutine to sort data
        HLT             ; Halt the processor

INIT_VALUES:            ; Subroutine to initialize memory locations
        LXI D, 9000H   ; Load D-E pair with source address 1000H
INIT_LOOP:              ; Loop to copy values
        MOV M, A        ; Move data from Accumulator to memory pointed by H-L
        INX H           ; Increment H-L pair (destination address)
        INX D           ; Increment D-E pair (source address)
        DCR C           ; Decrement counter C
        JNZ INIT_LOOP   ; Jump back to INIT_LOOP if counter is not zero
        RET             ; Return from subroutine

SORT:                   ; Subroutine to sort data using bubble sort
        MVI D, 09H      ; Initialize outer loop counter D with 9 (n-1 passes)
OUTER:  LXI H, 2000H    ; Point H-L to the start of the array for each pass
        MVI E, 09H      ; Initialize inner loop counter E with 9 (n-1 comparisons)
INNER:  MOV A, M        ; Load current element into Accumulator
        INX H           ; Point to the next element
        CMP M           ; Compare Accumulator with the next element
        JC SKIP         ; If A < M (no swap needed), jump to SKIP
        MOV B, M        ; Swap elements: Store M in B
        MOV M, A        ; Move A to M (current location)
        DCX H           ; Point back to the previous element
        MOV M, B        ; Move B (original next element) to M (previous location)
        INX H           ; Point back to the next element position for loop continuation
SKIP:   DCR E           ; Decrement inner loop counter
        JNZ INNER       ; Jump back to INNER if not zero
        DCR D           ; Decrement outer loop counter
        JNZ OUTER       ; Jump back to OUTER if not zero
        RET             ; Return from subroutine