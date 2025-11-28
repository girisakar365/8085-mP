export const DESIGN_TOKENS = {
  // Colors (Hex and RGB for rgba usage)
  COLORS: {
    PRIMARY: '#007acc',
    PRIMARY_RGB: '0, 122, 204',
    PRIMARY_HOVER: '#005a9e',
    PRIMARY_HOVER_RGB: '0, 90, 158',
    PRIMARY_LIGHT: '#e6f3ff',
    PRIMARY_LIGHT_RGB: '230, 243, 255',

    SUCCESS: '#28a745',
    SUCCESS_RGB: '40, 167, 69',
    SUCCESS_LIGHT: '#d4edda',
    SUCCESS_LIGHT_RGB: '212, 237, 218',

    ERROR: '#d73a49',
    ERROR_RGB: '215, 58, 73',
    ERROR_LIGHT: '#f8d7da',
    ERROR_LIGHT_RGB: '248, 215, 218',

    WARNING: '#ffc107',
    WARNING_RGB: '255, 193, 7',
    WARNING_LIGHT: '#fff3cd',
    WARNING_LIGHT_RGB: '255, 243, 205',

    INFO: '#17a2b8',
    INFO_RGB: '23, 162, 184',
    INFO_LIGHT: '#d1ecf1',
    INFO_LIGHT_RGB: '209, 236, 241',

    // Dialog theme colors
    EXPORT_BLUE: '#3b82f6',
    EXPORT_BLUE_RGB: '59, 130, 246',
    EXPORT_BLUE_LIGHT: '#2563eb',
    EXPORT_BLUE_LIGHT_RGB: '37, 99, 235',
    EXPORT_BLUE_DARKER: '#1d4ed8',

    REPORT_RED: '#ef4444',
    REPORT_RED_RGB: '239, 68, 68',
    REPORT_RED_LIGHT: '#dc2626',
    REPORT_RED_LIGHT_RGB: '220, 38, 38',

    API_PURPLE: '#9333ea',
    API_PURPLE_RGB: '147, 51, 234',
    // Message colors
    ERROR_LIGHT_BG_LIGHT: '#FFEBEE',
    ERROR_LIGHT_BG_DARK: '#2D1A1F',
    ERROR_LIGHT_BORDER_LIGHT: '#D73A49',
    ERROR_LIGHT_BORDER_DARK: '#FF7B8A',
    ERROR_LIGHT_TEXT_LIGHT: '#1A1A1A',
    ERROR_LIGHT_TEXT_DARK: '#FFD7DC',

    SUCCESS_LIGHT_BG_LIGHT: '#E8F5E9',
    SUCCESS_LIGHT_BG_DARK: '#1A2B1F',
    SUCCESS_LIGHT_BORDER_LIGHT: '#22863a',
    SUCCESS_LIGHT_BORDER_DARK: '#3FB950',
    SUCCESS_LIGHT_TEXT_LIGHT: '#1A1A1A',
    SUCCESS_LIGHT_TEXT_DARK: '#D4F0DB',
  },
  // Spacing Scale (in px)
  SPACING: {
    XS: 4,
    SM: 8,
    MD: 12,
    LG: 16,
    XL: 20,
    XXL: 24,
    XXXL: 32,
    HUGE: 48,
  },

  // Border Radius Scale
  RADIUS: {
    SM: 3,
    MD: 6,
    LG: 8,
    XL: 12,
    ROUND: 50,
  },

  // Font Sizes
  FONT_SIZE: {
    XS: 11,
    SM: 12,
    MD: 13,
    LG: 14,
    XL: 16,
    XXL: 18,
    XXXL: 20,
    HUGE: 24,
  },

  // Font Weights
  FONT_WEIGHT: {
    NORMAL: 400,
    MEDIUM: 500,
    SEMIBOLD: 600,
    BOLD: 700,
  },

  // Shadows
  SHADOW: {
    SM: '0 1px 3px rgba(0, 0, 0, 0.1)',
    MD: '0 2px 8px rgba(0, 0, 0, 0.15)',
    LG: '0 4px 16px rgba(0, 0, 0, 0.2)',
    XL: '0 8px 32px rgba(0, 0, 0, 0.3)',
  },

  // Overlay Colors
  OVERLAY: {
    MODAL: 'rgba(0, 0, 0, 0.6)',
  },

  // Z-Index Scale
  Z_INDEX: {
    BASE: 1,
    DROPDOWN: 100,
    MODAL: 200,
    TOOLTIP: 300,
    NOTIFICATION: 400,
  },

  // Transitions
  TRANSITION: {
    FAST: '0.15s ease',
    NORMAL: '0.2s ease',
    SLOW: '0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  },

  // Component Sizes
  COMPONENT_SIZE: {
    BUTTON_HEIGHT: 36,
    INPUT_HEIGHT: 36,
    ICON_SIZE: 18,
    AVATAR_SIZE: 32,
  },
};

export const API_CONFIG = {
  BASE_URL: 'http://127.0.0.1:3221',
  ENDPOINTS: {
    HEALTH: '/health',
    EXECUTE: '/api/execute',
    ASSEMBLE: '/api/assemble',
    RESET: '/api/reset',
    DOCS: '/api/docs',
    TIMING: '/api/timing',
  },
  TIMEOUT: 30000, // 30 seconds
};

export const SERVICE_CONFIG = {
  API: {
    TIMEOUT: 30000,
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY: 1000,
  },
  GEMINI: {
    MODEL: 'gemini-2.5-pro',
    TEST_MODEL: 'gemini-2.5-pro',
    KEY_PREFIX: 'AIza',
    MIN_KEY_LENGTH: 35,
    MAX_TOKENS: 4096,
    TEMPERATURE: 0.7,
  },
  NOTEBOOK: {
    AUTOSAVE_DELAY: 1000,
    MAX_CELLS: 100,
    DEFAULT_CELL_TYPE: 'code',
  },
};

export const AI_PROMPTS = {
  SYSTEM_PROMPT: 'You are an expert in 8085 microprocessor assembly programming. Provide clear, concise answers with code examples when appropriate.',

  ERROR_EXPLANATION: `You are an expert 8085 microprocessor assembly language programmer. A user has encountered an error in their 8085 assembly code. Please analyze the error and provide a helpful explanation and solution.

Code:
{code}

Error:
{error}

Please provide:
1. A clear explanation of what the error means
2. The likely cause of the error
3. A corrected version of the code if applicable
4. Any additional tips or best practices

Keep your response concise but informative.`,

  ERROR_ANALYSIS: `You are an expert in 8085 microprocessor assembly programming. 
A student has encountered an error in their code. Please explain what went wrong and how to fix it.

Code:
\`\`\`assembly
{code}
\`\`\`

Error: {error_type} on line {error_line}
Message: {error_message}

Please provide:
1. A clear explanation of what caused the error
2. How to fix it
3. A corrected version of the code if applicable

Keep your response concise and educational.`,

  CODE_EXPLANATION: `You are an expert in 8085 microprocessor assembly programming.
Please explain what the following code does:
\`\`\`assembly
{code}
\`\`\`
Provide a clear, line-by-line explanation that's easy for students to understand.`,
};
