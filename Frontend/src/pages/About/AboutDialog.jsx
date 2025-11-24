import React from 'react';
import { Info } from 'lucide-react';
import './AboutDialog.css';

const APP_CONFIG = {
  NAME: 'asm studio',
  DESCRIPTION: '8085 Assembly Notebook & AI Assistant',
  VERSION: '1.0.0',
};

export default function AboutDialog({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="dialog-overlay" onClick={onClose}>
      <div className="dialog" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <div className="dialog-header">
          <div className="dialog-icon">
            <Info size={24} />
          </div>
          <h2>About {APP_CONFIG.NAME.toLowerCase()}</h2>
        </div>
        
        <div className="dialog-body">
          <div className="about-content">
            <div className="about-section">
              <h3>{APP_CONFIG.NAME.toLowerCase()}</h3>
              <p>{APP_CONFIG.DESCRIPTION}</p>
            </div>
            
            <div className="about-section">
              <h4>Version</h4>
              <p>{APP_CONFIG.VERSION}</p>
            </div>

            <div className="about-section">
              <h4>Features</h4>
              <ul>
                <li>Code editing</li>
                <li>AI-powered code explanations</li>
                <li>Error analysis and suggestions</li>
                <li>Dark/Light theme support</li>
              </ul>
            </div>

            <div className="about-section">
              <h4>Privacy</h4>
              <p>
                Your API keys and preferences are stored locally on your device. 
                No data is transmitted without your explicit consent.
              </p>
            </div>
          </div>
        </div>
        
        <div className="dialog-footer">
          <button className="btn btn-primary" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
}