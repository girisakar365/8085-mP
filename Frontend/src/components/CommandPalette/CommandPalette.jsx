import { useState, useEffect, useRef } from "react";
import {
  Search,
  Trash2,
  FileText,
  Moon,
  Sun,
  Download,
  Upload,
  Keyboard,
} from "lucide-react";
import {
  useSettingsActions,
  useCommandPaletteOpen,
  useTheme,
} from "../../stores/settingsStore";
import { useProcessorActions } from "../../stores/processorStore";
import "./CommandPalette.css";
import { DESIGN_TOKENS } from "../../constants";


function CommandPalette({ onClearSession, onExportSession, onImportSession }) {
  const [query, setQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef(null);

  const commandPaletteOpen = useCommandPaletteOpen();
  const theme = useTheme();
  const { closeCommandPalette, toggleTheme, openShortcutsDialog } =
    useSettingsActions();
  const { resetState: resetProcessorState } = useProcessorActions();

  const commands = [
    {
      id: "view-shortcuts",
      name: "View Shortcuts",
      icon: Keyboard,
      action: () => {
        closeCommandPalette();
        openShortcutsDialog();
      },
    },
    {
      id: "clear-session",
      name: "Clear Session",
      icon: Trash2,
      action: () => {
        closeCommandPalette();
        if (onClearSession) onClearSession();
      },
    },
    {
      id: "export-session",
      name: "Export Session",
      icon: Download,
      action: () => {
        closeCommandPalette();
        if (onExportSession) onExportSession();
      },
    },
    {
      id: "import-session",
      name: "Import Session",
      icon: Upload,
      action: () => {
        closeCommandPalette();
        if (onImportSession) onImportSession();
      },
    },
    {
      id: "toggle-theme",
      name: `Toggle Theme (Current: ${theme})`,
      icon: theme === DESIGN_TOKENS.COLORS.DARK ? Moon : Sun,
      action: () => {
        toggleTheme();
        closeCommandPalette();
      },
    },
    {
      id: "reset-processor",
      name: "Reset Processor State",
      icon: FileText,
      action: () => {
        resetProcessorState();
        closeCommandPalette();
      },
    },
  ];

  const filteredCommands = commands.filter((cmd) =>
    cmd.name.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    if (commandPaletteOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [commandPaletteOpen]);

  useEffect(() => {
    setSelectedIndex(0);
  }, [query]);

  const handleKeyDown = (e) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) =>
        prev < filteredCommands.length - 1 ? prev + 1 : prev
      );
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (filteredCommands[selectedIndex]) {
        executeCommand(filteredCommands[selectedIndex]);
      }
    } else if (e.key === "Escape") {
      closeCommandPalette();
    }
  };

  const executeCommand = (command) => {
    command.action();
    setQuery("");
  };

  if (!commandPaletteOpen) return null;

  return (
    <>
      <div className="command-palette-overlay" onClick={closeCommandPalette} />
      <div className="command-palette">
        <div className="command-palette-header">
          <Search size={20} />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a command or search..."
            className="command-palette-input"
          />
        </div>

        <div className="command-palette-results">
          {filteredCommands.length > 0 ? (
            filteredCommands.map((command, index) => {
              const Icon = command.icon;
              return (
                <div
                  key={command.id}
                  className={`command-item ${index === selectedIndex ? "selected" : ""}`}
                  onClick={() => executeCommand(command)}
                  onMouseEnter={() => setSelectedIndex(index)}
                >
                  <Icon size={18} />
                  <span className="command-name">{command.name}</span>
                </div>
              );
            })
          ) : (
            <div className="command-empty">No commands found</div>
          )}
        </div>

        <div className="command-palette-footer">
          <span>↑↓ Navigate</span>
          <span>↵ Select</span>
          <span>Esc Close</span>
        </div>
      </div>
    </>
  );
}

export default CommandPalette;
