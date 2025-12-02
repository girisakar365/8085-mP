import { API_CONFIG, SERVICE_CONFIG } from '../../constants';

// Default fallback port
const DEFAULT_PORT = 8085;
const DEFAULT_HOST = "127.0.0.1";

// Cache for the backend URL
let cachedBackendUrl = null;

/**
 * Get the backend URL dynamically.
 * In Tauri, retrieves from Rust. Otherwise uses default.
 */
async function getBackendUrl() {
  // Return cached URL if available
  if (cachedBackendUrl) {
    return cachedBackendUrl;
  }

  // Check if running in Tauri
  if (window.__TAURI__) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      const url = await invoke('get_backend_url');
      cachedBackendUrl = url;
      console.log('Backend URL from Tauri:', url);
      return url;
    } catch (e) {
      console.warn('Failed to get backend URL from Tauri, using default:', e);
    }
  }

  // Fallback to default
  cachedBackendUrl = `http://${DEFAULT_HOST}:${DEFAULT_PORT}`;
  return cachedBackendUrl;
}

/**
 * Reset the cached backend URL (useful for reconnection attempts)
 */
export function resetBackendUrlCache() {
  cachedBackendUrl = null;
}

class ApiService {
  constructor() {
    this.baseUrl = null;
    this.initPromise = this._init();
  }

  async _init() {
    this.baseUrl = await getBackendUrl();
  }

  async _ensureInitialized() {
    if (!this.baseUrl) {
      await this.initPromise;
    }
  }

  async _fetch(endpoint, options = {}) {
    await this._ensureInitialized();
    
    const url = `${this.baseUrl}${endpoint}`;
    const timeout = options.timeout || SERVICE_CONFIG.API.TIMEOUT;
    
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error.name === 'AbortError') {
        throw new Error(`Request timeout after ${timeout}ms`);
      }
      throw error;
    }
  }

  async execute(code) {
    try {
      const response = await this._fetch(API_CONFIG.ENDPOINTS.EXECUTE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        return {
          error: true,
          message: 'Server error occurred during execution',
          details: {
            instruction: 'Unknown',
            position: 'Unknown',
            line: code,
            hint: 'Please check your code syntax and try again'
          }
        };
      }
      
      return response.json();
    } catch (error) {
      return {
        error: true,
        message: error.message || 'Failed to connect to backend',
        details: {
          instruction: 'Unknown',
          position: 'Unknown',
          line: code,
          hint: 'Please ensure the backend server is running'
        }
      };
    }
  }

  async assemble(code) {
    try {
      const response = await this._fetch(API_CONFIG.ENDPOINTS.ASSEMBLE, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })  
      });
      return response.json();
    } catch (error) {
      return { error: true, message: error.message };
    }
  }

  async reset() {
    try {
      const response = await this._fetch(API_CONFIG.ENDPOINTS.RESET, {
        method: 'POST'
      });
      return response.json();
    } catch (error) {
      return { error: true, message: error.message };
    }
  }

  async getDocs(instruction) {
    try {
      const response = await this._fetch(`${API_CONFIG.ENDPOINTS.DOCS}/${instruction}`);
      return response.json();
    } catch (error) {
      return { error: true, message: error.message };
    }
  }

  async getTimingDiagram(instruction) {
    try {
      const response = await this._fetch(`${API_CONFIG.ENDPOINTS.TIMING}/${instruction}`);
      return response.json();
    } catch (error) {
      return { error: true, message: error.message };
    }
  }

  async healthCheck() {
    try {
      const response = await this._fetch(API_CONFIG.ENDPOINTS.HEALTH, {
        timeout: 5000
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  async getConfig() {
    try {
      const response = await this._fetch('/config');
      return response.json();
    } catch (error) {
      return null;
    }
  }
}

const api = new ApiService();
export default api;
