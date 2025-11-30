import Groq from 'groq-sdk';
import { SERVICE_CONFIG, AI_PROMPTS } from '../../constants';

const SYSTEM_CONTEXT = AI_PROMPTS.SYSTEM_PROMPT;

// Default model - using a reliable Groq model
const DEFAULT_MODEL = 'llama-3.1-8b-instant';

class GroqService {
  constructor() {
    this.groq = null;
    this.apiKey = null;
    this.chatHistory = [];
    this.currentModel = DEFAULT_MODEL;
  }

  initialize(apiKey) {
    if (!apiKey) {
      this.groq = null;
      this.apiKey = null;
      return false;
    }

    try {
      this.apiKey = apiKey;
      this.groq = new Groq({
        apiKey,
        dangerouslyAllowBrowser: true
      });
      
      // Initialize chat history with system message
      this.chatHistory = [
        {
          role: 'system',
          content: SYSTEM_CONTEXT
        }
      ];

      return true;
    } catch (error) {
      this.groq = null;
      this.apiKey = null;
      return false;
    }
  }

  setModel(modelId) {
    this.currentModel = modelId || DEFAULT_MODEL;
  }

  getModel() {
    return this.currentModel;
  }

  validateKey(key) {
    return key && key.startsWith('gsk_') && key.length >= 20; // Groq API key format
  }

  async testApiKey(apiKey) {
    try {
      const testGroq = new Groq({
        apiKey,
        dangerouslyAllowBrowser: true
      });
      
      const completion = await testGroq.chat.completions.create({
        messages: [
          {
            role: 'user',
            content: 'Just say hi only. Nothing else.'
          }
        ],
        model: this.currentModel,
        max_tokens: 10
      });
      
      if (completion && completion.choices && completion.choices[0]?.message?.content) {
        return { valid: true };
      }
      
      return { valid: false, error: 'Invalid API response' };
    } catch (error) {
      console.error('Groq API test error:', error);
      const errorMsg = error.message || error.toString() || '';
      const statusCode = error.status || error.statusCode || '';
      
      // Check for specific HTTP status codes first
      if (statusCode === 401 || errorMsg.includes('401') || errorMsg.includes('Unauthorized')) {
        return { valid: false, error: 'The API key you entered is invalid. Please check and try again.' };
      } else if (statusCode === 403 || errorMsg.includes('403') || errorMsg.includes('Forbidden')) {
        return { valid: false, error: 'Access forbidden. Please verify your API key has the correct permissions.' };
      } else if (statusCode === 429 || errorMsg.includes('429') || errorMsg.includes('quota') || errorMsg.includes('rate limit')) {
        return { valid: false, error: 'Rate limit exceeded. Please try again in a few moments.' };
      } else if (statusCode === 404 || errorMsg.includes('404') || errorMsg.includes('not found')) {
        return { valid: false, error: 'Model not found. Please select a different model.' };
      } else if (statusCode === 400 || errorMsg.includes('400') || errorMsg.includes('Bad Request')) {
        return { valid: false, error: 'Invalid request. Please try again.' };
      } else if (errorMsg.includes('ENOTFOUND') || errorMsg.includes('network') || errorMsg.includes('ECONNREFUSED') || errorMsg.includes('NetworkError') || errorMsg.includes('Failed to fetch') || errorMsg.includes('fetch')) {
        return { valid: false, error: 'Unable to connect to Groq. Please check your internet connection.' };
      } else if (errorMsg.toLowerCase().includes('invalid_api_key') || errorMsg.toLowerCase().includes('invalid api key')) {
        return { valid: false, error: 'The API key you entered is invalid. Please check and try again.' };
      }
      
      // For any other error, show the actual error message for debugging
      return { valid: false, error: `Validation failed: ${errorMsg.substring(0, 150)}` };
    }
  }

  async askAI(prompt, context = null) {
    if (!this.apiKey || !this.groq) {
      throw new Error('API key not configured. Please set your Groq API key.');
    }

    try {
      const fullPrompt = context
        ? `Context: ${context}\n\nQuestion: ${prompt}`
        : prompt;

      // Add user message to chat history
      this.chatHistory.push({
        role: 'user',
        content: fullPrompt
      });

      const completion = await this.groq.chat.completions.create({
        messages: this.chatHistory,
        model: this.currentModel,
        max_tokens: 4096,
        temperature: 0.7
      });

      const response = completion.choices[0]?.message?.content || '';
      
      // Add assistant response to chat history
      if (response) {
        this.chatHistory.push({
          role: 'assistant',
          content: response
        });
      }

      return response;
    } catch (error) {
      if (error.message?.includes('invalid') || error.message?.includes('unauthorized')) {
        throw new Error('Invalid API key. Please check your Groq API key.');
      } else if (error.message?.includes('quota') || error.message?.includes('429')) {
        throw new Error('Rate limit exceeded. Please try again in a moment.');
      } else if (error.message?.includes('not found') || error.message?.includes('404')) {
        throw new Error('AI model not available. The API version may have changed.');
      }

      throw error;
    }
  }

  resetChat() {
    // Reset chat history to just the system message
    this.chatHistory = [
      {
        role: 'system',
        content: SYSTEM_CONTEXT
      }
    ];
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

const groqService = new GroqService();
export default groqService;