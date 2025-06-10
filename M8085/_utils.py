from random import randbytes
from ._instruction import opcode
from prettytable import PrettyTable
import re

class Setup:
    def memory():
        memory = {}
        for i in range(65536):
            address = hex(i)[2:].upper()
            if len(address) < 4:
                bit = '0'*(4-len(address))
                address = bit + address
            memory[address + 'H'] = '00'
        
        return memory

    def port():
        port = {}
        for i in range(256):
            if len(hex(i)[2:]) == 1 :port['0' + hex(i)[2:].upper() + 'H'] = '0'
            else: port[hex(i)[2:].upper() + 'H'] = '0'
        
        return port

    def register():
        return {'A':'00','B':'00','C':'00','D':'00','E':'00','H':'00','L':'00','M':00,'PC':'0000H','SP':'0000H'}

    def flag():
        return {'S':0,'Z':0,'AC':0,'P':0,'C':0}
        
class Tool:
    TOKEN = None
    PARAM_RULE = {
            'MOV':(2,1,1),
            'MVI':(2,1,3),
            'LXI':(2,1,5),
            'LDA':(1,5),
            'STA':(1,5),
            'LDAX':(1,1),
            'STAX':(1,1),
            'LHLD':(1,5),
            'SHLD':(1,5),
            'XCHG':(0,0),
            'IN':(1,3),
            'OUT':(1,3),
            'ADD':(1,1),
            'ADI':(1,3),
            'ADC':(1,1),
            'SUB':(1,1),
            'SUI':(1,3),
            'SBB':(1,1),
            'SBI':(1,3),
            'INR':(1,1),
            'DCR':(1,1),
            'INX':(1,1),
            'DCX':(1,1),
            'DAD':(1,1),
            'DAA':None,
            'RRC':(0,0),
            'RAR':(0,0),
            'RLC':(0,0),
            'RAL':(0,0),
            'ANI':(1,3),
            'XRI':(1,3),
            'ORI':(1,3),
            'ANA':(1,1),
            'ORA':(1,1),
            'XRA':(1,1),
            'CMA':(0,0),
            'CMP':(1,1),
            'CPI':(1,3),
            'CMC':(0,0),
            'STC':(0,0),
            'PUSH':(1,1),
            'XTHL':(0,0),
            'PCHL':(0,0),
            'SPHL':(0,0),
            'JMP':(1,5),
            'JC':(1,5),
            'JZ':(1,5),
            'JPE':(1,5),
            'JPO':(1,5),
            'JP':(1,5),
            'JM':(1,5),
            'JNZ':(1,5),
            'JNC':(1,5),
            'HLT':(0,0),
            'RST5.5':(0,0),
        }

    def check_param(inst:str,arg:str):
        prompt = arg.upper().replace(' ', '').split(',')
        if inst in ['HLT','RST5.5'] and prompt[0] == '': return None

        elif Tool.PARAM_RULE[inst][0] == 0 and prompt[0] != '': return 'NoArgumentError'

        elif Tool.PARAM_RULE[inst][0] == 1:
            if len(prompt[0]) != Tool.PARAM_RULE[inst][1]: return 'SyntaxError'
            elif len(prompt[0]) == 0: return 'TypeError'
            elif len(prompt[0]) == 1 and prompt[0] not in Tool.TOKEN['register'].keys(): return 'RegisterError'
            elif len(prompt[0]) == 5 and prompt[0] not in Tool.TOKEN['memory'].keys(): return 'MemoryError'
            elif len(prompt[0]) == 3 and prompt[0] not in Tool.TOKEN['port'].keys(): return 'DataError'
            elif inst in ['INX','DCX','DAD'] and prompt[0] not in ['H','B','D']: return 'RpError'
            elif inst in ['LDAX', 'STAX'] and prompt[0] == "H": return 'RpNotAllowedError'
            elif inst in ['LDAX', 'STAX'] and prompt[0] not in ['B','D']: return 'RpError'
            else: return prompt[0]
        else:
            if arg.find(',') == -1: return 'CommaError' 
            elif any([len(prompt[0]) != Tool.PARAM_RULE[inst][1],
                  len(prompt[1]) != Tool.PARAM_RULE[inst][2]]): return 'SyntaxError'
            elif len(prompt[0]) == 0 or len(prompt[1]) == 0: return 'TypeError'
            else:
                if any(
                    [len(prompt[0]) == 1 and prompt[0] not in Tool.TOKEN['register'].keys(),
                     len(prompt[1]) == 1 and prompt[1] not in Tool.TOKEN['register'].keys()]
                ): return 'RegisterError'
                elif any(
                    [len(prompt[0]) == 1 and inst == 'LXI' and prompt[0] not in ['H','B','D'], 
                     len(prompt[1]) == 1 and inst == 'LXI' and prompt[1] not in ['H','B','D']
                    ]
                ): return 'RpError'
                elif any(
                    [len(prompt[0]) == 5 and prompt[0] not in Tool.TOKEN['memory'].keys(),
                     len(prompt[1]) == 5 and prompt[1] not in Tool.TOKEN['memory'].keys()]
                ): return 'MemoryError'
                elif len(prompt[1]) == 3 and prompt[1] not in Tool.TOKEN['port'].keys(): return 'DataError'
                else: return tuple(prompt)
    
    def rp(rp:str = 'H') -> str:
        if rp == 'B': return Tool.TOKEN["register"]['B'] + Tool.TOKEN["register"]['C'] + 'H'
        elif rp == 'D': return  Tool.TOKEN["register"]['D'] + Tool.TOKEN["register"]['E'] + 'H'
        else: return Tool.TOKEN["register"]['H'] + Tool.TOKEN["register"]['L'] + 'H'
    
    def check_parity(result:str):
        if bin(decode(result[:-1])).count('1') % 2 == 0:
            Tool.TOKEN['flag']['P'] = 1
        else:
            Tool.TOKEN['flag']['P'] = 0
        
    def check_zero(result:str):
        if decode(result[:-1]) == 0:
            Tool.TOKEN['flag']['Z'] = 1
        else:
            Tool.TOKEN['flag']['Z'] = 0
    
    def check_sign(result:str):
        if decode(result[:-1]) < 0:
            Tool.TOKEN['flag']['S'] = 1
        else:
            Tool.TOKEN['flag']['S'] = 0

class Memory:
    TOKEN = None

    history = {}
    exe_address = []

    def update_pc(inst:str):
        Memory.TOKEN['register']['PC'] = encode(decode(Memory.TOKEN['register']['PC']) + opcode[inst]['byte'],4)

    def store(bind:tuple):
        key = Memory.TOKEN['register']['PC']
        Memory.history[key] = bind
        Memory.exe_address.append(key)
    
    def fetch():
        key = Memory.TOKEN['register']['PC']
        return Memory.history[key]

    def placement(bind:tuple):
        inst, prompt = bind
        if any([i in opcode[inst] for i in ['H','B', 'D', 'A', 'C', 'E', 'L', 'M']]):
        
            key = prompt[0] if isinstance(prompt, tuple) else prompt

        else:
            if inst == 'MOV':
                key = ','.join(prompt)
            
            else:
                key = 'op'

        address = Memory.TOKEN['register']['PC']
        if opcode[inst]['byte'] == 3:
            if isinstance(prompt ,tuple):
                for i in opcode[inst][key], prompt[1][2:-1], prompt[1][:2]:
                    Memory.TOKEN['stack'][address] = i
                    address = encode(decode(address) + 1,4)
            else:
                for i in opcode[inst][key], prompt[2:-1], prompt[:2]:
                    Memory.TOKEN['stack'][address] = i
                    address = encode(decode(address) + 1,4)
            
        elif opcode[inst]['byte'] == 2:
            if isinstance(prompt ,tuple):
                parse = prompt[1] if len(prompt[1]) == 3 else prompt[0]
            else: parse = prompt
            for i in  opcode[inst][key], parse:
                Memory.TOKEN['stack'][address] = i
                address = encode(decode(address) + 1,4)

        elif opcode[inst]['byte'] == 1:
            Memory.TOKEN['stack'][address] = opcode[inst][key]
            address = encode(decode(address) + 1,4)
        

def get_token():
    return  {
                "memory":Setup.memory(),
                "stack":Setup.memory(),
                "register":Setup.register(),
                "flag":Setup.flag(),
                "port":Setup.port(),
            }

def decode(arg:str, base:int = 16):
    return int(arg.replace('H',''),base)

def encode(arg:int, bit:int=2):
    if bit == 2:
        if len(hex(arg)[2:].upper()) < 2:
            return '0' + hex(arg)[2:].upper() + 'H'

        return hex(arg)[2:].upper() + 'H'
    
    elif bit == 4:
        if len(hex(arg)[2:].upper()) < 4:
            return '0'*(4- len(hex(arg)[2:].upper())) + hex(arg)[2:].upper() + 'H'
        
        return hex(arg)[2:].upper() + 'H'

def _preprocess_code(code):
   
    lines = []
    original_line_map = {}
    line_number = 0
    for raw_line in code.strip().split('\n'):
        line_number += 1
        cleaned_line = raw_line.strip()
        if cleaned_line:
            original_line_map[len(lines)] = line_number
            lines.append(cleaned_line)
    return lines, original_line_map

def _identify_labels(instruction_lines, original_line_map):
    labels_in_order = []
    label_to_line_index = {}
    explicit_labels = set()
    label_defined_at_zero = False
    warnings = []

    for i, line in enumerate(instruction_lines):
        line_num = original_line_map[i]
        match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)', line)
        label = None
        if match:
            label = match.group(1).strip()
        else:
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
    default_start_label = "START"
    start_label_to_use = None
    needs_injection = not label_defined_at_zero and instruction_lines

    if needs_injection:
        if default_start_label in explicit_labels:
            counter = 1
            while f"START_{counter}" in explicit_labels:
                counter += 1
            start_label_to_use = f"START_{counter}"
        else:
            start_label_to_use = default_start_label
          
        labels_in_order.insert(0, start_label_to_use)
        label_to_line_index[start_label_to_use] = 0
    elif not labels_in_order and instruction_lines:
         start_label_to_use = default_start_label
         labels_in_order.append(start_label_to_use)
         label_to_line_index[start_label_to_use] = 0

    return start_label_to_use

def _find_end_markers(instruction_lines):
    end_marker_indices = {}
    has_any_end_marker = False
    warnings = []

    for i, line in enumerate(instruction_lines):
        instruction_part = line.split(';')[0].strip().upper()
        if instruction_part == 'RET' or instruction_part == 'HLT' or instruction_part == 'RST5':
            end_marker_indices[i] = instruction_part
            has_any_end_marker = True

    if not has_any_end_marker and instruction_lines:
        warnings.append("Warning: No 'RET', 'HLT', or 'RST5' instructions found. Code might not terminate as expected. Blocks assumed to end at file end.")
        if len(instruction_lines) > 0:
            end_marker_indices[len(instruction_lines) - 1] = "END"
    elif instruction_lines and sorted(end_marker_indices.keys())[-1] < len(instruction_lines) - 1:
         end_marker_indices[len(instruction_lines) - 1] = "END"

    sorted_end_indices = sorted(end_marker_indices.keys())
    return end_marker_indices, sorted_end_indices, warnings

def _map_labels_to_end(labels_in_order, label_to_line_index, sorted_end_indices, end_marker_indices, original_line_map, num_lines):
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
                end_type = end_marker_indices.get(end_idx, "UNKNOWN") 
                break

        if found_end_idx == -1:
             found_end_idx = num_lines - 1 if num_lines > 0 else 0
             end_type = "END"
             line_num = original_line_map.get(label_def_line_idx, 'N/A')
             warnings.append(f"Warning: Label '{label}' (line {line_num}) appears after the last detected terminator or none exists. Scope assumed to end of file.")

        label_to_end_info[label] = (found_end_idx, end_type)

    return label_to_end_info, warnings

def _clean_block_lines(block_lines_raw, all_known_labels):
    final_instructions = []
    for line in block_lines_raw:
        line_content = line
        match = re.match(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)', line_content)
        if match:
            potential_label = match.group(1)
            if potential_label in all_known_labels:
                line_content = match.group(2)

        instruction_part = line_content.split(';', 1)[0]
        cleaned_instruction = instruction_part.strip()

        if cleaned_instruction:
             final_instructions.append(cleaned_instruction)

    return final_instructions

def _build_result_dict(labels_in_order, label_to_line_index, label_to_end_info, instruction_lines, all_known_labels, original_line_map, default_start_label, explicit_labels):
    result = {}
    processed_labels_final = set()
    warnings = []

    for label in labels_in_order:
        if label in processed_labels_final: continue
        processed_labels_final.add(label)

        label_def_line_idx = label_to_line_index[label]
        end_line_idx, end_type = label_to_end_info.get(label, (-1, "UNKNOWN"))
        if end_line_idx == -1:
            line_num = original_line_map.get(label_def_line_idx, 'N/A')
            warnings.append(f"Error: Could not determine end scope for label '{label}' (line {line_num}). Skipping.")
            result[label]=[]
            continue

        is_primary_label_def_standalone = False
        is_injected_start = (label == default_start_label and label not in explicit_labels)
        if not is_injected_start:
            line_content_at_def = instruction_lines[label_def_line_idx]
            match_standalone = re.match(r'^\s*' + re.escape(label) + r':\s*(?:;.*)?$', line_content_at_def)
            if match_standalone:
                is_primary_label_def_standalone = True

        start_line_idx_for_block = label_def_line_idx + 1 if is_primary_label_def_standalone else label_def_line_idx

        if start_line_idx_for_block > end_line_idx:
            result[label] = []
            if end_type != "UNKNOWN" and label_def_line_idx <= end_line_idx :
                 line_num = original_line_map.get(label_def_line_idx, 'N/A')
                 warnings.append(f"Info: Label '{label}' (line {line_num}) appears to define an empty block (no instructions before scope end).")
        else:
            block_lines_raw = instruction_lines[start_line_idx_for_block : end_line_idx + 1]
            if block_lines_raw:
                last_line_in_block = block_lines_raw[-1]
                last_instr = last_line_in_block.split(';')[0].strip().upper()
                if last_instr != 'RET' and last_instr != 'HLT' and last_instr !='RST5' and end_type != 'END':
                    line_num = original_line_map.get(label_def_line_idx, 'N/A')
                    end_line_num = original_line_map.get(end_line_idx, 'N/A')
                    warnings.append(f"Warning: Block for label '{label}' (line {line_num}) seems incomplete. Scope ends at line {end_line_num} with '{last_instr}', not RET or HLT.")
            elif end_type != "UNKNOWN" and end_type != "END":
                 line_num = original_line_map.get(label_def_line_idx, 'N/A')
                 end_line_num = original_line_map.get(end_line_idx, 'N/A')
                 warnings.append(f"Info: Label '{label}' (line {line_num}) defines an empty block ending at line {end_line_num}.")
            final_instructions = _clean_block_lines(
                block_lines_raw,
                all_known_labels,
            )
            result[label] = final_instructions

    return result, warnings

def get_dict(code):
    all_warnings = []
    instruction_lines, original_line_map = _preprocess_code(code)
    if not instruction_lines:
        all_warnings.append("Input code is empty or contains only whitespace.")
        return {}, all_warnings

    labels_in_order, label_to_line_index, explicit_labels, label_defined_at_zero, label_warnings = _identify_labels(instruction_lines, original_line_map)
    all_warnings.extend(label_warnings)

    default_start_label = _inject_default_start_label(
        labels_in_order, label_to_line_index, explicit_labels, label_defined_at_zero, instruction_lines
    )
    # all_warnings.extend(start_label_warnings)

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
