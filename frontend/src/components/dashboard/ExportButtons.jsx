import PropTypes from "prop-types";
import { useState } from "react";
import "./ExportButtons.css";

function ExportButtons({ token }) {
  const [exporting, setExporting] = useState("");

  const handleExport = async (tipo) => {
    try {
      setExporting(tipo);
      const response = await fetch(
        `http://localhost:8000/admin/reports/export/csv?tipo=${tipo}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        const filename =
          response.headers
            .get("Content-Disposition")
            ?.split("filename=")[1]
            ?.replace(/"/g, "") ||
          `${tipo}_${new Date().toISOString().split("T")[0]}.csv`;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      } else {
        alert("Erro ao exportar dados");
      }
    } catch (error) {
      console.error("Erro na exportação:", error);
      alert("Erro ao exportar dados");
    } finally {
      setExporting("");
    }
  };

  return (
    <div className="export-buttons">
      <h3>📤 Exportar Relatórios</h3>
      <div className="export-options">
        <button
          onClick={() => handleExport("clientes")}
          disabled={exporting === "clientes"}
          className="export-btn"
        >
          {exporting === "clientes"
            ? "⏳ Exportando..."
            : "👥 Exportar Clientes (CSV)"}
        </button>
        <button
          onClick={() => handleExport("agendamentos")}
          disabled={exporting === "agendamentos"}
          className="export-btn"
        >
          {exporting === "agendamentos"
            ? "⏳ Exportando..."
            : "📅 Exportar Agendamentos (CSV)"}
        </button>
        <button
          onClick={() => handleExport("servicos")}
          disabled={exporting === "servicos"}
          className="export-btn"
        >
          {exporting === "servicos"
            ? "⏳ Exportando..."
            : "💇 Exportar Serviços (CSV)"}
        </button>
      </div>
      <div className="export-info">
        <p>
          💡 Dica: Os arquivos CSV podem ser abertos no Excel ou Google Sheets para análise avançada.
        </p>
      </div>
    </div>
  );
}

ExportButtons.propTypes = {
  token: PropTypes.string.isRequired,
};

export default ExportButtons;
