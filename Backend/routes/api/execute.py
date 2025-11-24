from fastapi import APIRouter
from M8085 import Processor, Message, Memory
from M8085._memory import _MEMORY, _REGISTER, _FLAG
from ..model import ExecuteRequest, ExecuteSuccessResponse, ExecuteErrorResponse

def get_execute_program(code: str) -> dict:
    """
    Execute 8085 assembly code and return structured JSON results.
    """
    try:
        processor = Processor(code)
        result = processor.execute()

        if isinstance(result, Message):
            return {
                "success": False,
                "error": result.as_dict()
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
