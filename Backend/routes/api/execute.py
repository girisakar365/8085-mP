from fastapi import APIRouter
from M8085 import Processor, Message, Memory
from M8085._memory import _MEMORY, _REGISTER, _FLAG, Assembler
from ..model import ExecuteRequest, ExecuteSuccessResponse, ExecuteErrorResponse, ExecuteErrorDetails

def get_execute_program(code):
    """
    Execute 8085 assembly code and return structured JSON results.
    """
    try:
        Assembler().reset() 
        processor = Processor(code)
        result = processor.execute()

        if isinstance(result, Message):
            error_dict = result.as_dict()
            details = error_dict.get("details", {})
            error_details = ExecuteErrorDetails(
                type="execution_error",
                instruction=details.get("instruction"),
                tag=details.get("tag"),
                position=details.get("position"),
                line=details.get("line"),
                hint=details.get("hint"),
                message=error_dict.get("message"),
            )
            return {
                "success": False,
                "error": error_details
            }

        memory_dict = {addr: _MEMORY[addr] for addr in Memory().get_used_addresses()}

        return {
            "success": True,
            "newState": {
                "registers": _REGISTER.copy(),
                "flags": _FLAG.copy(),
                "memory": memory_dict
            }
        }

    except Exception as e:
        first_line = code.splitlines()[0] if code else ""
        return {
            "success": False,
            "error": {
                "type": "execution_error",
                "instruction": None,
                "tag": None,
                "position": 1,
                "line": first_line,
                "hint": None,
                "message": str(e)
            }
        }

router = APIRouter()

@router.post("/execute")
async def execute_program(request: ExecuteRequest):
    """
    Execute 8085 assembly code using the global simulator state.
    Returns structured JSON errors for frontend consumption.
    """
    result = get_execute_program(request.code)

    if result["success"]:
        return ExecuteSuccessResponse(**result)
    return ExecuteErrorResponse(**result)
