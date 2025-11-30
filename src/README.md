
## File Structure of Frontend (src/)
```
src/
├── features/                    # Feature-based modules
│   ├── notebook/                # Assembly notebook feature
│   │   ├── components/          # NotebookEditor, Cell, CellList, etc.
│   │   ├── hooks/               # useNotebook, useCellExecution
│   │   ├── outputs/             # All output renderers
│   │   └── index.js             # Barrel export
│   │
│   ├── processor/               # 8085 processor simulation
│   │   ├── components/          # ProcessorState
│   │   ├── stores/              # processorStore (Zustand)
│   │   └── index.js
│   │
│   ├── settings/                # App settings & API management
│   │   ├── components/          # APIKeyManager
│   │   ├── hooks/               # useHeader
│   │   ├── stores/              # settingsStore (Zustand)
│   │   └── index.js
│   │
│   └── index.js                 # Features barrel export
│
├── shared/                      # Reusable across features
│   ├── components/
│   │   ├── dialogs/             # ConfirmDialog, ExportDialog, ShortcutDialog
│   │   └── ui/                  # Header, CommandPalette, MobileTabBar
│   ├── hooks/                   # useKeyboardShortcuts, useConfirmDialog, etc.
│   ├── services/                # API, Groq, magicCommand, etc.
│   ├── utils/                   # notebookDB, documentationParser
│   └── index.js
│
├── pages/                       # Page-level components
│   ├── About/
│   ├── Home/
│   └── Report/
│
├── App.jsx                      # Root component
├── renderer.jsx                 # Entry point
├── constants.js                 # Global constants
└── *.css                        # Global styles
```