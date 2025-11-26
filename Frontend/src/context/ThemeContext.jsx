import { createContext, useState, useContext, useEffect } from 'react';
import { DESIGN_TOKENS } from '../constants.js';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('dark');

  // Set design token CSS variables
  useEffect(() => {
    const root = document.documentElement;
    
    // Set color variables
    Object.entries(DESIGN_TOKENS.COLORS).forEach(([key, value]) => {
      root.style.setProperty(`--color-${key.toLowerCase()}`, value);
    });
    
    // Set spacing variables
    Object.entries(DESIGN_TOKENS.SPACING).forEach(([key, value]) => {
      root.style.setProperty(`--space-${key.toLowerCase()}`, `${value}px`);
    });
    
    // Set radius variables
    Object.entries(DESIGN_TOKENS.RADIUS).forEach(([key, value]) => {
      root.style.setProperty(`--radius-${key.toLowerCase()}`, `${value}px`);
    });
    
    // Set font size variables
    Object.entries(DESIGN_TOKENS.FONT_SIZE).forEach(([key, value]) => {
      root.style.setProperty(`--font-${key.toLowerCase()}`, `${value}px`);
    });
    
    // Set font weight variables
    Object.entries(DESIGN_TOKENS.FONT_WEIGHT).forEach(([key, value]) => {
      root.style.setProperty(`--font-weight-${key.toLowerCase()}`, value);
    });
    
    // Set shadow variables
    Object.entries(DESIGN_TOKENS.SHADOW).forEach(([key, value]) => {
      root.style.setProperty(`--shadow-${key.toLowerCase()}`, value);
    });
    
    // Set overlay variables
    Object.entries(DESIGN_TOKENS.OVERLAY).forEach(([key, value]) => {
      root.style.setProperty(`--overlay-${key.toLowerCase()}`, value);
    });
    
    // Set z-index variables
    Object.entries(DESIGN_TOKENS.Z_INDEX).forEach(([key, value]) => {
      root.style.setProperty(`--z-${key.toLowerCase()}`, value);
    });
    
    // Set transition variables
    Object.entries(DESIGN_TOKENS.TRANSITION).forEach(([key, value]) => {
      root.style.setProperty(`--transition-${key.toLowerCase()}`, value);
    });
    
    // Set component size variables
    Object.entries(DESIGN_TOKENS.COMPONENT_SIZE).forEach(([key, value]) => {
      root.style.setProperty(`--${key.toLowerCase()}`, `${value}px`);
    });
  }, []);

  useEffect(() => {
    const savedSettings = localStorage.getItem('8085_settings');
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      if (settings.theme) {
        setTheme(settings.theme);
      }
    }
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    
    document.documentElement.classList.add('theme-transitioning');
    
    setTimeout(() => {
      document.documentElement.classList.remove('theme-transitioning');
    }, 600);
    
    const savedSettings = JSON.parse(localStorage.getItem('8085_settings') || '{}');
    savedSettings.theme = theme;
    localStorage.setItem('8085_settings', JSON.stringify(savedSettings));
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
