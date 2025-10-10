// src/components/Header.jsx
import { useAuth } from "../contexts/AuthContext";
import "./Header.css";

export default function Header() {
  const { user, logout, isAuthenticated } = useAuth();

  const handleLogout = () => {
    if (window.confirm("Tem certeza que deseja sair?")) {
      logout();
    }
  };

  if (!isAuthenticated) {
    return null; // Não mostrar header se não estiver logado
  }

  return (
    <header className="header">
      <div className="header-content">
        <h1>Sistema de Agendamento</h1>

        <div className="header-user">
          <span>Olá, {user?.username}</span>
          <button onClick={handleLogout} className="logout-button">
            Sair
          </button>
        </div>
      </div>
    </header>
  );
}
