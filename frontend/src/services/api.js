const api = {
  baseURL: 'http://localhost:8000/api',
  
  async request(endpoint, options = {}) {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }
    
    return response.json();
  },
  
  getConfigs: () => api.request('/configs'),
  createConfig: (data) => api.request('/configs', { method: 'POST', body: JSON.stringify(data) }),
  updateConfig: (id, data) => api.request(`/configs/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  triggerCall: (data) => api.request('/calls/trigger', { method: 'POST', body: JSON.stringify(data) }),
  getCalls: () => api.request('/calls'),
  getCall: (id) => api.request(`/calls/${id}`),
};
export default api;