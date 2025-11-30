# Backend - 8085 Simulator Engine

This directory contains the Python backend for ASM Studio, including the core 8085 simulator engine and REST API.

## Structure

```
Backend/
├── M8085/                      # Core simulator engine
│   ├── __init__.py             # Package initialization
│   ├── __main__.py             # CLI entry point
│   ├── _base.py                # Base processor class
│   ├── _arithmetic.py          # Arithmetic instructions (ADD, SUB, INR, DCR, etc.)
│   ├── _branch.py              # Branch instructions (JMP, CALL, RET, etc.)
│   ├── _data.py                # Data transfer instructions (MOV, MVI, LXI, etc.)
│   ├── _logical.py             # Logical instructions (ANA, ORA, XRA, CMA, etc.)
│   ├── _memory.py              # Memory operations (FLAG, REGISTER, MEMORY.)
│   ├── _parser.py              # Assembly language parser
│   ├── _peripheral.py          # I/O instructions (IN, OUT)
│   ├── _stack.py               # Stack instructions (PUSH, POP, XTHL, etc.)
│   ├── _timing.py              # Timing/control instructions (NOP, HLT, etc.)
│   ├── _utils.py               # Utility functions
│   ├── logs.py                 # Logging configuration
│   ├── commands_property.yml   # Instruction properties
│   ├── docs.yml                # Instruction documentation
│   └── api/                    # REST API
│       ├── main.py             # API routes
│       └── model.py            # Pydantic models
│
├── Server/                     # FastAPI server
│   └── __main__.py             # Server entry point
│
└── requirements.txt            # Python dependencies
```

## Setup

### Scripted Setup

```bash
# Linux/macOS
chmod +x Scripts/dev.sh
./Scripts/dev.sh
# Windows
.\Scripts\dev.bat
```

### Manual Setup
```bash
cd Backend
python3 -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
python -m Server
```

The API will be available at `http://127.185.243.18:8085`.

## API Documentation

Once running, access the interactive documentation:

- Swagger UI: `http://127.185.243.18:8085/docs`
- ReDoc: `http://127.185.243.18:8085/redoc`

## Testing

Tests are located in the `Test/` directory at the project root.
