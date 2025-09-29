// src/components/dashboard/MetricCard.jsx
import './MetricCard.css';

export default function MetricCard({ title, value, icon, color }) {
  return (
    <div className="metric-card" style={{ borderLeftColor: color }}>
      <div className="metric-icon" style={{ backgroundColor: color }}>
        {icon}
      </div>
      <div className="metric-content">
        <h3>{title}</h3>
        <p className="metric-value">{value}</p>
      </div>
    </div>
  );
}