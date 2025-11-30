import { useHeader } from '../../../features/settings/hooks/useHeader';
import { useGeminiKeyDialogOpen, useAboutDialogOpen, useReportDialogOpen, useSettingsActions } from '../../../features/settings/stores/settingsStore';
import APIKeyManager from '../../../features/settings/components/APIKeyManager';
import AboutDialog from '../../../pages/About/AboutDialog';
import ReportDialog from '../../../pages/Report/ReportDialog';
import './Header.css';

const THEMES = {
  DARK: 'dark',
  LIGHT: 'light',
};

import { DESIGN_TOKENS } from '../../../constants';

function AppIcon() {
  return (
    <img src="icon.png" alt="App Icon" height="30px" width="30px"/>
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
