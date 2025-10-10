// src/services/api.js
//const API_BASE_URL = 'http://localhost:8000';
const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Função para fazer requests com tratamento de erro
export const api = {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail || `HTTP error! status: ${response.status}`,
        );
      }

      return await response.json();
    } catch (error) {
      console.error("API request failed:", error);
      throw error;
    }
  },

  // Métodos específicos para autenticação
  async login(username, password) {
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    return this.request("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });
  },

  async register(userData) {
    return this.request("/register", {
      method: "POST",
      body: JSON.stringify(userData),
    });
  },

  async getProfile(token) {
    return this.request("/auth/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },
};
