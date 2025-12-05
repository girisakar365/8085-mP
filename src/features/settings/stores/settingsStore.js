
import { create } from 'zustand';
import { persist, subscribeWithSelector } from 'zustand/middleware';
import { DESIGN_TOKENS } from '../../../constants';

const THEMES = {
  DARK: DESIGN_TOKENS.COLORS.DARK || 'dark',
  LIGHT: DESIGN_TOKENS.COLORS.LIGHT || 'light',
};

const STORAGE_KEYS = {
  SETTINGS: 'asm-studio-settings',
};

// Initialize CSS design tokens
const initializeDesignTokens = () => {
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
};

export const SETTINGS_ACTIONS = {
  SET_THEME: 'SET_THEME',
  TOGGLE_THEME: 'TOGGLE_THEME',
  SET_GROQ_API_KEY: 'SET_GROQ_API_KEY',
  CLEAR_GROQ_API_KEY: 'CLEAR_GROQ_API_KEY',
  SET_SELECTED_MODEL: 'SET_SELECTED_MODEL',
  OPEN_COMMAND_PALETTE: 'OPEN_COMMAND_PALETTE',
  CLOSE_COMMAND_PALETTE: 'CLOSE_COMMAND_PALETTE',
  TOGGLE_COMMAND_PALETTE: 'TOGGLE_COMMAND_PALETTE',
  OPEN_SHORTCUTS_DIALOG: 'OPEN_SHORTCUTS_DIALOG',
  CLOSE_SHORTCUTS_DIALOG: 'CLOSE_SHORTCUTS_DIALOG',
  TOGGLE_SHORTCUTS_DIALOG: 'TOGGLE_SHORTCUTS_DIALOG',
  OPEN_AI_KEY_DIALOG: 'OPEN_AI_KEY_DIALOG',
  CLOSE_AI_KEY_DIALOG: 'CLOSE_AI_KEY_DIALOG',
  OPEN_ABOUT_DIALOG: 'OPEN_ABOUT_DIALOG',
  CLOSE_ABOUT_DIALOG: 'CLOSE_ABOUT_DIALOG',
  OPEN_REPORT_DIALOG: 'OPEN_REPORT_DIALOG',
  CLOSE_REPORT_DIALOG: 'CLOSE_REPORT_DIALOG',
  SHOW_CONFIRM_DIALOG: 'SHOW_CONFIRM_DIALOG',
  CLOSE_CONFIRM_DIALOG: 'CLOSE_CONFIRM_DIALOG',
};

export const settingsActions = {
  setTheme: (theme) => ({
    type: SETTINGS_ACTIONS.SET_THEME,
    payload: theme,
  }),

  toggleTheme: () => ({
    type: SETTINGS_ACTIONS.TOGGLE_THEME,
  }),

  setGroqApiKey: (key) => ({
    type: SETTINGS_ACTIONS.SET_GROQ_API_KEY,
    payload: key,
  }),

  clearGroqApiKey: () => ({
    type: SETTINGS_ACTIONS.CLEAR_GROQ_API_KEY,
  }),

  setSelectedModel: (model) => ({
    type: SETTINGS_ACTIONS.SET_SELECTED_MODEL,
    payload: model,
  }),

  openCommandPalette: () => ({
    type: SETTINGS_ACTIONS.OPEN_COMMAND_PALETTE,
  }),

  closeCommandPalette: () => ({
    type: SETTINGS_ACTIONS.CLOSE_COMMAND_PALETTE,
  }),

  toggleCommandPalette: () => ({
    type: SETTINGS_ACTIONS.TOGGLE_COMMAND_PALETTE,
  }),

  openShortcutsDialog: () => ({
    type: SETTINGS_ACTIONS.OPEN_SHORTCUTS_DIALOG,
  }),

  closeShortcutsDialog: () => ({
    type: SETTINGS_ACTIONS.CLOSE_SHORTCUTS_DIALOG,
  }),

  toggleShortcutsDialog: () => ({
    type: SETTINGS_ACTIONS.TOGGLE_SHORTCUTS_DIALOG,
  }),

  openGroqKeyDialog: () => ({
    type: SETTINGS_ACTIONS.OPEN_AI_KEY_DIALOG,
  }),

  closeGroqKeyDialog: () => ({
    type: SETTINGS_ACTIONS.CLOSE_AI_KEY_DIALOG,
  }),

  openAboutDialog: () => ({
    type: SETTINGS_ACTIONS.OPEN_ABOUT_DIALOG,
  }),

  closeAboutDialog: () => ({
    type: SETTINGS_ACTIONS.CLOSE_ABOUT_DIALOG,
  }),

  openReportDialog: () => ({
    type: SETTINGS_ACTIONS.OPEN_REPORT_DIALOG,
  }),

  closeReportDialog: () => ({
    type: SETTINGS_ACTIONS.CLOSE_REPORT_DIALOG,
  }),

  showConfirmDialog: (config) => ({
    type: SETTINGS_ACTIONS.SHOW_CONFIRM_DIALOG,
    payload: config,
  }),

  closeConfirmDialog: () => ({
    type: SETTINGS_ACTIONS.CLOSE_CONFIRM_DIALOG,
  }),
};

// Available AI Models for the dropdown
export const AI_MODELS = [
  { id: 'llama-3.3-70b-versatile', name: 'Llama 3.3 70B Versatile', provider: 'Groq' },
  { id: 'llama-3.1-8b-instant', name: 'Llama 3.1 8B Instant', provider: 'Groq' },
  { id: 'llama-3.1-70b-versatile', name: 'Llama 3.1 70B Versatile', provider: 'Groq' },
  { id: 'llama3-8b-8192', name: 'Llama 3 8B', provider: 'Groq' },
  { id: 'llama3-70b-8192', name: 'Llama 3 70B', provider: 'Groq' },
  { id: 'gemma2-9b-it', name: 'Gemma 2 9B', provider: 'Groq' },
  { id: 'mixtral-8x7b-32768', name: 'Mixtral 8x7B', provider: 'Groq' },
];

const useSettingsStore = create(
  persist(
    subscribeWithSelector((set, get) => ({
      theme: THEMES.DARK,
      groqApiKey: null,
      maskedGroqKey: null,
      selectedModel: 'llama-3.1-8b-instant',
      commandPaletteOpen: false,
      shortcutsDialogOpen: false,
      groqKeyDialogOpen: false,
      aboutDialogOpen: false,
      reportDialogOpen: false,
      confirmDialog: {
        isOpen: false,
        title: '',
        message: '',
        confirmText: 'Confirm',
        cancelText: 'Cancel',
        variant: 'danger',
        onConfirm: null,
        onCancel: null,
      },

      // Initialize theme and design tokens
      __init: (() => {
        setTimeout(() => {
          const state = get();
          initializeDesignTokens();
          document.documentElement.setAttribute('data-theme', state.theme);
        }, 0);
      })(),

      // Dispatch function for actions
      dispatch: (action) => {
        const state = get();
        switch (action.type) {
          case SETTINGS_ACTIONS.SET_THEME:
            document.documentElement.setAttribute('data-theme', action.payload);
            document.documentElement.classList.add('theme-transitioning');
            setTimeout(() => {
              document.documentElement.classList.remove('theme-transitioning');
            }, 600);
            set({ theme: action.payload });
            break;

          case SETTINGS_ACTIONS.TOGGLE_THEME:
            const newTheme = state.theme === THEMES.DARK ? THEMES.LIGHT : THEMES.DARK;
            document.documentElement.setAttribute('data-theme', newTheme);
            document.documentElement.classList.add('theme-transitioning');
            setTimeout(() => {
              document.documentElement.classList.remove('theme-transitioning');
            }, 600);
            set({ theme: newTheme });
            break;

          case SETTINGS_ACTIONS.SET_GROQ_API_KEY:
            const masked = action.payload ? `${action.payload.slice(0, 8)}...${action.payload.slice(-4)}` : null;
            set({
              groqApiKey: action.payload,
              maskedGroqKey: masked
            });
            break;

          case SETTINGS_ACTIONS.CLEAR_GROQ_API_KEY:
            set({
              groqApiKey: null,
              maskedGroqKey: null
            });
            break;

          case SETTINGS_ACTIONS.SET_SELECTED_MODEL:
            set({ selectedModel: action.payload });
            break;

          case SETTINGS_ACTIONS.OPEN_COMMAND_PALETTE:
            set({ commandPaletteOpen: true });
            break;

          case SETTINGS_ACTIONS.CLOSE_COMMAND_PALETTE:
            set({ commandPaletteOpen: false });
            break;

          case SETTINGS_ACTIONS.TOGGLE_COMMAND_PALETTE:
            set({ commandPaletteOpen: !state.commandPaletteOpen });
            break;

          case SETTINGS_ACTIONS.OPEN_SHORTCUTS_DIALOG:
            set({ shortcutsDialogOpen: true });
            break;

          case SETTINGS_ACTIONS.CLOSE_SHORTCUTS_DIALOG:
            set({ shortcutsDialogOpen: false });
            break;

          case SETTINGS_ACTIONS.TOGGLE_SHORTCUTS_DIALOG:
            set({ shortcutsDialogOpen: !state.shortcutsDialogOpen });
            break;

          case SETTINGS_ACTIONS.OPEN_AI_KEY_DIALOG:
            set({ groqKeyDialogOpen: true });
            break;

          case SETTINGS_ACTIONS.CLOSE_AI_KEY_DIALOG:
            set({ groqKeyDialogOpen: false });
            break;

          case SETTINGS_ACTIONS.OPEN_ABOUT_DIALOG:
            set({ aboutDialogOpen: true });
            break;

          case SETTINGS_ACTIONS.CLOSE_ABOUT_DIALOG:
            set({ aboutDialogOpen: false });
            break;

          case SETTINGS_ACTIONS.OPEN_REPORT_DIALOG:
            set({ reportDialogOpen: true });
            break;

          case SETTINGS_ACTIONS.CLOSE_REPORT_DIALOG:
            set({ reportDialogOpen: false });
            break;

          case SETTINGS_ACTIONS.SHOW_CONFIRM_DIALOG:
            set({
              confirmDialog: {
                isOpen: true,
                title: action.payload.title || 'Confirm Action',
                message: action.payload.message,
                confirmText: action.payload.confirmText || 'Confirm',
                cancelText: action.payload.cancelText || 'Cancel',
                variant: action.payload.variant || 'danger',
                onConfirm: action.payload.onConfirm,
                onCancel: action.payload.onCancel,
              },
            });
            break;

          case SETTINGS_ACTIONS.CLOSE_CONFIRM_DIALOG:
            set({
              confirmDialog: {
                ...state.confirmDialog,
                isOpen: false,
              },
            });
            break;
        }
      },
    })),
    {
      name: STORAGE_KEYS.SETTINGS,
      partialize: (state) => ({
        theme: state.theme,
        groqApiKey: state.groqApiKey,
        maskedGroqKey: state.maskedGroqKey,
        selectedModel: state.selectedModel,
      }),
    }
  )
);

// Selectors
export const settingsSelectors = {
  getTheme: (state) => state.theme,
  getGroqApiKey: (state) => state.groqApiKey,
  getMaskedGroqKey: (state) => state.maskedGroqKey,
  getSelectedModel: (state) => state.selectedModel,
  isCommandPaletteOpen: (state) => state.commandPaletteOpen,
  isShortcutsDialogOpen: (state) => state.shortcutsDialogOpen,
  isGroqKeyDialogOpen: (state) => state.groqKeyDialogOpen,
  isAboutDialogOpen: (state) => state.aboutDialogOpen,
  isReportDialogOpen: (state) => state.reportDialogOpen,
  getConfirmDialog: (state) => state.confirmDialog,

  // Computed selectors
  hasGroqKey: (state) => !!state.groqApiKey,
  isDarkTheme: (state) => state.theme === THEMES.DARK,
  isLightTheme: (state) => state.theme === THEMES.LIGHT,
  getAllSettings: (state) => ({
    theme: state.theme,
    groqApiKey: state.groqApiKey,
    maskedGroqKey: state.maskedGroqKey,
    selectedModel: state.selectedModel,
    commandPaletteOpen: state.commandPaletteOpen,
    shortcutsDialogOpen: state.shortcutsDialogOpen,
    groqKeyDialogOpen: state.groqKeyDialogOpen,
    aboutDialogOpen: state.aboutDialogOpen,
    reportDialogOpen: state.reportDialogOpen,
    confirmDialog: state.confirmDialog,
  }),
};

// Convenience hooks that use selectors
export const useTheme = () => useSettingsStore(settingsSelectors.getTheme);
export const useGroqApiKey = () => useSettingsStore(settingsSelectors.getGroqApiKey);
export const useMaskedGroqKey = () => useSettingsStore(settingsSelectors.getMaskedGroqKey);
export const useSelectedModel = () => useSettingsStore(settingsSelectors.getSelectedModel);
export const useCommandPaletteOpen = () => useSettingsStore(settingsSelectors.isCommandPaletteOpen);
export const useShortcutsDialogOpen = () => useSettingsStore(settingsSelectors.isShortcutsDialogOpen);
export const useGroqKeyDialogOpen = () => useSettingsStore(settingsSelectors.isGroqKeyDialogOpen);
export const useAboutDialogOpen = () => useSettingsStore(settingsSelectors.isAboutDialogOpen);
export const useReportDialogOpen = () => useSettingsStore(settingsSelectors.isReportDialogOpen);
export const useConfirmDialog = () => useSettingsStore(settingsSelectors.getConfirmDialog);
export const useHasGroqKey = () => useSettingsStore(settingsSelectors.hasGroqKey);
export const useIsDarkTheme = () => useSettingsStore(settingsSelectors.isDarkTheme);
export const useIsLightTheme = () => useSettingsStore(settingsSelectors.isLightTheme);
export const useAllSettings = () => useSettingsStore(settingsSelectors.getAllSettings);

// Action hooks
export const useSettingsActions = () => {
  const dispatch = useSettingsStore((state) => state.dispatch);

  return {
    setTheme: (theme) => dispatch(settingsActions.setTheme(theme)),
    toggleTheme: () => dispatch(settingsActions.toggleTheme()),
    setGroqApiKey: (key) => dispatch(settingsActions.setGroqApiKey(key)),
    clearGroqApiKey: () => dispatch(settingsActions.clearGroqApiKey()),
    setSelectedModel: (model) => dispatch(settingsActions.setSelectedModel(model)),
    openCommandPalette: () => dispatch(settingsActions.openCommandPalette()),
    closeCommandPalette: () => dispatch(settingsActions.closeCommandPalette()),
    toggleCommandPalette: () => dispatch(settingsActions.toggleCommandPalette()),
    openShortcutsDialog: () => dispatch(settingsActions.openShortcutsDialog()),
    closeShortcutsDialog: () => dispatch(settingsActions.closeShortcutsDialog()),
    toggleShortcutsDialog: () => dispatch(settingsActions.toggleShortcutsDialog()),
    openGroqKeyDialog: () => dispatch(settingsActions.openGroqKeyDialog()),
    closeGroqKeyDialog: () => dispatch(settingsActions.closeGroqKeyDialog()),
    openAboutDialog: () => dispatch(settingsActions.openAboutDialog()),
    closeAboutDialog: () => dispatch(settingsActions.closeAboutDialog()),
    openReportDialog: () => dispatch(settingsActions.openReportDialog()),
    closeReportDialog: () => dispatch(settingsActions.closeReportDialog()),
    showConfirmDialog: (config) => dispatch(settingsActions.showConfirmDialog(config)),
    closeConfirmDialog: () => dispatch(settingsActions.closeConfirmDialog()),
  };
};

export default useSettingsStore;
