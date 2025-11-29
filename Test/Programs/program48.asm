; --------------------------------------------------------
; MAIN ROUTINE
; HL -> Starting address of array
; B  -> N - 1  (outer loop count)
; --------------------------------------------------------

SORT_OUTER:
        MOV C, B            ; Inner loop count = B
        CALL PASS           ; Perform one bubble pass
        DCR B               ; Decrement number of passes
        JNZ SORT_OUTER      ; Continue until B = 0
        HLT                 ; Finished


; --------------------------------------------------------
; PASS SUBROUTINE
; Performs one full bubble pass of C comparisons
; HL = pointer to current array start
; C  = number of comparisons in this pass
; --------------------------------------------------------

PASS:
        PUSH B              ; Save outer loop counter
        PUSH H              ; Save start pointer

PASS_LOOP:
        MOV A, M            ; A = element[i]
        INX H               ; HL -> element[i+1]
        CMP M               ; Compare A with M[i+1]
        JC NO_SWAP          ; If A < next, no swap

        ; -------- Perform swap ----------
        DCX H               ; Back to element[i]
        PUSH H              ; Save pointer of left element
        INX H               ; HL -> right element
        MOV D, M            ; D = right
        POP H               ; HL -> left
        MOV E, M            ; E = left
        CALL SWAP           ; Swap them

NO_SWAP:
        DCX H               ; Return HL to left element
        INX H               ; Move HL for next comparison
        DCR C
        JNZ PASS_LOOP

        POP H               ; Restore HL
        POP B               ; Restore B
        RET


; --------------------------------------------------------
; SWAP SUBROUTINE
; HL -> left element
; D = right element
; E = left element
; --------------------------------------------------------

SWAP:
        MOV M, D            ; left  = right
        INX H
        MOV M, E            ; right = left
        DCX H
        RET
