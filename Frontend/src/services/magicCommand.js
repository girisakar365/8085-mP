import api from './api';
import geminiService from './geminiService';
import { parseDocumentation } from '../utils/documentationParser';
import useSettingsStore from '../stores/settingsStore';

export const MAGIC_COMMANDS = {
  HELP: "@help",
  DOCS: "@docs",
  TIMING_DIAGRAM: "@timing",
  ASSEMBLE: "@assemble",
  ASK_AI: "@ask",
  RESET: "@reset"
};

export const handleMagicCommand = async (command, apiKey = null) => {
  const trimmed = command.trim();
  const spaceIdx = trimmed.indexOf(' ');
  const newlineIdx = trimmed.indexOf('\n');
  const splitIdx = (spaceIdx === -1) ? newlineIdx : ((newlineIdx === -1) ? spaceIdx : Math.min(spaceIdx, newlineIdx));

  let cmd, args;
  if (splitIdx === -1) {
    cmd = trimmed;
    args = '';
  } else {
    cmd = trimmed.slice(0, splitIdx);
    args = trimmed.slice(splitIdx).trim();
  }

  try {
    switch (cmd) {
      case MAGIC_COMMANDS.HELP:
        return { type: 'help' };

      case MAGIC_COMMANDS.RESET:
        return await handleResetCommand();

      case MAGIC_COMMANDS.ASK_AI:
        return await handleAskAICommand(args, apiKey);

      case MAGIC_COMMANDS.DOCS:
        return await handleDocsCommand(args);

      case MAGIC_COMMANDS.TIMING_DIAGRAM:
        return await handleTimingDiagramCommand(args);

      case MAGIC_COMMANDS.ASSEMBLE:
        return await handleAssembleCommand(args);

      default:
        return {
          type: 'error',
          data: { message: `Unknown magic command: ${cmd}. Type ${MAGIC_COMMANDS.HELP} for a list of available commands.` }
        };
    }
  } catch (error) {
    return {
      type: 'error',
      data: { message: 'Error executing command: ' + error.message }
    };
  }
};

const handleResetCommand = async () => {
  try {
    const result = await api.reset();
    if (result.success) {
      return {
        type: 'success',
        data: {
          message: 'Reset Successful: Processor state has been reset to default values. Check the Processor State panel to see the updated values.'
        }
      };
    }
    throw new Error('Reset failed');
  } catch (error) {
    return {
      type: 'error',
      data: { message: 'Failed to reset processor: ' + error.message }
    };
  }
};

const handleAskAICommand = async (args, apiKey) => {
  if (!args) {
    return {
      type: 'error',
      data: {
        title: 'Usage Error',
        message: `Usage: ${MAGIC_COMMANDS.ASK_AI} [question]\nExample: ${MAGIC_COMMANDS.ASK_AI} How does MOV instruction work?`
      }
    };
  }

  const currentApiKey = apiKey || useSettingsStore.getState().geminiApiKey;

  if (!currentApiKey) {
    return {
      type: 'warning',
      data: {
        message: 'API Key Required: AI features require a Google Gemini API key. Click "Configure AI Key" in the settings menu to set it up.'
      }
    };
  }

  geminiService.initialize(currentApiKey);

  try {
    const response = await geminiService.askAI(args);
    return {
      type: 'ai-response',
      data: { response }
    };
  } catch (error) {
    const showKeyButton = error.message.includes('API key');
    return {
      type: showKeyButton ? 'warning' : 'error',
      data: {
        message: `AI Service Error: ${error.message}${showKeyButton ? '\nPlease configure your Google Gemini API key.' : ''}`
      }
    };
  }
};

const handleDocsCommand = async (args) => {
  if (!args) {
    return {
      type: 'error',
      data: {
        title: 'Usage Error',
        message: `Usage: ${MAGIC_COMMANDS.DOCS} [instruction]\nExample: ${MAGIC_COMMANDS.DOCS} MOV`
      }
    };
  }

  try {
    const result = await api.getDocs(args.toUpperCase());
    
    if (result && result.error) {
      return {
        type: 'error',
        data: {
          title: 'Documentation Error',
          message: result.message,
          error: result.details
        }
      };
    }
    
    if (result && result.documentation) {
      const docText = result.documentation.trim();
      if (docText.startsWith('Invalid Instruction') || docText.includes('not found')) {
        return {
          type: 'error',
          data: {
            title: 'Documentation Error',
            message: docText,
            error: {
              instruction: result.instruction || args.toUpperCase(),
              hint: 'Valid instructions: MOV, MVI, LDA, STA, ADD, SUB, etc.'
            }
          }
        };
      }
      
      const sections = parseDocumentation(result.documentation);
      return {
        type: 'docs',
        data: {
          instruction: result.instruction,
          sections
        }
      };
    }
    
    return {
      type: 'error',
      data: { 
        title: 'Documentation Error',
        message: 'Documentation not found for instruction: ' + args 
      }
    };
  } catch (error) {
    return {
      type: 'error',
      data: { 
        title: 'Documentation Error',
        message: 'Failed to fetch documentation: ' + error.message 
      }
    };
  }
};

const handleTimingDiagramCommand = async (args) => {
  if (!args) {
    return {
      type: 'error',
      data: {
        message: `Usage: ${MAGIC_COMMANDS.TIMING_DIAGRAM} [instruction]\nExample: ${MAGIC_COMMANDS.TIMING_DIAGRAM} MOV`
      }
    };
  }

  try {
    const result = await api.getTimingDiagram(args.toUpperCase());
    
    if (result && result.error) {
      return {
        type: 'error',
        data: {
          title: 'Timing Diagram Error',
          message: result.message,
          error: result.details
        }
      };
    }
    
    if (result && result.detail) {
      return {
        type: 'error',
        data: {
          title: 'Timing Diagram Error',
          message: result.detail,
          error: {
            instruction: args.toUpperCase(),
            hint: 'Valid instructions: MOV, MVI, ADD, SUB, LDA, STA, etc.'
          }
        }
      };
    }
    
    if (result && result.diagram) {
      return {
        type: 'timing-diagram',
        data: {
          instruction: result.instruction,
          diagram: result.diagram
        }
      };
    }
    
    return {
      type: 'error',
      data: { 
        title: 'Timing Diagram Error',
        message: 'Failed to generate timing diagram for: ' + args 
      }
    };
  } catch (error) {
    return {
      type: 'error',
      data: { 
        title: 'Timing Diagram Error',
        message: 'Failed to fetch timing diagram: ' + error.message 
      }
    };
  }
};

const handleAssembleCommand = async (args) => {
  if (!args) {
    return {
      type: 'error',
      data: {
        message: `Usage: ${MAGIC_COMMANDS.ASSEMBLE} [instructions]\nExample: ${MAGIC_COMMANDS.ASSEMBLE} MVI A, 05H\nADD B`
      }
    };
  }

  const result = await api.assemble(args);
  
  if (result && result.status === 'success' && result.label && result.data) {
    return {
      type: 'assembly-table',
      data: {
        labels: result.label,
        rows: result.data
      }
    };
  } else if (result && result.status === 'error') {
    return {
      type: 'error',
      data: {
        title: 'Assembly Error',
        message: result.details.message,
        error: result.details.details
      }
    };
  }
  
  return {
    type: 'error',
    data: {
      message: 'Unable to process the assembly code. Please check your syntax and try again.'
    }
  };
};
