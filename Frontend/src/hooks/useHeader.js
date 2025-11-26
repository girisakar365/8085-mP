import { useState, useEffect, useRef } from 'react';
import { useSettingsActions, useTheme } from '../stores/settingsStore';

export function useHeader() {
  const theme = useTheme();
  const { toggleTheme, openGeminiKeyDialog } = useSettingsActions();

  // Menu state
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef(null);

  // Close menu when clicking outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setMenuOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Menu action handlers
  const handleApiKey = () => {
    setMenuOpen(false);
    openGeminiKeyDialog();
  };

  const handleThemeToggle = () => {
    setMenuOpen(false);
    toggleTheme();
  };

  const handleAbout = () => {
    setMenuOpen(false);
  };

  const handleUpdate = () => {
    setMenuOpen(false);
  };

  const handleReport = () => {
    setMenuOpen(false);
  };

  return {
    menuOpen,
    setMenuOpen,
    menuRef,
    theme,
    handleApiKey,
    handleThemeToggle,
    handleAbout,
    handleUpdate,
    handleReport,
  };
}