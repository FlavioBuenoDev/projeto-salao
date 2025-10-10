// src/components/dashboard/AgendamentosChart.jsx

import PropTypes from "prop-types";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
);

function AgendamentosChart({ agendamentosData, clientesData }) {
  const chartData = {
    labels: agendamentosData.map((item) => item.data_formatada),
    datasets: [
      {
        label: "Agendamentos",
        data: agendamentosData.map((item) => item.quantidade),
        borderColor: "#3498db",
        backgroundColor: "rgba(52, 152, 219, 0.1)",
        tension: 0.4,
        fill: true,
      },
      {
        label: "Clientes Novos",
        data: clientesData.map((item) => item.quantidade),
        borderColor: "#2ecc71",
        backgroundColor: "rgba(46, 204, 113, 0.1)",
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "📈 Agendamentos e Clientes Novos",
        font: {
          size: 16,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
}

AgendamentosChart.propTypes = {
  agendamentosData: PropTypes.arrayOf(PropTypes.object).isRequired,
  clientesData: PropTypes.arrayOf(PropTypes.object).isRequired,
};

export default AgendamentosChart;
