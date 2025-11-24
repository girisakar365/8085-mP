from pydantic import BaseModel
from typing import List, Any, Dict, Optional

class ProcessorState(BaseModel):
    """Processor state structure."""
    registers: Dict[str, Any]
    flags: Dict[str, int]
    memory: Dict[str, Any]

class DocumentationResponse(BaseModel):
    """Response model for instruction documentation."""
    instruction: str
    documentation: str

class TimingResponse(BaseModel):
    """Response model for instruction timing diagram."""
    instruction: str
    format: str
    diagram: str

class AssembleRequest(BaseModel):
    program: str


class AssembleSuccessResponse(BaseModel):
    status: str
    label: List[str]
    data: List[Any]


class AssembleErrorDetails(BaseModel):
    error: bool
    message: str
    details: Dict[str, Optional[Any]]


class AssembleErrorResponse(BaseModel):
    status: str
    type: Optional[str] = None
    details: AssembleErrorDetails

class ResetSuccessResponse(BaseModel):
    """Response model for successful CPU reset."""
    success: bool
    message: str
    defaultState: ProcessorState

class ResetErrorResponse(BaseModel):
    """Response model for CPU reset errors."""
    success: bool
    message: str

class ExecuteRequest(BaseModel):
    """Request model for execution endpoint."""
    code: str

class ExecuteErrorDetails(BaseModel):
    """Structured error details for execution runtime or parser errors."""
    type: Optional[str] = None
    instruction: Optional[str] = None
    tag: Optional[str] = None
    position: Optional[int] = None
    line: Optional[str] = None
    hint: Optional[str] = None
    message: str

class ExecuteSuccessResponse(BaseModel):
    """Response model for successful execution."""
    success: bool
    newState: ProcessorState

class ExecuteErrorResponse(BaseModel):
    """Response model for execution errors."""
    success: bool
    error: ExecuteErrorDetails
