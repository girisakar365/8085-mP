from functools import wraps
from Backend.M8085._utils import encode, decode

def process_memory(func):
    """
    Validate memory address input before calling do_* handler.
    Wrapper signature matches cmd.Cmd do_* methods: (self, line: str)
    On validation failure calls self.response(msg) and returns None.
    """
    def validate_memory_token(tok: str):
        tok = tok.strip().upper()
        if not tok.endswith('H'):
            return f'Invalid address format {tok}. Missing "H".'
        if len(tok) != 5:
            return f'Invalid address {tok}. Expected 4 hex digits + "H".'
        val = decode(tok)
        if val is None:
            return f'Invalid hexadecimal address {tok}.'
        return val

    @wraps(func)
    def wrapper(self, line):
        if not isinstance(line, str) or not line.strip():
            self.response("No address provided. Provide address(es)")
            return None

        s = line.strip().upper()

        # Range
        if '-' in s:
            parts = [p.strip() for p in s.split('-', 1)]
            if len(parts) != 2 or not parts[0] or not parts[1]:
                self.response(f'Invalid range format: {line}. Use STARTH-ENDH.')
                return None
            start = validate_memory_token(parts[0])
            if isinstance(start, str):
                self.response(start)
                return None
            end = validate_memory_token(parts[1])
            if isinstance(end, str):
                self.response(end)
                return None
            if start > end:
                self.response(f'Invalid address range {line}. Start > End.')
                return None
            # call handler with original string (or choose to pass processed data)
            return func(self, [encode(addr, 4) for addr in range(start, end + 1)])

        # List
        if ',' in s:
            toks = [p.strip() for p in s.split(',') if p.strip()]
            if not toks:
                self.response(f'Invalid list format: {line}.')
                return None
            for tok in toks:
                v = validate_memory_token(tok)
                if isinstance(v, str):
                    self.response(v)
                    return None
            return func(self, toks)

        # Single address
        v = validate_memory_token(s)
        if isinstance(v, str):
            self.response(v)
            return None
        return func(self, s)

    return wrapper