import re

# --- Helper Functions ---

def _preprocess_code(code):
    """Splits code into cleaned lines and maps processed index to original line number."""
    lines = []
    original_line_map = {}
    line_number = 0
    for raw_line in code.strip().split('\n'):
        line_number += 1
        # Keep initial strip minimal to preserve inline label+instruction structure
        cleaned_line = raw_line.strip()
        if cleaned_line:
            original_line_map[len(lines)] = line_number
            lines.append(cleaned_line)
    return lines, original_line_map

def _identify_labels(instruction_lines, original_line_map):
    """Identifies labels, checks for duplicates, and records their order/position."""
    labels_in_order = []
    label_to_line_index = {}
    explicit_labels = set()
    label_defined_at_zero = False
    warnings = []

    for i, line in enumerate(instruction_lines):
        line_num = original_line_map[i]
        # Match label at the start of the line
        match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)', line)
        label = None
        if match:
            label = match.group(1).strip()
        else:
            # Check for label potentially ending the line (standalone)
            is_standalone_check = line.endswith(':') and not re.search(r':.*:', line)
            if is_standalone_check:
                label = line[:-1].strip()

        if label:
            if label in label_to_line_index:
                first_def_line = original_line_map.get(label_to_line_index[label], 'N/A')
                warnings.append(f"Warning: Label '{label}' redefined on line {line_num} (first definition on line {first_def_line}). Using first definition for structure.")
            else:
                labels_in_order.append(label)
                label_to_line_index[label] = i
                explicit_labels.add(label)
                if i == 0:
                    label_defined_at_zero = True

    return labels_in_order, label_to_line_index, explicit_labels, label_defined_at_zero, warnings

def _inject_default_start_label(labels_in_order, label_to_line_index, explicit_labels, label_defined_at_zero, instruction_lines):
    """Adds a 'START' label if code doesn't start with one."""
    default_start_label = "START"
    start_label_to_use = None
    warnings = []
    needs_injection = not label_defined_at_zero and instruction_lines

    if needs_injection:
        if default_start_label in explicit_labels:
            counter = 1
            while f"START_{counter}" in explicit_labels:
                counter += 1
            start_label_to_use = f"START_{counter}"
            warnings.append(f"Info: Code does not start with a label. Using auto-generated label '{start_label_to_use}' as entry point.")
        else:
            start_label_to_use = default_start_label
            warnings.append("Info: Code does not start with a label. Using 'START' as entry point.")

        labels_in_order.insert(0, start_label_to_use)
        label_to_line_index[start_label_to_use] = 0 # Conceptually defined at line 0
    elif not labels_in_order and instruction_lines:
         start_label_to_use = default_start_label
         warnings.append("Warning: No labels found or defined in the code. Treating entire code as one block under 'START'.")
         labels_in_order.append(start_label_to_use)
         label_to_line_index[start_label_to_use] = 0

    return start_label_to_use, warnings

def _find_end_markers(instruction_lines):
    """Finds RET/HLT instructions and handles cases with no terminators."""
    end_marker_indices = {}
    has_any_end_marker = False
    warnings = []

    for i, line in enumerate(instruction_lines):
        # Check only instruction part for RET/HLT
        instruction_part = line.split(';')[0].strip().upper()
        if instruction_part == 'RET' or instruction_part == 'HLT':
            end_marker_indices[i] = instruction_part
            has_any_end_marker = True

    if not has_any_end_marker and instruction_lines:
        warnings.append("Warning: No 'RET' or 'HLT' instructions found. Code might not terminate as expected. Blocks assumed to end at file end.")
        # Mark last line as EOF only if needed for structure determination
        if len(instruction_lines) > 0:
            end_marker_indices[len(instruction_lines) - 1] = "EOF"
    elif instruction_lines and sorted(end_marker_indices.keys())[-1] < len(instruction_lines) - 1:
        # End marker exists, but not on the last line. Add EOF for blocks after last RET/HLT
         end_marker_indices[len(instruction_lines) - 1] = "EOF"

    sorted_end_indices = sorted(end_marker_indices.keys())
    return end_marker_indices, sorted_end_indices, warnings

def _map_labels_to_end(labels_in_order, label_to_line_index, sorted_end_indices, end_marker_indices, original_line_map, num_lines):
    """Determines the scope-ending RET/HLT/EOF index for each label."""
    label_to_end_info = {}
    processed_labels = set()
    warnings = []

    for label in labels_in_order:
        if label in processed_labels: continue
        processed_labels.add(label)

        label_def_line_idx = label_to_line_index[label]
        found_end_idx = -1
        end_type = "UNKNOWN"

        for end_idx in sorted_end_indices:
            if end_idx >= label_def_line_idx:
                found_end_idx = end_idx
                end_type = end_marker_indices.get(end_idx, "UNKNOWN") # Use .get for safety
                break

        if found_end_idx == -1:
             found_end_idx = num_lines - 1 if num_lines > 0 else 0
             end_type = "EOF"
             line_num = original_line_map.get(label_def_line_idx, 'N/A')
             warnings.append(f"Warning: Label '{label}' (line {line_num}) appears after the last detected terminator or none exists. Scope assumed to end of file.")

        label_to_end_info[label] = (found_end_idx, end_type)

    return label_to_end_info, warnings

def _clean_block_lines(block_lines_raw, all_known_labels):
    """Cleans label prefixes, removes comments, and trims whitespace."""
    final_instructions = []
    for line in block_lines_raw:
        line_content = line # Start with the raw line from the block

        # 1. Strip potential label prefix IF it's a known label
        match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)', line_content)
        if match:
            potential_label = match.group(1)
            if potential_label in all_known_labels:
                # It's a known label, take only the part after the colon
                line_content = match.group(2)
        # If it wasn't a known label prefix, line_content remains the original line

        # 2. Remove comments (split by ';' and take the first part)
        instruction_part = line_content.split(';', 1)[0]

        # 3. Trim whitespace
        cleaned_instruction = instruction_part.strip()

        # 4. Add to list only if it's not empty after cleaning
        if cleaned_instruction:
             final_instructions.append(cleaned_instruction)

    return final_instructions

def _build_result_dict(labels_in_order, label_to_line_index, label_to_end_info, instruction_lines, all_known_labels, original_line_map, default_start_label, explicit_labels):
    """Builds the final dictionary, slicing blocks, cleaning lines, and validating."""
    result = {}
    processed_labels_final = set()
    warnings = []

    for label in labels_in_order:
        if label in processed_labels_final: continue
        processed_labels_final.add(label)

        label_def_line_idx = label_to_line_index[label]
        end_line_idx, end_type = label_to_end_info.get(label, (-1, "UNKNOWN")) # Use .get for safety

        if end_line_idx == -1: # Should not happen if mapping is correct, but safety check
            line_num = original_line_map.get(label_def_line_idx, 'N/A')
            warnings.append(f"Error: Could not determine end scope for label '{label}' (line {line_num}). Skipping.")
            result[label]=[]
            continue

        is_primary_label_def_standalone = False
        is_injected_start = (label == default_start_label and label not in explicit_labels)
        if not is_injected_start:
            # Check if the label definition line itself contains only the label + optional comment
            line_content_at_def = instruction_lines[label_def_line_idx]
            match_standalone = re.match(r'^\s*' + re.escape(label) + r':\s*(?:;.*)?$', line_content_at_def)
            if match_standalone:
                is_primary_label_def_standalone = True

        start_line_idx_for_block = label_def_line_idx + 1 if is_primary_label_def_standalone else label_def_line_idx

        if start_line_idx_for_block > end_line_idx:
            result[label] = []
            # Add info only if not already covered by other warnings
            if end_type != "UNKNOWN" and label_def_line_idx <= end_line_idx :
                 line_num = original_line_map.get(label_def_line_idx, 'N/A')
                 warnings.append(f"Info: Label '{label}' (line {line_num}) appears to define an empty block (no instructions before scope end).")
        else:
            block_lines_raw = instruction_lines[start_line_idx_for_block : end_line_idx + 1]

            # Validation Check (Optional but good)
            if block_lines_raw:
                last_line_in_block = block_lines_raw[-1]
                last_instr = last_line_in_block.split(';')[0].strip().upper()
                if last_instr != 'RET' and last_instr != 'HLT' and end_type != 'EOF':
                    line_num = original_line_map.get(label_def_line_idx, 'N/A')
                    end_line_num = original_line_map.get(end_line_idx, 'N/A')
                    warnings.append(f"Warning: Block for label '{label}' (line {line_num}) seems incomplete. Scope ends at line {end_line_num} with '{last_instr}', not RET or HLT.")
            elif end_type != "UNKNOWN" and end_type != "EOF": # Avoid warning for empty block if it's just EOF
                 line_num = original_line_map.get(label_def_line_idx, 'N/A')
                 end_line_num = original_line_map.get(end_line_idx, 'N/A')
                 warnings.append(f"Info: Label '{label}' (line {line_num}) defines an empty block ending at line {end_line_num}.")

            # Clean lines within the block (removes labels, comments, trims whitespace)
            final_instructions = _clean_block_lines(
                block_lines_raw,
                all_known_labels,
            )
            result[label] = final_instructions

    return result, warnings


# --- Main Function ---

def get_dict(code):
    """
    Processes 8085 assembly code, organizing instructions by labels.
    Includes error/warning checks. Output lists contain only instructions,
    cleaned of labels, comments, and excess whitespace.

    Args:
        code: String containing assembly code.

    Returns:
        A tuple: (dictionary, warnings)
        - dictionary: {label: [cleaned_instruction_strings]}.
        - warnings: List of strings describing potential issues.
    """
    all_warnings = []
    instruction_lines, original_line_map = _preprocess_code(code)
    if not instruction_lines:
        all_warnings.append("Input code is empty or contains only whitespace.")
        return {}, all_warnings

    labels_in_order, label_to_line_index, explicit_labels, label_defined_at_zero, label_warnings = \
        _identify_labels(instruction_lines, original_line_map)
    all_warnings.extend(label_warnings)

    default_start_label, start_label_warnings = _inject_default_start_label(
        labels_in_order, label_to_line_index, explicit_labels, label_defined_at_zero, instruction_lines
    )
    all_warnings.extend(start_label_warnings)

    if not labels_in_order:
         all_warnings.append("Critical: Could not determine any labels or entry point.")
         return {}, all_warnings

    all_known_labels = set(labels_in_order)

    end_marker_indices, sorted_end_indices, marker_warnings = _find_end_markers(instruction_lines)
    all_warnings.extend(marker_warnings)

    label_to_end_info, map_warnings = _map_labels_to_end(
        labels_in_order, label_to_line_index, sorted_end_indices, end_marker_indices, original_line_map, len(instruction_lines)
    )
    all_warnings.extend(map_warnings)

    result_dict, build_warnings = _build_result_dict(
        labels_in_order, label_to_line_index, label_to_end_info, instruction_lines,
        all_known_labels, original_line_map, default_start_label, explicit_labels
    )
    all_warnings.extend(build_warnings)

    final_warnings = []
    seen_warnings = set()
    for w in all_warnings:
        if w not in seen_warnings:
            final_warnings.append(w)
            seen_warnings.add(w)


    return result_dict, final_warnings


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

    test2 = '''LXI H, 2000H    ; Start without Label
        MVI C, 0AH      ;
        CALL INIT_VALUES;
        CALL SORT       ;
        IN_LOOP:        ; This label seems misplaced in the main flow
        LDAX D          ;
        MOV M, A        ;
        INX H           ;
        INX D           ;
        DCR C           ;
        JNZ IN_LOOP   ; Should this jump be here? Or part of INIT_VALUES?
        MOV M, A        ; Unclear purpose after loop
        INX H           ;
        INX D           ;
        HLT             ; Halt

INIT_VALUES:
        LXI D, 1200H;
INIT_LOOP:              ; This label is inside INIT_VALUES
        LDAX D          ;
        MOV M, A        ;
        INX H           ;
        INX D           ;
        DCR C           ;
        JNZ INIT_LOOP   ; Jump within INIT_VALUES
        RET ;

SORT:
        MVI D, 09H      ;
OUTER:  LXI H, 2000H    ;
        MVI E, 09H      ;
INNER:  MOV A, M        ;
        INX H           ;
        CMP M           ;
        JC SKIP         ;
        MOV B, M        ;
        MOV M, A        ;
        DCX H           ;
        MOV M, B        ;
        INX H           ;
SKIP:   DCR E           ;
        JNZ INNER       ;
        DCR D           ;
        JNZ OUTER       ;
        RET;
        '''
print(type(test1))
print(get_dict(test1)) 
get_dict(test1)

'''
({'START': ['LXI H, 2000H', 'MVI C, 0AH', 'CALL INIT_VALUES', 'CALL SORT', 'HLT'], 'INIT_VALUES': ['LXI D, 1000H', 'LDAX D', 'MOV M, A', 'INX H', 'INX D', 'DCR C', 'JNZ INIT_LOOP', 'RET'], 'INIT_LOOP': ['LDAX D', 'MOV M, A', 'INX H', 'INX D', 'DCR C', 'JNZ INIT_LOOP', 'RET'], 'SORT': ['MVI D, 09H', 'LXI H, 2000H', 'MVI E, 09H', 'MOV A, M', 'INX H', 'CMP M', 'JC SKIP', 'MOV B, M', 'MOV M, A', 'DCX H', 'MOV M, B', 'INX H', 'DCR E', 'JNZ INNER', 'DCR D', 'JNZ OUTER', 'RET'], 'OUTER': ['LXI H, 2000H', 'MVI E, 09H', 'MOV A, M', 'INX H', 'CMP M', 'JC SKIP', 'MOV B, M', 'MOV M, A', 'DCX H', 'MOV M, B', 'INX H', 'DCR E', 'JNZ INNER', 'DCR D', 'JNZ OUTER', 'RET'], 'INNER': ['MOV A, M', 'INX H', 'CMP M', 'JC SKIP', 'MOV B, M', 'MOV M, A', 'DCX H', 'MOV M, B', 'INX H', 'DCR E', 'JNZ INNER', 'DCR D', 'JNZ OUTER', 'RET'], 'SKIP': ['DCR E', 'JNZ INNER', 'DCR D', 'JNZ OUTER', 'RET']}, []) 
__
this is the response i get from the get_dict and i want you to execute the program as:
LXI H, 2000H 
MVI C, 0AH
CALL INIT_VALUES ; here call with init so we go to the init block and execute
LXI D, 1000H, 
LDAX D,
MOV M, A, 
INX H, 
INX D, 
DCR C, 
JNZ INIT_LOOP, ; here jump instruction is present so according to the branch_instruction on execution we should get the label for true condition if true then we execute the init_loop block and if false then we go to the next instruction
RET  here return so we go back to the block where this instruction was called from and continue executing the next instruction
CALL SORT ; here call with sort so we go to the sort block and execute
MVI D, 09H', 
'LXI H, 2000H', 
'MVI E, 09H', 
'MOV A, M', 
'INX H', 
'CMP M', 
'JC SKIP', 
'MOV B, M', 
'MOV M, A', 
'DCX H', 
'MOV M, B', 
'INX H', 
'DCR E', 
'JNZ INNER', 
'DCR D', 
'JNZ OUTER', 
'RET
and so on accordingly

--

'''


