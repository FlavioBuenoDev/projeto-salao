import { useState, useEffect } from "react";
import axios from "axios";
import Loading from "../components/Loading/Loading";
import "./Agendamentos.css";

function Agendamentos() {
  // Estados para dados e carregamento
  const [agendamentos, setAgendamentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para filtros
  const [filtroData, setFiltroData] = useState("");
  const [filtroServico, setFiltroServico] = useState("");

  // Estados para ordenação
  const [ordenacao, setOrdenacao] = useState("data");
  const [ordemCrescente, setOrdemCrescente] = useState(true);

  // Estados para paginação
  const [paginaAtual, setPaginaAtual] = useState(1);
  const [itensPorPagina] = useState(5);

  // Buscar agendamentos da API
  useEffect(() => {
    const fetchAgendamentos = async () => {
      try {
        const response = await axios.get("http://localhost:8000/agendamentos/");
        setAgendamentos(response.data);
        setLoading(false);
      } catch (err) {
        setError("Erro ao carregar agendamentos: " + err.message);
        setLoading(false);
      }
    };

    fetchAgendamentos();
  }, []);

  // Função para aplicar filtros
  const aplicarFiltros = (lista) => {
    let resultados = lista;

    if (filtroData) {
      resultados = resultados.filter((agendamento) => {
        const dataAgendamento = new Date(agendamento.data_hora)
          .toISOString()
          .split("T")[0];
        return dataAgendamento === filtroData;
      });
    }

    if (filtroServico) {
      resultados = resultados.filter((agendamento) =>
        agendamento.servico.toLowerCase().includes(filtroServico.toLowerCase()),
      );
    }

    return resultados;
  };

  // Função para ordenar agendamentos
  const ordenarAgendamentos = (lista) => {
    return [...lista].sort((a, b) => {
      let valorA, valorB;

      if (ordenacao === "data") {
        valorA = new Date(a.data_hora);
        valorB = new Date(b.data_hora);
      } else {
        valorA = a.servico.toLowerCase();
        valorB = b.servico.toLowerCase();
      }

      if (ordemCrescente) {
        return valorA > valorB ? 1 : -1;
      } else {
        return valorA < valorB ? 1 : -1;
      }
    });
  };

  // Aplicar filtros e ordenação
  const agendamentosFiltrados = aplicarFiltros(agendamentos);
  const agendamentosOrdenados = ordenarAgendamentos(agendamentosFiltrados);

  // Calcular paginação
  const indexUltimoItem = paginaAtual * itensPorPagina;
  const indexPrimeiroItem = indexUltimoItem - itensPorPagina;
  const agendamentosPaginaAtual = agendamentosOrdenados.slice(
    indexPrimeiroItem,
    indexUltimoItem,
  );
  const totalPaginas = Math.ceil(agendamentosOrdenados.length / itensPorPagina);

  // Funções de paginação
  const proximaPagina = () => {
    if (paginaAtual < totalPaginas) {
      setPaginaAtual(paginaAtual + 1);
    }
  };

  const paginaAnterior = () => {
    if (paginaAtual > 1) {
      setPaginaAtual(paginaAtual - 1);
    }
  };

  // Removido: irParaPagina não é utilizada

  // Função para limpar filtros
  const limparFiltros = () => {
    setFiltroData("");
    setFiltroServico("");
    setPaginaAtual(1);
  };

  // Resetar paginação quando filtros mudarem
  useEffect(() => {
    setPaginaAtual(1);
  }, [filtroData, filtroServico, ordenacao, ordemCrescente]);

  if (loading) return <Loading message="Carregando agendamentos..." />;

  if (error)
    return (
      <div className="error-message">
        <p>{error}</p>
        <button onClick={() => window.location.reload()} className="btn-limpar">
          Tentar Novamente
        </button>
      </div>
    );

  return (
    <div className="agendamentos-container">
      <h1>Agendamentos</h1>

      {/* Seção de Filtros */}
      <div className="filtros-section">
        <h2>Filtros</h2>

        <div className="filtros-container">
          <div className="filtro-group">
            <label htmlFor="filtro-data">Filtrar por Data:</label>
            <input
              type="date"
              id="filtro-data"
              value={filtroData}
              onChange={(e) => setFiltroData(e.target.value)}
              className="filtro-input"
            />
          </div>

          <div className="filtro-group">
            <label htmlFor="filtro-servico">Filtrar por Serviço:</label>
            <input
              type="text"
              id="filtro-servico"
              value={filtroServico}
              onChange={(e) => setFiltroServico(e.target.value)}
              placeholder="Digite o nome do serviço"
              className="filtro-input"
            />
          </div>

          <button onClick={limparFiltros} className="btn-limpar">
            Limpar Filtros
          </button>
        </div>

        {/* Controles de Ordenação */}
        <div className="ordenacao-section">
          <label htmlFor="ordenacao">Ordenar por:</label>
          <select
            id="ordenacao"
            value={ordenacao}
            onChange={(e) => setOrdenacao(e.target.value)}
            className="ordenacao-select"
          >
            <option value="data">Data/Hora</option>
            <option value="servico">Serviço</option>
          </select>

          <button
            onClick={() => setOrdemCrescente(!ordemCrescente)}
            className="btn-ordenacao"
          >
            {ordemCrescente ? "↑ Crescente" : "↓ Decrescente"}
          </button>
        </div>

        <div className="info-filtros">
          <p>
            Mostrando {agendamentosOrdenados.length} de {agendamentos.length}{" "}
            agendamentos
            {filtroData || filtroServico ? " (filtrados)" : ""}
          </p>
        </div>
      </div>

      {/* Lista de Agendamentos */}
      {agendamentosOrdenados.length === 0 ? (
        <div className="sem-resultados">
          <p>Nenhum agendamento encontrado.</p>
          {(filtroData || filtroServico) && (
            <button onClick={limparFiltros} className="btn-limpar">
              Ver todos os agendamentos
            </button>
          )}
        </div>
      ) : (
        <>
          <div className="agendamentos-list">
            {agendamentosPaginaAtual.map((agendamento) => (
              <div key={agendamento.id} className="agendamento-card">
                <div className="agendamento-header">
                  <h3>{agendamento.servico}</h3>
                  <span className="agendamento-id">#{agendamento.id}</span>
                </div>

                <div className="agendamento-details">
                  <p>
                    <strong>📅 Data/Hora:</strong>{" "}
                    {new Date(agendamento.data_hora).toLocaleString("pt-BR")}
                  </p>
                  <p>
                    <strong>👤 Cliente ID:</strong> {agendamento.cliente_id}
                  </p>
                  {agendamento.observacoes && (
                    <p>
                      <strong>📝 Observações:</strong> {agendamento.observacoes}
                    </p>
                  )}
                </div>

                <div className="agendamento-actions">
                  <button className="btn-editar">Editar</button>
                  <button className="btn-cancelar">Cancelar</button>
                </div>
              </div>
            ))}
          </div>

          {/* Controles de Paginação */}
          {totalPaginas > 1 && (
            <div className="paginacao">
              <button
                onClick={paginaAnterior}
                disabled={paginaAtual === 1}
                className="btn-paginacao"
              >
                Anterior
              </button>

              <div className="info-paginacao">
                Página {paginaAtual} de {totalPaginas}
              </div>

              <button
                onClick={proximaPagina}
                disabled={paginaAtual === totalPaginas}
                className="btn-paginacao"
              >
                Próxima
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default Agendamentos;
