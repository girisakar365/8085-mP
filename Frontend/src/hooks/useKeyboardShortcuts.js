import { useEffect } from 'react';

const SHORTCUTS = {
  COMMAND_PALETTE: { key: 'k' },
  COMMAND_PALETTE_ALT: { key: 'P' },
  SHORTCUTS_DIALOG: { key: '/' },
  SAVE: { key: 's' },
};

export function useKeyboardShortcuts({
  onCommandPalette,
  onShortcutsDialog,
  onSave,
}) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Command Palette: Ctrl+K or Ctrl+Shift+P
      if ((e.ctrlKey && e.key === SHORTCUTS.COMMAND_PALETTE.key) ||
          (e.ctrlKey && e.shiftKey && e.key === SHORTCUTS.COMMAND_PALETTE_ALT.key)) {
        e.preventDefault();
        onCommandPalette?.();
      }

      // Shortcuts Dialog: Ctrl+/
      if (e.ctrlKey && e.key === SHORTCUTS.SHORTCUTS_DIALOG.key) {
        e.preventDefault();
        onShortcutsDialog?.();
      }

      // Save: Ctrl+S
      if (e.ctrlKey && e.key === SHORTCUTS.SAVE.key) {
        e.preventDefault();
        onSave?.();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onCommandPalette, onShortcutsDialog, onSave]);
}