from pydantic import BaseModel
from typing import List, Any, Dict, Optional

# Global models for type checking
class Request(BaseModel):
    """Request model for execution endpoint."""
    code: str

class ErrorDetails(BaseModel):
    """Structured error details for execution runtime or parser errors."""
    instruction: Optional[str] = None
    tag: Optional[str] = None
    position: Optional[str] = None  
    line: Optional[str] = None
    hint: Optional[str] = None
    message: str

class ProcessorState(BaseModel):
    """Processor state structure."""
    registers: Dict[str, str]
    flags: Dict[str, int]
    memory: Dict[str, str]

# Models for API requests and responses
class AssembleSuccessResponse(BaseModel):
    status: str
    checkpoint: Optional[str] = None
    label: List[str]
    data: List[Any]

class AssembleErrorResponse(BaseModel):
    status: str
    checkpoint: Optional[str] = None
    details: ErrorDetails


class DocumentationResponse(BaseModel):
    """Response model for instruction documentation."""
    instruction: str
    documentation: str

class ExecuteSuccessResponse(BaseModel):
    """Response model for successful execution."""
    success: bool
    checkpoint: Optional[str] = None
    newState: ProcessorState

class ExecuteErrorResponse(BaseModel):
    """Response model for execution errors."""
    success: bool
    checkpoint: Optional[str] = None
    error: ErrorDetails

class ResetResponse(BaseModel):
    """Response model for successful CPU reset."""
    success: bool
    checkpoint: Optional[str] = None
    message: str
    defaultState: ProcessorState

class TimingResponse(BaseModel):
    """Response model for instruction timing diagram."""
    instruction: str
    format: str
    diagram: str
