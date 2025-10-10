// src/pages/Dashboard.jsx
import { useState, useEffect } from "react";
import { useAuth } from "../contexts/AuthContext";
import { api } from "../services/api";
import MetricCard from "../components/dashboard/MetricCard";
import ServicosChart from "../components/dashboard/ServicosChart";
import AgendamentosChart from "../components/dashboard/AgendamentosChart";
import TopClientes from "../components/dashboard/TopClientes";
import ExportButtons from "../components/dashboard/ExportButtons";
import "./Dashboard.css";

export default function Dashboard() {
  const { token } = useAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDashboardData();
  }, [loadDashboardData]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const data = await api.request("/admin/reports/dashboard", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setDashboardData(data);
    } catch (err) {
      setError("Erro ao carregar dados do dashboard");
      console.error("Erro:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner">📊 Carregando Dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>{error}</p>
        <button onClick={loadDashboardData}>Tentar Novamente</button>
      </div>
    );
  }

  const {
    estatisticas_gerais,
    agendamentos_por_servico,
    agendamentos_diarios,
    clientes_novos,
    top_clientes,
  } = dashboardData;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>📊 Dashboard Administrativo</h1>
        <p>Visão geral do seu salão de beleza</p>
      </div>

      {/* Cards de Métricas */}
      <div className="metrics-grid">
        <MetricCard
          title="Total de Clientes"
          value={estatisticas_gerais.total_clientes}
          icon="👥"
          color="#3498db"
        />
        <MetricCard
          title="Agendamentos Totais"
          value={estatisticas_gerais.total_agendamentos}
          icon="📅"
          color="#2ecc71"
        />
        <MetricCard
          title="Agendamentos Este Mês"
          value={estatisticas_gerais.agendamentos_mes}
          icon="📈"
          color="#9b59b6"
        />
        <MetricCard
          title="Clientes Novos (Mês)"
          value={estatisticas_gerais.clientes_novos_mes}
          icon="🆕"
          color="#e74c3c"
        />
        <MetricCard
          title="Agendamentos Hoje"
          value={estatisticas_gerais.agendamentos_hoje}
          icon="✅"
          color="#f39c12"
        />
        <MetricCard
          title="Taxa de Ocupação"
          value={`${estatisticas_gerais.taxa_ocupacao}%`}
          icon="📊"
          color="#1abc9c"
        />
      </div>

      {/* Gráficos e Tabelas */}
      <div className="charts-grid">
        <div className="chart-container">
          <ServicosChart data={agendamentos_por_servico} />
        </div>
        <div className="chart-container">
          <AgendamentosChart
            agendamentosData={agendamentos_diarios}
            clientesData={clientes_novos}
          />
        </div>
        <div className="chart-container">
          <TopClientes data={top_clientes} />
        </div>
      </div>

      {/* Botões de Exportação */}
      <div className="export-section">
        <ExportButtons token={token} />
      </div>
    </div>
  );
}
