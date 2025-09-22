import { useState, useEffect } from 'react'
import axios from 'axios'
import Loading from '../components/Loading/Loading'

function Agendamentos() {
  const [agendamentos, setAgendamentos] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchAgendamentos = async () => {
      try {
        const response = await axios.get('http://localhost:8000/agendamentos/')
        setAgendamentos(response.data)
        setLoading(false)
      } catch (err) {
        setError('Erro ao carregar agendamentos: ' + err.message)
        setLoading(false)
      }
    }

    fetchAgendamentos()
  }, [])

  if (loading) return <Loading message="Carregando agendamentos..." />
  if (error) return <div className="error-message">{error}</div>

  return (
    <div>
      <h1>Agendamentos</h1>
      
      {agendamentos.length === 0 ? (
        <p>Não há agendamentos cadastrados.</p>
      ) : (
        <div className="agendamentos-list">
          {agendamentos.map(agendamento => (
            <div key={agendamento.id} className="agendamento-card">
              <h3>{agendamento.servico}</h3>
              <p><strong>Data/Hora:</strong> {new Date(agendamento.data_hora).toLocaleString('pt-BR')}</p>
              <p><strong>Cliente ID:</strong> {agendamento.cliente_id}</p>
              {agendamento.observacoes && (
                <p><strong>Observações:</strong> {agendamento.observacoes}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Agendamentos