import yaml
from pathlib import Path
from fastapi import APIRouter, HTTPException
from ..model import DocumentationResponse

file_path = Path(__file__).parent.parent.parent.parent / "M8085" / "docs.yml"
with open(file_path, "r") as f:
    INSTRUCTION_DOCS = yaml.safe_load(f)

def get_instruction_document(instruction):
    normalized_instruction = instruction.upper()
    payload = INSTRUCTION_DOCS.get(normalized_instruction, f"Invalid Instruction {instruction}.")
    return {
        "instruction": normalized_instruction,
        "documentation": payload
    }
router = APIRouter()
@router.get("/docs/{instruction}", response_model=DocumentationResponse)
async def get_docs(instruction):
    docs = get_instruction_document(instruction)
    if docs is None:
        raise HTTPException(status_code=404, detail="Documentation not found for the given instruction.")
    return DocumentationResponse(**docs)
