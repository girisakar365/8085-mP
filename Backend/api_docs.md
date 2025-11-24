
# 8085 Asm Studio - API Documentation

## Overview
Backend API for the 8085 microprocessor simulator. All requests should be sent to `http://localhost:8000/api/`.

---

## Endpoints

### 1. **Health Check**
Check if the backend is running.

```
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "message": "8085 Asm Studio Backend is running."
}
```

---

### 2. **Assemble**
Convert 8085 assembly code to machine code.

```
POST /api/assemble
```

**Request Body:**
```json
{
  "program": "MVI A, 05\nADD B\nHLT"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "label": ["Address", "Label", "Instruction", "Opcode", "Cycles", "Operand"],
  "data": [
    ["0000", "", "MVI A, 05", "3E05", "7", "05"],
    ["0002", "", "ADD B", "80", "4", ""],
    ["0003", "", "HLT", "76", "7", ""]
  ]
}
```

**Error Response (400):**
```json
{
  "status": "error",
  "details": {
    "message": "Invalid instruction",
    "type": "parse_error"
  }
}
```

---

### 3. **Execute**
Run 8085 assembly code and get processor state after execution.

```
POST /api/execute
```

**Request Body:**
```json
{
  "code": "MVI A, 05\nMVI B, 03\nADD B\nHLT"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "newState": {
    "registers": {
      "A": "08",
      "B": "03",
      "C": "00",
      "D": "00",
      "E": "00",
      "H": "00",
      "L": "00"
    },
    "flags": {
      "Z": 0,
      "S": 0,
      "P": 1,
      "C": 0,
      "AC": 0
    },
    "memory": {
      "2000": "05",
      "2001": "03"
    }
  }
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": {
    "line": 1,
    "message": "Undefined label",
    "code": "JMP LOOP"
  }
}
```

---

### 4. **Reset**
Reset the simulator to default state (all registers, flags, and memory cleared).

```
POST /api/reset
```

**Response (200):**
```json
{
  "success": true,
  "message": "Components reset to default values",
  "defaultState": {
    "registers": {
      "A": "00",
      "B": "00",
      "C": "00",
      "D": "00",
      "E": "00",
      "H": "00",
      "L": "00"
    },
    "flags": {
      "Z": 0,
      "S": 0,
      "P": 0,
      "C": 0,
      "AC": 0
    },
    "memory": {}
  }
}
```

---

### 5. **Get Instruction Documentation**
Retrieve documentation for a specific 8085 instruction.

```
GET /api/docs/{instruction}
```

**Example:**
```
GET /api/docs/MVI
```

**Response (200):**
```json
{
  "instruction": "MVI",
  "documentation": "Move Immediate - Load an 8-bit number into a register or memory location. Format: MVI r,data or MVI M,data"
}
```

**Error Response (404):**
```json
{
  "detail": "Documentation not found for the given instruction."
}
```

---

### 6. **Get Instruction Timing Diagram**
Retrieve timing diagram for a specific 8085 instruction.

```
GET /api/timing/{instruction}
```

**Example:**
```
GET /api/timing/MVI
```

**Response (200):**
```json
{
  "instruction": "MVI",
  "format": "base64",
  "diagram": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA..."
}
```

**Error Response (404):**
```json
{
  "detail": "Timing diagram for instruction 'MVI' not found"
}
```

---

## Data Structures

### ProcessorState
Represents the current state of the processor.
```json
{
  "registers": {
    "A": "00",
    "B": "00",
    "C": "00",
    "D": "00",
    "E": "00",
    "H": "00",
    "L": "00"
  },
  "flags": {
    "Z": 0,
    "S": 0,
    "P": 0,
    "C": 0,
    "AC": 0
  },
  "memory": {
    "address": "value"
  }
}
```

**Registers:** A, B, C, D, E, H, L (8-bit values in hex)
**Flags:** 
- `Z` - Zero Flag
- `S` - Sign Flag
- `P` - Parity Flag
- `C` - Carry Flag
- `AC` - Auxiliary Carry Flag

---

## Error Handling

All error responses include:
- **HTTP Status Code** (400, 404, 500, etc.)
- **Error Details** in JSON format

Common status codes:
- `200` - Success
- `400` - Bad Request (syntax error, invalid input)
- `404` - Not Found (instruction not found)
- `500` - Server Error

---

## Usage Example (JavaScript/Fetch)

### Assemble Code
```javascript
const response = await fetch('http://localhost:8000/api/assemble', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ program: 'MVI A, 05\nHLT' })
});
const result = await response.json();
console.log(result);
```

### Execute Code
```javascript
const response = await fetch('http://localhost:8000/api/execute', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ code: 'MVI A, 05\nHLT' })
});
const result = await response.json();
console.log(result.newState);
```

### Get Documentation
```javascript
const response = await fetch('http://localhost:8000/api/docs/MVI');
const result = await response.json();
console.log(result.documentation);
```

### Get Timing Diagram
```javascript
const response = await fetch('http://localhost:8000/api/timing/MVI');
const result = await response.json();
console.log(result.diagram); // Base64-encoded PNG image
```

### Reset Simulator
```javascript
const response = await fetch('http://localhost:8000/api/reset', {
  method: 'POST'
});
const result = await response.json();
console.log(result.defaultState);
```

---

## CORS Configuration

The backend supports CORS from:
- `http://localhost:5173`
- `http://localhost:4173`
- `http://127.0.0.1:5173`
- `http://127.0.0.1:4173`

---

## Running the Backend

```bash
python -m Backend.main
# Server runs at http://localhost:8000
```

