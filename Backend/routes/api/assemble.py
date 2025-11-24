from fastapi import APIRouter
from M8085 import Parser, Message, stack
from ..model import (
    AssembleRequest,
    AssembleSuccessResponse,
    AssembleErrorResponse,
    AssembleErrorDetails
)
from M8085 import Memory, Register, Flag
from M8085._memory import _FLAG, _REGISTER, Assembler

def assemble_8085_program(program):
    """Assemble the given 8085 assembly program."""
    try:
        Memory().reset()
        Register().reset()
        Flag().reset()
        Assembler().reset()
        parser = Parser(program)
        parse_result = parser.parse()

        if isinstance(parse_result, Message):
            return {
                "status": "error",
                "type": "parse_error",
                "details": AssembleErrorDetails(**parse_result.as_dict())
            }

        assembled_data = stack()
        labels = ["Address", "Label", "Instruction", "Opcode", "Cycles", "Operand"]

        return {
            "status": "success",
            "label": labels,
            "data": assembled_data
        }

    except Exception as e:
        return {
            "status": "error",
            "type": "assemble_error",
            "details": AssembleErrorDetails(
                error=True,
                message=str(e),
                details={}
            )
        }


router = APIRouter()

@router.post("/assemble")
async def assemble_program(request: AssembleRequest):
    result = assemble_8085_program(request.program)

    if result["status"] == "error":
        return AssembleErrorResponse(**result)

    return AssembleSuccessResponse(**result)
