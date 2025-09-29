// src/components/dashboard/ServicosChart.jsx
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function ServicosChart({ data }) {
  const chartData = {
    labels: data.map(item => item.servico),
    datasets: [
      {
        data: data.map(item => item.quantidade),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
          '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
        ],
        borderWidth: 2,
        borderColor: '#fff'
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: true,
        text: '📊 Agendamentos por Serviço (Últimos 30 dias)',
        font: {
          size: 16
        }
      }
    }
  };

  return (
    <div>
      <Doughnut data={chartData} options={options} />
    </div>
  );
}