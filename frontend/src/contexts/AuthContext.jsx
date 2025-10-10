// src/contexts/AuthContext.jsx

import PropTypes from "prop-types";
import { createContext, useState, useContext, useEffect } from "react";
import { api } from "../services/api";

const AuthContext = createContext();

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth deve ser usado dentro de um AuthProvider");
  }
  return context;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem("token"));

  // Carregar dados do usuário quando o token mudar
  useEffect(() => {
    const loadUser = async () => {
      if (token) {
        try {
          const userData = await api.getProfile(token);
          setUser(userData);
        } catch (error) {
          console.error("Erro ao carregar usuário:", error);
          logout();
        }
      }
      setLoading(false);
    };

    loadUser();
  }, [token]);

  const login = async (username, password) => {
    try {
      const data = await api.login(username, password);
      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);
      const userData = await api.getProfile(data.access_token);
      setUser(userData);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.message || "Erro ao fazer login",
      };
    }
  };

  const register = async (userData) => {
    try {
      const result = await api.register(userData);
      if (result.user_id) {
        return await login(userData.username, userData.password);
      }
      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.message || "Erro ao registrar",
      };
    }
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  const value = {
    user,
    token,
    login,
    register,
    logout,
    loading,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

AuthProvider.propTypes = {
  children: PropTypes.node,
};
