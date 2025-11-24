from fastapi import APIRouter
from M8085 import Memory, Register, Flag
from M8085._memory import _FLAG, _REGISTER
from ..model import ResetSuccessResponse, ResetErrorResponse

def reset_state():
    """Reset all components to default values."""
    try:
        Memory().reset()
        Register().reset()
        Flag().reset()
        
        default_state = {
            "registers": _REGISTER.copy(),
            "flags": _FLAG.copy(),
            "memory": {}
        }
        
        return {
            "success": True,
            "message": "Components reset to default values",
            "defaultState": default_state
        }
    except Exception as e:
        return {"success": False, "message": f"Failed to reset components: {str(e)}"}

router = APIRouter()
@router.post("/reset")
async def reset_simulator():
    """Reset all components to default values."""
    result = reset_state()
    if result["success"]:
        return ResetSuccessResponse(**result)
    else:
        return ResetErrorResponse(**result)