import { Code2, Cpu } from 'lucide-react';
import './MobileTabBar.css';

function MobileTabBar({ activeTab, onTabChange }) {
  return (
    <div className="mobile-tab-bar" role="tablist" aria-label="Mobile Navigation">
      <button
        className={`mobile-tab ${activeTab === 'editor' ? 'active' : ''}`}
        onClick={() => onTabChange('editor')}
        role="tab"
        aria-selected={activeTab === 'editor'}
        aria-controls="editor-panel"
      >
        <Code2 size={24} />
        <span>Editor</span>
      </button>
      <button
        className={`mobile-tab ${activeTab === 'processor' ? 'active' : ''}`}
        onClick={() => onTabChange('processor')}
        role="tab"
        aria-selected={activeTab === 'processor'}
        aria-controls="processor-panel"
      >
        <Cpu size={24} />
        <span>Processor</span>
      </button>
    </div>
  );
}

export default MobileTabBar;
