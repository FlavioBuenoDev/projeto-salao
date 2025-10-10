// src/components/dashboard/MetricCard.jsx
import PropTypes from "prop-types";
import "./MetricCard.css";

function MetricCard({ title, value, icon, color }) {
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

MetricCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  icon: PropTypes.node,
  color: PropTypes.string,
};

export default MetricCard;
