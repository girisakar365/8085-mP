
import { create } from 'zustand';
import { persist, subscribeWithSelector } from 'zustand/middleware';
import { DESIGN_TOKENS } from '../constants';

const THEMES = {
  DARK: DESIGN_TOKENS.COLORS.DARK || 'dark',
  LIGHT: DESIGN_TOKENS.COLORS.LIGHT || 'light',
};

const STORAGE_KEYS = {
  SETTINGS: 'asm-studio-settings',
};

export const SETTINGS_ACTIONS = {
  SET_THEME: 'SET_THEME',
  TOGGLE_THEME: 'TOGGLE_THEME',
  SET_GEMINI_API_KEY: 'SET_GEMINI_API_KEY',
  CLEAR_GEMINI_API_KEY: 'CLEAR_GEMINI_API_KEY',
  OPEN_COMMAND_PALETTE: 'OPEN_COMMAND_PALETTE',
  CLOSE_COMMAND_PALETTE: 'CLOSE_COMMAND_PALETTE',
  TOGGLE_COMMAND_PALETTE: 'TOGGLE_COMMAND_PALETTE',
  OPEN_SHORTCUTS_DIALOG: 'OPEN_SHORTCUTS_DIALOG',
  CLOSE_SHORTCUTS_DIALOG: 'CLOSE_SHORTCUTS_DIALOG',
  TOGGLE_SHORTCUTS_DIALOG: 'TOGGLE_SHORTCUTS_DIALOG',
  OPEN_GEMINI_KEY_DIALOG: 'OPEN_GEMINI_KEY_DIALOG',
  CLOSE_GEMINI_KEY_DIALOG: 'CLOSE_GEMINI_KEY_DIALOG',
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

  setGeminiApiKey: (key) => ({
    type: SETTINGS_ACTIONS.SET_GEMINI_API_KEY,
    payload: key,
  }),

  clearGeminiApiKey: () => ({
    type: SETTINGS_ACTIONS.CLEAR_GEMINI_API_KEY,
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

  openGeminiKeyDialog: () => ({
    type: SETTINGS_ACTIONS.OPEN_GEMINI_KEY_DIALOG,
  }),

  closeGeminiKeyDialog: () => ({
    type: SETTINGS_ACTIONS.CLOSE_GEMINI_KEY_DIALOG,
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

const useSettingsStore = create(
  persist(
    subscribeWithSelector((set, get) => ({
      theme: THEMES.DARK,
      geminiApiKey: null,
      maskedGeminiKey: null,
      commandPaletteOpen: false,
      shortcutsDialogOpen: false,
      geminiKeyDialogOpen: false,
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

      // Initialize theme on document element
      __init: (() => {
        setTimeout(() => {
          const state = get();
          document.documentElement.setAttribute('data-theme', state.theme);
        }, 0);
      })(),

      // Dispatch function for actions
      dispatch: (action) => {
        const state = get();
        switch (action.type) {
          case SETTINGS_ACTIONS.SET_THEME:
            document.documentElement.setAttribute('data-theme', action.payload);
            set({ theme: action.payload });
            break;

          case SETTINGS_ACTIONS.TOGGLE_THEME:
            const newTheme = state.theme === THEMES.DARK ? THEMES.LIGHT : THEMES.DARK;
            document.documentElement.setAttribute('data-theme', newTheme);
            set({ theme: newTheme });
            break;

          case SETTINGS_ACTIONS.SET_GEMINI_API_KEY:
            const masked = action.payload ? `${action.payload.slice(0, 8)}...${action.payload.slice(-4)}` : null;
            set({
              geminiApiKey: action.payload,
              maskedGeminiKey: masked
            });
            break;

          case SETTINGS_ACTIONS.CLEAR_GEMINI_API_KEY:
            set({
              geminiApiKey: null,
              maskedGeminiKey: null
            });
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

          case SETTINGS_ACTIONS.OPEN_GEMINI_KEY_DIALOG:
            set({ geminiKeyDialogOpen: true });
            break;

          case SETTINGS_ACTIONS.CLOSE_GEMINI_KEY_DIALOG:
            set({ geminiKeyDialogOpen: false });
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
        geminiApiKey: state.geminiApiKey,
        maskedGeminiKey: state.maskedGeminiKey,
      }),
    }
  )
);

// Selectors
export const settingsSelectors = {
  getTheme: (state) => state.theme,
  getGeminiApiKey: (state) => state.geminiApiKey,
  getMaskedGeminiKey: (state) => state.maskedGeminiKey,
  isCommandPaletteOpen: (state) => state.commandPaletteOpen,
  isShortcutsDialogOpen: (state) => state.shortcutsDialogOpen,
  isGeminiKeyDialogOpen: (state) => state.geminiKeyDialogOpen,
  isAboutDialogOpen: (state) => state.aboutDialogOpen,
  isReportDialogOpen: (state) => state.reportDialogOpen,
  getConfirmDialog: (state) => state.confirmDialog,

  // Computed selectors
  hasGeminiKey: (state) => !!state.geminiApiKey,
  isDarkTheme: (state) => state.theme === THEMES.DARK,
  isLightTheme: (state) => state.theme === THEMES.LIGHT,
  getAllSettings: (state) => ({
    theme: state.theme,
    geminiApiKey: state.geminiApiKey,
    maskedGeminiKey: state.maskedGeminiKey,
    commandPaletteOpen: state.commandPaletteOpen,
    shortcutsDialogOpen: state.shortcutsDialogOpen,
    geminiKeyDialogOpen: state.geminiKeyDialogOpen,
    aboutDialogOpen: state.aboutDialogOpen,
    reportDialogOpen: state.reportDialogOpen,
    confirmDialog: state.confirmDialog,
  }),
};

// Convenience hooks that use selectors
export const useTheme = () => useSettingsStore(settingsSelectors.getTheme);
export const useGeminiApiKey = () => useSettingsStore(settingsSelectors.getGeminiApiKey);
export const useMaskedGeminiKey = () => useSettingsStore(settingsSelectors.getMaskedGeminiKey);
export const useCommandPaletteOpen = () => useSettingsStore(settingsSelectors.isCommandPaletteOpen);
export const useShortcutsDialogOpen = () => useSettingsStore(settingsSelectors.isShortcutsDialogOpen);
export const useGeminiKeyDialogOpen = () => useSettingsStore(settingsSelectors.isGeminiKeyDialogOpen);
export const useAboutDialogOpen = () => useSettingsStore(settingsSelectors.isAboutDialogOpen);
export const useReportDialogOpen = () => useSettingsStore(settingsSelectors.isReportDialogOpen);
export const useConfirmDialog = () => useSettingsStore(settingsSelectors.getConfirmDialog);
export const useHasGeminiKey = () => useSettingsStore(settingsSelectors.hasGeminiKey);
export const useIsDarkTheme = () => useSettingsStore(settingsSelectors.isDarkTheme);
export const useIsLightTheme = () => useSettingsStore(settingsSelectors.isLightTheme);
export const useAllSettings = () => useSettingsStore(settingsSelectors.getAllSettings);

// Action hooks
export const useSettingsActions = () => {
  const dispatch = useSettingsStore((state) => state.dispatch);

  return {
    setTheme: (theme) => dispatch(settingsActions.setTheme(theme)),
    toggleTheme: () => dispatch(settingsActions.toggleTheme()),
    setGeminiApiKey: (key) => dispatch(settingsActions.setGeminiApiKey(key)),
    clearGeminiApiKey: () => dispatch(settingsActions.clearGeminiApiKey()),
    openCommandPalette: () => dispatch(settingsActions.openCommandPalette()),
    closeCommandPalette: () => dispatch(settingsActions.closeCommandPalette()),
    toggleCommandPalette: () => dispatch(settingsActions.toggleCommandPalette()),
    openShortcutsDialog: () => dispatch(settingsActions.openShortcutsDialog()),
    closeShortcutsDialog: () => dispatch(settingsActions.closeShortcutsDialog()),
    toggleShortcutsDialog: () => dispatch(settingsActions.toggleShortcutsDialog()),
    openGeminiKeyDialog: () => dispatch(settingsActions.openGeminiKeyDialog()),
    closeGeminiKeyDialog: () => dispatch(settingsActions.closeGeminiKeyDialog()),
    openAboutDialog: () => dispatch(settingsActions.openAboutDialog()),
    closeAboutDialog: () => dispatch(settingsActions.closeAboutDialog()),
    openReportDialog: () => dispatch(settingsActions.openReportDialog()),
    closeReportDialog: () => dispatch(settingsActions.closeReportDialog()),
    showConfirmDialog: (config) => dispatch(settingsActions.showConfirmDialog(config)),
    closeConfirmDialog: () => dispatch(settingsActions.closeConfirmDialog()),
  };
};

export default useSettingsStore;
