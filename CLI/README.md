# CLI — 8085 Microprocessor Simulator

Purpose
-------
The `CLI` folder contains a lightweight command-line interface for the 8085 Microprocessor Simulator. It is the testing paltform as well as the first stable release of the simulator.

Quick start
-----------
Prerequisites:
- Python 3.12+ (recommended)
- Project dependencies in the repository's `Backend/requirements.txt`

Run the CLI:

```bash
python -m CLI
```

What it provides
----------------
- Interactive prompt with commands to: load/execute code, view registers, inspect memory ranges, view flags, and assemble code.
- A themed output layer (`CLI/theme.py`) that centralises colours and table styles.
- Input validation helpers and decorators in `CLI/decorators.py` to keep command handlers robust.

Files of interest
-----------------
- `__main__.py` — main CLI implementation and command handlers.
- `decorators.py` — input validation (memory parsing / guards).
- `theme.py` — colours, styled panels and `create_table()` helper.

Notes for contributors
----------------------
Keep CLI output concise and accessible. Use `console` from `CLI/theme.py` for all prints so style changes remain centralised.

License & author
----------------
Follow the repository [LICENSE](../LICENSE) and [contribution guidelines](../CONTRIBUTING.md) in the project root.
