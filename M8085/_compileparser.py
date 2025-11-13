import re

class CompileParser:
    def __init__(self, code: str):
        self.raw_code = code
        self.cleaned_lines = []
        self.structure_dict = {}

    def _preprocess_code(self):
        """Clean and prepare the code for processing."""
        code = self.raw_code.upper()
        lines = [line.strip() for line in code.strip().split('\n') if line]
        clean_lines = []

        for line in lines:
            if ';' in line:
                line = line.split(';', 1)[0].strip()
            if line:
                clean_lines.append(line)

        if not clean_lines[0].split()[0].endswith(':'):
            clean_lines[0] = 'START: ' + clean_lines[0]

        self.cleaned_lines = clean_lines

    def _build_structure(self):
        """Create an empty dictionary for each label."""
        for line in self.cleaned_lines:
            tokens = line.split()
            if tokens and tokens[0].endswith(':'):
                label = tokens[0].rstrip(':')
                self.structure_dict[label] = []

    def _fill_structure(self):
        """Fill the structure with corresponding code lines."""
        keys = list(self.structure_dict.keys())

        for i, key in enumerate(keys):
            start_idx = None
            for idx, line in enumerate(self.cleaned_lines):
                if line.startswith(key + ':'):
                    start_idx = idx
                    break

            stop_words = ["HLT", "RST"] if i == 0 else ["RET"]

            for line in self.cleaned_lines[start_idx:]:
                if line.startswith(key + ':'):
                    line = line.split(':', 1)[1].strip()
                elif re.match(r'^([A-Z_][A-Z0-9_]*):\s*(.*)', line):
                    line = line.split(':', 1)[1].strip()
                if line:
                    self.structure_dict[key].append(line)
                if any(line.startswith(sw) for sw in stop_words):
                    break
        return self.structure_dict

    def get_structure(self):
        """Main method to get the structured code."""
        self._preprocess_code()
        self._build_structure()
        return self._fill_structure()


if __name__ == "__main__":
    test = '''
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
    processor = CompileParser(test)
    structure = processor.get_structure()
    print(structure)



