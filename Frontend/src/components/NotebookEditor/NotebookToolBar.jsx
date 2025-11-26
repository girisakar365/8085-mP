import { Play, Plus, Trash2, RotateCcw } from 'lucide-react';
import './NotebookToolBar.css';

export default function NotebookToolBar({ 
  onRunAll, 
  onClearOutputs, 
  onClearAll, 
  onAddCell,
  isExecuting 
}) {
  return (
    <div className="notebook-toolbar">
      <div className="toolbar-group">
        <button 
          onClick={onRunAll} 
          className="btn btn-primary"
          disabled={isExecuting}
          title="Run All Cells (Ctrl+Shift+Enter)"
        >
          <Play size={16} />
          <span>Run All</span>
        </button>
        
        <button 
          onClick={onAddCell} 
          className="btn"
          title="Add Cell Below (B)"
        >
          <Plus size={16} />
          <span>Add Cell</span>
        </button>
      </div>

      <div className="toolbar-group">
        <button 
          onClick={onClearOutputs} 
          className="toolbar-btn"
          title="Clear All Outputs"
        >
          <RotateCcw size={16} />
          <span>Clear Outputs</span>
        </button>
        
        <button 
          onClick={onClearAll} 
          className="btn btn-danger"
          title="Clear All Cells"
        >
          <Trash2 size={16} />
          <span>Clear All</span>
        </button>
      </div>
    </div>
  );
}
