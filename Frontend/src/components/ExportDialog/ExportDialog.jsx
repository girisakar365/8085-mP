import { Download, FileText, X, Calendar, Hash } from 'lucide-react';
import { useState, useEffect } from 'react';
import './ExportDialog.css';

const EXPORT_FORMAT_VERSION = '1.0.0';

function ExportDialog({ isOpen, onClose, onConfirm, cells }) {
  const [filename, setFilename] = useState('');
  const [includeMetadata, setIncludeMetadata] = useState(true);

  useEffect(() => {
    if (isOpen) {
      const date = new Date().toISOString().split('T')[0];
      setFilename(`asm-session-${date}.json`);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;
      
      if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
      } else if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        handleExport();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, filename]);

  if (!isOpen) return null;

  const cellCount = cells?.length || 0;
  const codeCount = cells?.filter(c => c.type === 'code').length || 0;
  const markdownCount = cells?.filter(c => c.type === 'markdown').length || 0;

  const handleExport = () => {
    if (!filename.trim()) {
      return;
    }
    onConfirm(filename, includeMetadata);
  };

  return (
    <>
      <div className="export-overlay" onClick={onClose} />
      <div className="export-dialog">
        <div className="export-header">
          <div className="export-icon">
            <Download size={24} />
          </div>
          <h2>Export Session</h2>
          <button onClick={onClose} className="export-close" aria-label="Close">
            <X size={20} />
          </button>
        </div>
        
        <div className="export-content">
          <div className="export-summary">
            <div className="summary-item">
              <FileText size={16} />
              <span>{cellCount} cell{cellCount !== 1 ? 's' : ''}</span>
            </div>
            <div className="summary-item">
              <Hash size={16} />
              <span>{codeCount} code • {markdownCount} markdown</span>
            </div>
            <div className="summary-item">
              <Calendar size={16} />
              <span>{new Date().toLocaleString()}</span>
            </div>
          </div>

          <div className="export-field">
            <label htmlFor="export-filename">Filename</label>
            <input
              id="export-filename"
              type="text"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              placeholder="session-export.json"
              autoFocus
            />
          </div>

          <div className="export-options">
            <label className="export-checkbox">
              <input
                type="checkbox"
                checked={includeMetadata}
                onChange={(e) => setIncludeMetadata(e.target.checked)}
              />
              <span>Include metadata (timestamp, version)</span>
            </label>
          </div>

          <div className="export-info">
            <p>The session will be exported as a JSON file containing all your cells and their content.</p>
          </div>
        </div>
        
        <div className="export-footer">
          <button onClick={onClose} className="btn btn-secondary">
            Cancel
          </button>
          <button 
            onClick={handleExport} 
            className="btn btn-primary"
            disabled={!filename.trim()}
          >
            <Download size={16} />
            Export Session
          </button>
        </div>
        
        <div className="export-hint">
          <kbd>Esc</kbd> to cancel • <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to export
        </div>
      </div>
    </>
  );
}

export default ExportDialog;
