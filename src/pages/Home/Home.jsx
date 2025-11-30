import { useState, useEffect } from "react";
import NotebookEditor from "../../features/notebook/components/NotebookEditor";
import ProcessorState from "../../features/processor/components/ProcessorState";
import CommandPalette from "../../shared/components/ui/CommandPalette";
import ShortcutsDialog from "../../shared/components/dialogs/ShortcutDialog";
import APIKeyManager from "../../features/settings/components/APIKeyManager";
import ConfirmDialog from "../../shared/components/dialogs/ConfirmDialog";
import ExportDialog from "../../shared/components/dialogs/ExportDialog";
import MobileTabBar from "../../shared/components/ui/MobileTabBar";
import Header from "../../shared/components/ui/Header";
import AboutDialog from "../About/AboutDialog";
import ReportDialog from "../Report/ReportDialog";
import {
  useSettingsActions,
  useGroqKeyDialogOpen,
  useAboutDialogOpen,
  useReportDialogOpen,
} from "../../features/settings/stores/settingsStore";
import useNotebook from "../../features/notebook/hooks/useNotebook";
import { useConfirmDialog } from "../../shared/hooks/useConfirmDialog";
import { useKeyboardShortcuts } from "../../shared/hooks/useKeyboardShortcuts";
import { useSidebarResize } from "../../shared/hooks/useSidebarResize";
import "./Home.css";

export default function Home() {
  const [showExportDialog, setShowExportDialog] = useState(false);
  const [mobileActiveTab, setMobileActiveTab] = useState("editor");

  const {
    toggleCommandPalette,
    toggleShortcutsDialog,
    closeGroqKeyDialog,
    openAboutDialog,
    closeAboutDialog,
    openReportDialog,
    closeReportDialog,
  } = useSettingsActions();
  const groqKeyDialogOpen = useGroqKeyDialogOpen();
  const aboutDialogOpen = useAboutDialogOpen();
  const reportDialogOpen = useReportDialogOpen();

  const { dialogState, showConfirm, closeDialog } = useConfirmDialog();
  const { sidebarWidth, isResizing, handleMouseDown } = useSidebarResize();

  const {
    cells,
    activeCellId,
    isExecuting,
    addCell,
    updateCell,
    deleteCell,
    executeCell,
    executeAllCells,
    clearAllOutputs,
    clearAll,
    importCells,
    setActiveCellId,
  } = useNotebook();

  // Global keyboard shortcuts
  useKeyboardShortcuts({
    onCommandPalette: toggleCommandPalette,
    onShortcutsDialog: toggleShortcutsDialog,
    onSave: () => setShowExportDialog(true),
  });

  useEffect(() => {
    if (!activeCellId && cells.length > 0) {
      setActiveCellId(cells[0].id);
    }
  }, [activeCellId, cells, setActiveCellId]);

  const handleClearSession = async () => {
    const confirmed = await showConfirm({
      title: "Clear Entire Session",
      message:
        "Are you sure you want to clear the entire session? This will delete all cells and outputs. This action cannot be undone.",
      confirmText: "Clear Session",
      cancelText: "Cancel",
      variant: "danger",
    });

    if (confirmed) {
      clearAll();
    }
  };

  const handleExportSession = () => {
    setShowExportDialog(true);
  };

  const handleExportConfirm = async (filename, includeMetadata) => {
    try {
      const exportData = {
        cells: cells.map((cell) => ({
          type: cell.type,
          content: cell.content,
        })),
      };

      if (includeMetadata) {
        exportData.version = "1.0.0";
        exportData.timestamp = new Date().toISOString();
        exportData.appName = "asm studio";
      }

      const jsonString = JSON.stringify(exportData, null, 2);
      const blob = new Blob([jsonString], { type: "application/json" });
      const url = URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = filename.endsWith(".json") ? filename : `${filename}.json`;

      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      setShowExportDialog(false);
    } catch (error) {
      setShowExportDialog(false);
      await showConfirm({
        title: "Export Failed",
        message: `Failed to export session: ${error.message}`,
        confirmText: "OK",
        cancelText: "",
        variant: "danger",
      });
    }
  };

  const handleImportSession = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json";
    input.onchange = async (e) => {
      try {
        const file = e.target.files[0];
        if (!file) return;

        const text = await file.text();
        const data = JSON.parse(text);

        if (!data.cells || !Array.isArray(data.cells)) {
          await showConfirm({
            title: "Import Failed",
            message: "Invalid session file format: missing cells array",
            confirmText: "OK",
            cancelText: "",
            variant: "warning",
          });
          return;
        }

        if (data.cells.length === 0) {
          await showConfirm({
            title: "Import Failed",
            message: "The session file contains no cells",
            confirmText: "OK",
            cancelText: "",
            variant: "warning",
          });
          return;
        }

        const confirmed = await showConfirm({
          title: "Import Session",
          message: `Import ${data.cells.length} cell(s) from "${file.name}"?\n\nThis will replace your current session.`,
          confirmText: "Import",
          cancelText: "Cancel",
          variant: "warning",
        });

        if (!confirmed) {
          return;
        }

        importCells(data.cells);

        await showConfirm({
          title: "Import Successful",
          message: `Session imported successfully! Loaded ${data.cells.length} cell(s).`,
          confirmText: "OK",
          cancelText: "",
          variant: "warning",
        });
      } catch (error) {
        if (error.name === "SyntaxError") {
          await showConfirm({
            title: "Import Failed",
            message: "Failed to import session: Invalid JSON file",
            confirmText: "OK",
            cancelText: "",
            variant: "danger",
          });
        } else {
          await showConfirm({
            title: "Import Failed",
            message: `Failed to import session: ${error.message}`,
            confirmText: "OK",
            cancelText: "",
            variant: "danger",
          });
        }
      }
    };
    input.click();
  };

  return (
    <div className="home-container">
      <Header onAbout={openAboutDialog} onReport={openReportDialog} />
      <div className="home-content">
        {/* Notebook Editor - Left Side */}
        <div
          className={`notebook-panel ${mobileActiveTab === "editor" ? "mobile-active" : "mobile-hidden"}`}
          id="editor-panel"
          role="tabpanel"
          aria-labelledby="editor-tab"
        >
          <NotebookEditor
            cells={cells}
            activeCellId={activeCellId}
            isExecuting={isExecuting}
            onAddCell={addCell}
            onUpdateCell={updateCell}
            onDeleteCell={deleteCell}
            onExecuteCell={executeCell}
            onExecuteAllCells={executeAllCells}
            onClearAllOutputs={clearAllOutputs}
            onClearAll={handleClearSession}
            onSetActiveCellId={setActiveCellId}
          />
        </div>

        {/* Resize Handle */}
        <div
          className="resize-handle"
          onMouseDown={handleMouseDown}
          style={{ cursor: isResizing ? "col-resize" : "col-resize" }}
        />

        {/* Processor State - Right Side */}
        <div
          className={`processor-panel ${mobileActiveTab === "processor" ? "mobile-active" : "mobile-hidden"}`}
          style={{ width: `${sidebarWidth}px` }}
          id="processor-panel"
          role="tabpanel"
          aria-labelledby="processor-tab"
        >
          <ProcessorState />
        </div>
      </div>

      {/* Mobile Tab Bar */}
      <MobileTabBar
        activeTab={mobileActiveTab}
        onTabChange={setMobileActiveTab}
      />

      {/* Global Components */}
      <CommandPalette
        onClearSession={handleClearSession}
        onExportSession={handleExportSession}
        onImportSession={handleImportSession}
      />
      <ShortcutsDialog />
      <APIKeyManager
        isOpen={groqKeyDialogOpen}
        onClose={closeGroqKeyDialog}
      />
      <ConfirmDialog
        isOpen={dialogState.isOpen}
        onClose={dialogState.onClose || closeDialog}
        onConfirm={dialogState.onConfirm || closeDialog}
        title={dialogState.title}
        message={dialogState.message}
        confirmText={dialogState.confirmText}
        cancelText={dialogState.cancelText}
        variant={dialogState.variant}
      />
      <ExportDialog
        isOpen={showExportDialog}
        onClose={() => setShowExportDialog(false)}
        onConfirm={handleExportConfirm}
        cells={cells}
      />
      <AboutDialog isOpen={aboutDialogOpen} onClose={closeAboutDialog} />
      <ReportDialog isOpen={reportDialogOpen} onClose={closeReportDialog} />
    </div>
  );
}
