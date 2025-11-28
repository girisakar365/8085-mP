from pathlib import Path
import yaml

from fastapi import APIRouter, HTTPException

from . import type_check as tc
from .. import Processor, TimingDiagram, Stack

router = APIRouter()

@router.post("/execute", response_model=tc.ExecuteSuccessResponse | tc.ExecuteErrorResponse)
async def execute(request: tc.Request):
    """
    Execute 8085 assembly code using the global simulator state.
    Returns structured JSON errors for frontend consumption.
    """
    result = Processor(request.code).as_dict()
    return result

@router.get("/timing/{instruction}", response_model=tc.TimingResponse)
async def timing_diagram(instruction: str):
    """
    Get timing diagram for a specific 8085 instruction.
    Returns structured timing data for frontend visualization.
    """
    timing_diagram = TimingDiagram()
    timing_data = timing_diagram.as_dict(instruction)
    if timing_data is None:
        raise HTTPException(status_code=404, detail=f"Timing diagram for instruction '{instruction}' not found")
    return timing_data

@router.post("/assemble", response_model=tc.AssembleSuccessResponse | tc.AssembleErrorResponse)
async def assemble(request: tc.Request):
    """
    Assemble 8085 assembly code into machine code.
    Returns structured JSON with assembly results or errors.
    """
    from .. import Parser, Assembler, Message

    result = Parser(request.code).parse()
    if isinstance(result, Message):
        return {
            'success' : False,
            'checkpoint': 'assemble/parse', 
            'details' : result.as_dict()
    }
    else:
        result = Assembler().pass2()
        if isinstance(result, Message):
            return {
                'success' : False,
                'checkpoint': 'assemble/pass2', 
                'details' : result.as_dict()
        }
        
        return Assembler().as_dict()

@router.post("/reset", response_model=tc.ResetResponse)
async def reset():
    """
    Reset all components to default values.
    Returns structured JSON with default processor state.
    """
    result = Stack()['RST5.5']()
    return result

@router.get("/docs/{instruction}", response_model=tc.DocumentationResponse)
async def docs(instruction: str):
    """
    Get documentation for a specific 8085 instruction.
    Returns structured JSON with instruction details.
    """
    file_path = Path(__file__).parent.parent / "docs.yml"
    with open(file_path, "r") as f:
        INSTRUCTION_DOCS = yaml.safe_load(f)

    normalized_instruction = instruction.upper()
    payload = INSTRUCTION_DOCS.get(normalized_instruction, f"Invalid Instruction {instruction}.")
    return {
        "instruction": normalized_instruction,
        "documentation": payload
    }