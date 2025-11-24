import base64
import io
import matplotlib.pyplot as plt
from fastapi import APIRouter, HTTPException
from M8085._utils import INSTRUCTION
from ..model import TimingResponse

def generate_timing_diagram(instruction):
    """Generate timing diagram as base64-encoded PNG."""
    normalized = instruction.upper()
    if normalized not in INSTRUCTION:
        return None

    try:
        from M8085._timing import TimingDiagram
        fig = TimingDiagram().get_table(normalized)
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', pad_inches=0.05, dpi=100)
        img_buffer.seek(0)

        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        plt.close(fig)
        img_buffer.close()

        return {
            "instruction": normalized,
            "format": "base64",
            "diagram": f"data:image/png;base64,{img_base64}",
        }
    except Exception:
        return None

router = APIRouter()
@router.get("/timing/{instruction}", response_model=TimingResponse)
async def get_timing_diagram(instruction: str):
    """Get timing diagram for a specific 8085 instruction."""
    timing_data = generate_timing_diagram(instruction)
    if timing_data is None:
        raise HTTPException(status_code=404, detail=f"Timing diagram for instruction '{instruction}' not found")
    return TimingResponse(**timing_data)