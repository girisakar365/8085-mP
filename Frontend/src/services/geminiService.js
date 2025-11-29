import { GoogleGenAI } from '@google/genai';
import { SERVICE_CONFIG, AI_PROMPTS } from '../constants';

// Custom fetch for Electron to handle network requests properly
const customFetch = async (url, options = {}) => {
  try {
    const response = await fetch(url, {
      ...options,
      mode: 'cors',
      credentials: 'omit'
    });
    return response;
  } catch (error) {
    throw error;
  }
};

const SYSTEM_CONTEXT = AI_PROMPTS.SYSTEM_PROMPT;

class GeminiService {
  constructor() {
    this.genAI = null;
    this.chat = null;
    this.apiKey = null;
  }

  initialize(apiKey) {
    if (!apiKey) {
      this.genAI = null;
      this.chat = null;
      this.apiKey = null;
      return false;
    }

    try {
      this.apiKey = apiKey;
      this.genAI = new GoogleGenAI({ 
        apiKey,
        fetch: customFetch
      });
      
      this.chat = this.genAI.chats.create({
        model: SERVICE_CONFIG.GEMINI.MODEL,
        systemInstruction: SYSTEM_CONTEXT, 
      });

      return true;
    } catch (error) {
      this.genAI = null;
      this.chat = null;
      this.apiKey = null;
      return false;
    }
  }

  validateKey(key) {
    return key && key.startsWith(SERVICE_CONFIG.GEMINI.KEY_PREFIX) && key.length >= SERVICE_CONFIG.GEMINI.MIN_KEY_LENGTH;
  }

  async testApiKey(apiKey) {
    try {
      const testGenAI = new GoogleGenAI({ 
        apiKey,
        fetch: customFetch
      });
      
      const response = await testGenAI.models.generateContent({
        model: SERVICE_CONFIG.GEMINI.TEST_MODEL,
        contents: 'Just say hi only. Nothing else.',
      });
      
      if (response && response.text && response.text.length > 0) {
        return { valid: true };
      }
      
      return { valid: false, error: 'Invalid API response' };
    } catch (error) {
      const errorMsg = error.message || error.toString() || '';
      
      if (errorMsg.includes('API_KEY_INVALID') || errorMsg.includes('invalid') || errorMsg.includes('401')) {
        return { valid: false, error: 'The API key you entered is invalid. Please check and try again.' };
      } else if (errorMsg.includes('quota') || errorMsg.includes('429')) {
        return { valid: false, error: 'Rate limit exceeded. Please try again in a few moments.' };
      } else if (errorMsg.includes('ENOTFOUND') || errorMsg.includes('network') || errorMsg.includes('fetch') || errorMsg.includes('ECONNREFUSED') || errorMsg.includes('NetworkError') || errorMsg.includes('Failed to fetch')) {
        return { valid: false, error: 'Unable to connect. Please check your internet connection.' };
      } else if (errorMsg.includes('API key not valid') || errorMsg.includes('API key not found') || errorMsg.includes('403')) {
        return { valid: false, error: 'The API key you entered is not valid. Please verify your key.' };
      } else if (errorMsg.includes('not found') || errorMsg.includes('404')) {
        return { valid: false, error: 'Model not found. Please try again later.' };
      } else if (errorMsg.includes('400') || errorMsg.includes('Bad Request')) {
        return { valid: false, error: 'Invalid request. Please try again.' };
      }
      
      return { valid: false, error: `Validation failed: ${errorMsg.substring(0, 100)}` };
    }
  }

  async askAI(prompt, context = null) {
    if (!this.apiKey || !this.chat) {
      throw new Error('API key not configured. Please set your Google Gemini API key.');
    }

    try {
      const fullPrompt = context
        ? `Context: ${context}\n\nQuestion: ${prompt}`
        : prompt;

      const response = await this.chat.sendMessage({
        message: fullPrompt,
      });

      return response.text || '';
    } catch (error) {
      if (error.message?.includes('API_KEY_INVALID') || error.message?.includes('invalid API key')) {
        throw new Error('Invalid API key. Please check your Google Gemini API key.');
      } else if (error.message?.includes('quota') || error.message?.includes('429')) {
        throw new Error('Rate limit exceeded. Please try again in a moment.');
      } else if (error.message?.includes('not found') || error.message?.includes('404')) {
        throw new Error('AI model not available. The API version may have changed.');
      }

      throw error;
    }
  }

  resetChat() {
    if (this.genAI && this.apiKey) {
      try {
        this.chat = this.genAI.chats.create({
          model: SERVICE_CONFIG.GEMINI.TEST_MODEL,
          systemInstruction: SYSTEM_CONTEXT,
        });
      } catch (error) {
      }
    }
  }

  async explainError(code, error) {
    const prompt = AI_PROMPTS.ERROR_ANALYSIS
      .replace('{code}', code)
      .replace('{error_type}', error.type || 'Error')
      .replace('{error_line}', error.line || 'unknown')
      .replace('{error_message}', error.message || 'Unknown error');

    return await this.askAI(prompt);
  }

  async explainCode(code) {
    const prompt = AI_PROMPTS.CODE_EXPLANATION.replace('{code}', code);
    
    return await this.askAI(prompt);
  }
}

const geminiService = new GeminiService();
export default geminiService;
