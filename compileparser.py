import re

def preprocess_code(code):
    code = code.upper()
    lines = [line.strip() for line in code.strip().split('\n') if line]
    clean_lines = []
    for line in lines:
        if ';' in line:
            line = line.split(';', 1)[0].strip()
        if line:
            clean_lines.append(line)
    if not clean_lines[0].split()[0].endswith(':'):
        clean_lines[0] = 'START: ' + clean_lines[0]
    return clean_lines

def structure(lines):
    structure = {}
    for line in lines:
        tokens = line.split()
        if tokens and tokens[0].endswith(':'):
            label = tokens[0].rstrip(':')
            structure[label] = []
    return structure

def fill_structure(clean_lines, structure):
    keys = list(structure.keys())

    for i, key in enumerate(keys):
        start_idx = None
        for idx, line in enumerate(clean_lines):
            if line.startswith(key + ':'):
                start_idx = idx
                break
        
        stop_words = ["RET"]
        if i == 0:
            stop_words = ["HLT", "RST"]

        for line in clean_lines[start_idx:]:
            if line.startswith(key + ':'):
                line = line.split(':', 1)[1].strip()
            if re.match(r'^([A-Z_][A-Z0-9_]*):\s*(.*)', line):
                line = line.split(':', 1)[1].strip()
            if line:
                structure[key].append(line)
            if any(line.startswith(sw) for sw in stop_words):
                break
    return structure


def get_dict(code):
    lines = preprocess_code(code)
    final_dict = structure(lines)
    return fill_structure(lines, final_dict)



# --- Test Cases ---
if __name__ == '__main__':

    test1 = '''
            START:  LXI H, 2000H    ; Load H-L pair with 2000H
                    MVI C, 0AH      ; Initialize counter C with 10
                    CALL INIT_VALUES; Call subroutine to initialize memory
                    CALL SORT       ; Call subroutine to sort data
                    HLT             ; Halt the processor

            INIT_VALUES:            ; Subroutine to initialize memory locations
                    LXI D, 1000H   ; Load D-E pair with source address 1000H
            INIT_LOOP:              ; Loop to copy values
                    LDAX D          ; Load Accumulator from address in D-E
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
            '''

#     test2 = '''LXI H, 2000H    ; Start without Label
#         MVI C, 0AH      ;
#         CALL INIT_VALUES;
#         CALL SORT       ;
#         IN_LOOP:        ; This label seems misplaced in the main flow
#         LDAX D          ;
#         MOV M, A        ;
#         INX H           ;
#         INX D           ;
#         DCR C           ;
#         JNZ IN_LOOP   ; Should this jump be here? Or part of INIT_VALUES?
#         MOV M, A        ; Unclear purpose after loop
#         INX H           ;
#         INX D           ;
#         HLT             ; Halt

# INIT_VALUES:
#         LXI D, 1200H;
# INIT_LOOP:              ; This label is inside INIT_VALUES
#         LDAX D          ;
#         MOV M, A        ;
#         INX H           ;
#         INX D           ;
#         DCR C           ;
#         JNZ INIT_LOOP   ; Jump within INIT_VALUES
#         RET ;

# SORT:
#         MVI D, 09H      ;
# OUTER:  LXI H, 2000H    ;
#         MVI E, 09H      ;
# INNER:  MOV A, M        ;
#         INX H           ;
#         CMP M           ;
#         JC SKIP         ;
#         MOV B, M        ;
#         MOV M, A        ;
#         DCX H           ;
#         MOV M, B        ;
#         INX H           ;
# SKIP:   DCR E           ;
#         JNZ INNER       ;
#         DCR D           ;
#         JNZ OUTER       ;
#         RET;
#         '''

    result = get_dict(test1)
    print(result)