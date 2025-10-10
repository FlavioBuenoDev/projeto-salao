import { Link } from "react-router-dom";
import "./Header.css";

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">Salão de Beleza</h1>
        <nav className="header-nav">
          <Link to="/" className="nav-link">
            Home
          </Link>
          <Link to="/agendamentos" className="nav-link">
            Agendamentos
          </Link>
          <Link to="/clientes" className="nav-link">
            Clientes
          </Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
