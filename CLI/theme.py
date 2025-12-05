"""
CLI Theme & Color Palette
Hacker / cyberpunk aesthetic: neon greens, cyans, magentas on dark terminal.
Import `console` for styled output; use style names directly in markup.
"""

from rich.console import Console
from rich.theme import Theme
from rich.table import Table

# Color Palette (hacker / cyberpunk vibe)
_THEME = Theme({
    # Headers & titles
    "header":        "bold bright_green",
    "subheader":     "bold cyan",
    "title":         "bold magenta",

    # General text
    "intro":         "dim green",
    "text":          "bright_white",
    "muted":         "dim white",

    # Accent / highlight
    "accent":        "bold bright_cyan",
    "highlight":     "bold bright_magenta",

    # Status
    "success":       "bold bright_green",
    "warning":       "bold yellow",
    "error":         "bold bright_red",

    # Prompt
    "prompt":        "bold bright_green",

    # Tables
    "table.header":  "bold bright_cyan",
    "table.border":  "bright_green",
    "table.row":     "bright_white",
    "table.row.alt": "dim white",

    # Code / technical
    "code":          "bright_yellow on grey23",
    "address":       "bold bright_magenta",
    "value":         "bright_cyan",
    "instruction":   "bright_green",
    "label":         "bold yellow",
    "opcode":        "bright_magenta",

    # Decorative
    "border":        "bright_green",
    "line":          "dim green",
})

# Configured Console (use this everywhere)
console = Console(theme=_THEME)

# Style name shortcuts (for f-strings or programmatic use)
STYLE = {
    "header":        "header",
    "subheader":     "subheader",
    "title":         "title",
    "intro":         "intro",
    "text":          "text",
    "muted":         "muted",
    "accent":        "accent",
    "highlight":     "highlight",
    "success":       "success",
    "warning":       "warning",
    "error":         "error",
    "prompt":        "prompt",
    "table_header":  "table.header",
    "table_border":  "table.border",
    "table_row":     "table.row",
    "table_row_alt": "table.row.alt",
    "code":          "code",
    "address":       "address",
    "value":         "value",
    "instruction":   "instruction",
    "label":         "label",
    "opcode":        "opcode",
    "border":        "border",
    "line":          "line",
}

from rich.panel import Panel
from rich import box as _box
from rich.align import Align

def intro_panel() -> Panel:
    """Return a detailed intro panel describing the app and commands."""
    body = (
        "Welcome,\n\n"
        "You have access to a fully emulated Intel 8085 microprocessor.\n"
        "Write assembly, execute instructions, inspect registers, memory, and flags in real-time.\n\n"
        "Type [accent]help[/accent] for commands or [accent]help <cmd>[/accent] for details.\n\n"
        "Examples: [code]MOV A, B[/code]  [code]LXI H, 8000H[/code]  [code]HLT[/code]"
    )
    return Panel(
        Align.left(body),
        box=_box.DOUBLE_EDGE,
        border_style=STYLE["line"],
        padding=(1, 2),
        title="[subheader]Intel 8085 Simulator[/]",
        title_align="left",
    )

# Helper: create a styled table with hacker theme
def create_table(*headers: str, title: str = None) -> Table:
    """Return a Table pre-configured with hacker theme styles."""
    from rich.box import DOUBLE_EDGE

    table = Table(
        title=title,
        title_style=STYLE["title"],
        header_style=STYLE["table_header"],
        border_style=STYLE["table_border"],
        box=DOUBLE_EDGE,
        show_lines=False,
        padding=(0, 1),
    )
    for h in headers:
        table.add_column(h, justify="center", style=STYLE["text"])
    return table
