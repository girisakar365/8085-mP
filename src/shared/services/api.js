import { API_CONFIG, SERVICE_CONFIG } from '../../constants';

class ApiService {
  async execute(code) {
    const response = await fetch(`${API_CONFIG.ENDPOINTS.EXECUTE}`, {
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
  }

  async assemble(program) {
    const response = await fetch(`${API_CONFIG.ENDPOINTS.ASSEMBLE}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ program })
    });
    return response.json();
  }

  async reset() {
    const response = await fetch(`${API_CONFIG.ENDPOINTS.RESET}`, {
      method: 'POST'
    });
    return response.json();
  }

  async getDocs(instruction) {
    const response = await fetch(`${API_CONFIG.ENDPOINTS.DOCS}/${instruction}`);
    return response.json();
  }

  async getTimingDiagram(instruction) {
    const response = await fetch(`${API_CONFIG.ENDPOINTS.TIMING}/${instruction}`);
    return response.json();
  }
}

const api = new ApiService();
export default api;
