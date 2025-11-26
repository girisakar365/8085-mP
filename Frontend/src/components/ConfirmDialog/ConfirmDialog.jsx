import { AlertTriangle, X } from 'lucide-react';
import { useEffect } from 'react';
import './ConfirmDialog.css';

function ConfirmDialog({ 
  isOpen, 
  onClose, 
  onConfirm, 
  title = 'Confirm Action',
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'danger' 
}) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!isOpen) return;
      
      if (e.key === 'Escape') {
        e.preventDefault();
        onClose();
      } else if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        onConfirm();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose, onConfirm]);

  if (!isOpen) return null;

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className={`dialog`} onClick={e => e.stopPropagation()} role="dialog" aria-modal="true">
        <div className="dialog-header">
          <div className="dialog-icon">
            <AlertTriangle size={24} />
          </div>
          <h2>{title}</h2>
          <button onClick={onClose} className="dialog-close" aria-label="Close">
            <X size={20} />
          </button>
        </div>
        <div className="dialog-body">
          <p>{message}</p>
        </div>
        <div className="dialog-footer">
          <button onClick={onClose} className="btn btn-secondary">
            {cancelText}
          </button>
          <button onClick={onConfirm} className={`btn btn-primary btn-${variant}`}>
            {confirmText}
          </button>
        </div>
        <div className="confirm-hint">
          <kbd>Esc</kbd> to cancel • <kbd>Ctrl</kbd> + <kbd>Enter</kbd> to confirm
        </div>
      </div>
    </div>
  );
}

export default ConfirmDialog;
