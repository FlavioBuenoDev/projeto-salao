// src/components/PrivateRoute.jsx
import { useAuth } from '../contexts/AuthContext';
import { Navigate, useLocation } from 'react-router-dom';

export default function PrivateRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">Carregando...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // Redirecionar para login, guardando a página que tentou acessar
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}