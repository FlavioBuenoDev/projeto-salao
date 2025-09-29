// src/components/dashboard/TopClientes.jsx
import './TopClientes.css';

export default function TopClientes({ data }) {
  const getMedal = (posicao) => {
    switch(posicao) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return '⭐';
    }
  };

  return (
    <div className="top-clientes">
      <h3>🏆 Top Clientes</h3>
      <div className="clientes-list">
        {data.map(cliente => (
          <div key={cliente.email} className="cliente-item">
            <div className="cliente-medal">
              {getMedal(cliente.posicao)}
            </div>
            <div className="cliente-info">
              <strong>{cliente.nome}</strong>
              <span>{cliente.email}</span>
            </div>
            <div className="cliente-stats">
              <span className="agendamentos-count">
                {cliente.total_agendamentos} agendamentos
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}