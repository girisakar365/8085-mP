import { useState, useEffect, useRef } from 'react';
import NotebookToolBar from './NotebookToolBar';
import CellList from './CellList';
import { useSettingsActions } from '../../settings/stores/settingsStore';
import './NotebookEditor.css';

const CELL_TYPES = {
  CODE: 'code',
  MARKDOWN: 'markdown',
};

export default function NotebookEditor({
  cells,
  activeCellId,
  isExecuting,
  onAddCell,
  onUpdateCell,
  onDeleteCell,
  onExecuteCell,
  onExecuteAllCells,
  onClearAllOutputs,
  onClearAll,
  onSetActiveCellId,
}) {
  const [deleteKeyCount, setDeleteKeyCount] = useState(0);
  const deleteTimerRef = useRef(null);
  
  const { openGroqKeyDialog } = useSettingsActions();

  useEffect(() => {
    if (activeCellId) {
      const activeCell = document.querySelector(`[data-cell-id="${activeCellId}"]`);
      if (activeCell) {
        activeCell.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  }, [activeCellId]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      const hasOpenDialog = document.querySelector('.command-palette, .shortcuts-dialog, .api-key-dialog');
      if (hasOpenDialog) return;

      const activeElement = document.activeElement;
      const isInEditMode = activeElement && activeElement.tagName === 'TEXTAREA';
      if (isInEditMode) return;

      const activeCellIndex = cells.findIndex(c => c.id === activeCellId);
      if (activeCellIndex === -1 && cells.length > 0) {
        onSetActiveCellId(cells[0].id);
        return;
      }

      if (e.key === 'b' && !e.ctrlKey && !e.shiftKey && !e.altKey && !e.metaKey) {
        e.preventDefault();
        onAddCell(CELL_TYPES.CODE, activeCellIndex);
        return;
      }

      if (e.key === 'a' && !e.ctrlKey && !e.shiftKey && !e.altKey && !e.metaKey) {
        e.preventDefault();
        onAddCell(CELL_TYPES.CODE, activeCellIndex - 1);
        return;
      }

      if (e.key === 'd' && !e.ctrlKey && !e.shiftKey && !e.altKey && !e.metaKey) {
        e.preventDefault();
        
        setDeleteKeyCount(prev => {
          const newCount = prev + 1;
          
          if (newCount === 2) {
            if (activeCellId && cells.length > 1) {
              onDeleteCell(activeCellId);
            }
            return 0;
          }
          
          if (deleteTimerRef.current) {
            clearTimeout(deleteTimerRef.current);
          }
          deleteTimerRef.current = setTimeout(() => {
            setDeleteKeyCount(0);
          }, 1000);
          
          return newCount;
        });
        return;
      }

      if (e.key === 'ArrowUp' && !e.ctrlKey && !e.shiftKey) {
        e.preventDefault();
        if (activeCellIndex > 0) {
          onSetActiveCellId(cells[activeCellIndex - 1].id);
        }
        return;
      }

      if (e.key === 'ArrowDown' && !e.ctrlKey && !e.shiftKey) {
        e.preventDefault();
        if (activeCellIndex < cells.length - 1) {
          onSetActiveCellId(cells[activeCellIndex + 1].id);
        }
        return;
      }

      if (e.key === 'Enter' && !e.ctrlKey && !e.shiftKey && !e.metaKey) {
        e.preventDefault();
        const activeCell = document.querySelector(`[data-cell-id="${activeCellId}"] textarea`);
        if (activeCell) {
          activeCell.focus();
          activeCell.setSelectionRange(activeCell.value.length, activeCell.value.length);
        }
        return;
      }

      if (e.key === 'Enter' && e.shiftKey && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        if (activeCellId) {
          onExecuteCell(activeCellId);
          if (activeCellIndex < cells.length - 1) {
            onSetActiveCellId(cells[activeCellIndex + 1].id);
          } else {
            onAddCell(CELL_TYPES.CODE, activeCellIndex);
          }
        }
        return;
      }

      if (e.key === 'Enter' && e.ctrlKey && !e.shiftKey) {
        e.preventDefault();
        if (activeCellId) {
          onExecuteCell(activeCellId);
        }
        return;
      }

      if (e.key === 'Enter' && e.ctrlKey && e.shiftKey) {
        e.preventDefault();
        onExecuteAllCells();
        return;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      if (deleteTimerRef.current) {
        clearTimeout(deleteTimerRef.current);
      }
    };
  }, [cells, activeCellId, onAddCell, onDeleteCell, onExecuteCell, onExecuteAllCells, onSetActiveCellId]);

  const handleRunAll = () => {
    onExecuteAllCells();
  };

  const handleClearOutputs = () => {
    onClearAllOutputs();
  };

  const handleClearAll = () => {
    onClearAll();
  };

  const handleAddCell = (type = CELL_TYPES.CODE, index = -1) => {
    onAddCell(type, index);
  };

  const handleCellActivate = (cellId) => {
    onSetActiveCellId(cellId);
  };

  const handleCellUpdate = (cellId, updates) => {
    onUpdateCell(cellId, updates);
  };

  const handleCellExecute = (cellId) => {
    onExecuteCell(cellId);
  };

  const handleCellDelete = (cellId) => {
    onDeleteCell(cellId);
  };

  const handleOpenAIKey = () => {
    openGroqKeyDialog();
  };

  return (
    <div className="notebook-editor">
      <NotebookToolBar
        onRunAll={handleRunAll}
        onClearOutputs={handleClearOutputs}
        onClearAll={handleClearAll}
        onAddCell={() => handleAddCell()}
        isExecuting={isExecuting}
      />
      
      <div className="notebook-content">
        <CellList
          cells={cells}
          activeCellId={activeCellId}
          onCellActivate={handleCellActivate}
          onCellUpdate={handleCellUpdate}
          onCellExecute={handleCellExecute}
          onCellDelete={handleCellDelete}
          onAddCell={handleAddCell}
          onOpenAIKey={handleOpenAIKey}
        />
      </div>
    </div>
  );
}
