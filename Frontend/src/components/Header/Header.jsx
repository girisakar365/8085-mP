import { useHeader } from '../../hooks/useHeader';
import { useGeminiKeyDialogOpen, useAboutDialogOpen, useReportDialogOpen, useSettingsActions } from '../../stores/settingsStore';
import APIKeyManager from '../APIKeyManager/APIKeyManager';
import AboutDialog from '../../pages/About/AboutDialog';
import ReportDialog from '../../pages/Report/ReportDialog';
import './Header.css';

const THEMES = {
  DARK: 'dark',
  LIGHT: 'light',
};

import { DESIGN_TOKENS } from '../../constants';

function AppIcon() {
  return (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="3" y="3" width="18" height="18" rx="4" fill="#222" />
      <path d="M8 9h8M8 12h8M8 15h5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
    </svg>
  );
}

export default function Header() {
  const {
    menuOpen,
    setMenuOpen,
    menuRef,
    theme,
    handleApiKey,
    handleThemeToggle,
    handleAbout,
    handleUpdate,
    handleReport,
  } = useHeader();

  const isGeminiKeyDialogOpen = useGeminiKeyDialogOpen();
  const isAboutDialogOpen = useAboutDialogOpen();
  const isReportDialogOpen = useReportDialogOpen();
  const { closeGeminiKeyDialog, openAboutDialog, closeAboutDialog, openReportDialog, closeReportDialog } = useSettingsActions();

  const handleAboutClick = () => {
    handleAbout();
    openAboutDialog();
  };

  const handleReportClick = () => {
    handleReport();
    openReportDialog();
  };

  return (
    <header className="header">
      <div className="header-left">
        <div className="header-icon">
          <AppIcon />
        </div>
        <h1 className="header-brand">asm studio</h1>
      </div>

      <div className="header-right" ref={menuRef}>
        <button
          className="hamburger"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle menu"
          aria-expanded={menuOpen}
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        {menuOpen && (
          <nav className="dropdown-menu" role="menu">
            <>
              <button className="menu-item" onClick={handleThemeToggle} role="menuitem">
                Theme: {theme === THEMES.LIGHT ? 'Light' : 'Dark'}
              </button>
              <button className="menu-item" onClick={handleApiKey} role="menuitem">
                API Key
              </button>
              <button className="menu-item" onClick={handleAboutClick} role="menuitem">
                About
              </button>
              <button className="menu-item" onClick={handleUpdate} role="menuitem">
                Check Update
              </button>
              <button className="menu-item" onClick={handleReportClick} role="menuitem">
                Report
              </button>
            </>
          </nav>
        )}
      </div>

      <>
        <APIKeyManager
          isOpen={isGeminiKeyDialogOpen}
          onClose={closeGeminiKeyDialog}
        />
        <AboutDialog
          isOpen={isAboutDialogOpen}
          onClose={closeAboutDialog}
        />
        <ReportDialog
          isOpen={isReportDialogOpen}
          onClose={closeReportDialog}
        />
      </>
    </header>
  );
}
