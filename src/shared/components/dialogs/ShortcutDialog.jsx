import { X } from 'lucide-react';
import { useEffect } from 'react';
import { useShortcutsDialogOpen, useSettingsActions } from '../../../features/settings/stores/settingsStore';
import './ShortcutDialog.css';

const SHORTCUTS = {
  COMMAND_PALETTE: { key: 'k' },
  SHORTCUTS_DIALOG: { key: '/' },
  RUN_CELL: { key: 'Enter', shift: true },
  RUN_CELL_STAY: { key: 'Enter', ctrl: true },
  RUN_ALL: { key: 'Enter', ctrl: true, shift: true },
  ADD_CELL_BELOW: { key: 'b' },
  DELETE_CELL: { key: 'd', repeat: 2 },
  INDENT: { key: 'Tab' },
  SAVE: { key: 's', ctrl: true },
};

function ShortcutsDialog() {
  const shortcutsDialogOpen = useShortcutsDialogOpen();
  const { closeShortcutsDialog } = useSettingsActions();

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && shortcutsDialogOpen) {
        closeShortcutsDialog();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [shortcutsDialogOpen, closeShortcutsDialog]);

  if (!shortcutsDialogOpen) return null;

  const shortcuts = [
    { 
      category: 'Global', 
      items: [
        { 
          keys: ['Ctrl', 'K'], 
          description: 'Open Command Palette',
          config: SHORTCUTS.COMMAND_PALETTE
        },
        { 
          keys: ['Ctrl', '/'], 
          description: 'View Keyboard Shortcuts',
          config: SHORTCUTS.SHORTCUTS_DIALOG
        },
      ]
    },
    { 
      category: 'Cell Operations (Command Mode)', 
      items: [
        { 
          keys: ['Shift', 'Enter'], 
          description: 'Run Cell and Select Below',
          config: SHORTCUTS.RUN_CELL
        },
        { 
          keys: ['Ctrl', 'Enter'], 
          description: 'Run Cell and Stay',
          config: SHORTCUTS.RUN_CELL_STAY
        },
        { 
          keys: ['Ctrl', 'Shift', 'Enter'], 
          description: 'Run All Cells',
          config: SHORTCUTS.RUN_ALL
        },
        { 
          keys: ['B'], 
          description: 'Add Cell Below (Command Mode)',
          config: SHORTCUTS.ADD_CELL_BELOW
        },
        { 
          keys: ['A'], 
          description: 'Add Cell Above (Command Mode)',
        },
        { 
          keys: ['D', 'D'], 
          description: 'Delete Cell (press D twice in Command Mode)',
          config: SHORTCUTS.DELETE_CELL
        },
        { 
          keys: ['↑'], 
          description: 'Select Cell Above (Command Mode)',
        },
        { 
          keys: ['↓'], 
          description: 'Select Cell Below (Command Mode)',
        },
        { 
          keys: ['Enter'], 
          description: 'Enter Edit Mode',
        },
        { 
          keys: ['Esc'], 
          description: 'Exit Edit Mode (Command Mode)',
        },
      ]
    },
    { 
      category: 'Editor (Edit Mode)', 
      items: [
        { 
          keys: ['Tab'], 
          description: 'Indent (4 spaces)',
          config: SHORTCUTS.INDENT
        },
        { 
          keys: ['Shift', 'Tab'], 
          description: 'Unindent',
        },
        { 
          keys: ['Ctrl', 'S'], 
          description: 'Export Session',
          config: SHORTCUTS.SAVE
        },
      ]
    },
  ];

  return (
    <>
      <div className="shortcuts-overlay" onClick={closeShortcutsDialog} />
      <div className="shortcuts-dialog">
        <div className="shortcuts-header">
          <h2>Keyboard Shortcuts</h2>
          <button onClick={closeShortcutsDialog} className="shortcuts-close" aria-label="Close">
            <X size={20} />
          </button>
        </div>
        
        <div className="shortcuts-content">
          {shortcuts.map((section, idx) => (
            <div key={idx} className="shortcuts-section">
              <h3>{section.category}</h3>
              <div className="shortcuts-list">
                {section.items.map((item, itemIdx) => (
                  <div key={itemIdx} className="shortcut-item">
                    <div className="shortcut-keys">
                      {item.keys.map((key, keyIdx) => (
                        <span key={keyIdx}>
                          <kbd>{key}</kbd>
                          {keyIdx < item.keys.length - 1 && <span className="plus">+</span>}
                        </span>
                      ))}
                    </div>
                    <div className="shortcut-description">{item.description}</div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
        
        <div className="shortcuts-footer">
          <p>Press <kbd>Esc</kbd> to close</p>
        </div>
      </div>
    </>
  );
}

export default ShortcutsDialog;
