import { useState, useEffect } from 'react'
import axios from 'axios'


function Agendamentos() {
  const [agendamentos, setAgendamentos] = useState()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        console.log('Iniciando requisição para API...')
        const response = await axios.get('http://localhost:8000/agendamentos/')
        console.log('Resposta recebida:', response)
        console.log('Dados:', response.data)
        
        setAgendamentos(response.data)
        setLoading(false)
      } catch (err) {
        console.error('Erro detalhado:', err)
        console.error('Mensagem:', err.message)
        console.error('Resposta do servidor:', err.response)
        
        setError(`Erro: ${err.message}. Verifique se o backend está rodando na porta 8000.`)
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) return <div style={{ padding: '20px' }}><h2>Carregando...</h2></div>
  if (error) return <div style={{ padding: '20px' }}><h2>Erro</h2><p>{error}</p></div>

  return (
    <div style={{ padding: '20px' }}>
      <h1>Agendamentos</h1>
      {agendamentos.length === 0 ? (
        <p>Nenhum agendamento encontrado.</p>
      ) : (
        <div>
          <p>Total: {agendamentos.length} agendamento(s)</p>
          <ul>
            {agendamentos.map(agendamento => (
              <li key={agendamento.id} style={{ marginBottom: '15px', padding: '10px', border: '1px solid #ccc' }}>
                <strong>ID:</strong> {agendamento.id} <br />
                <strong>Cliente ID:</strong> {agendamento.cliente_id} <br />
                <strong>Serviço:</strong> {agendamento.servico} <br />
                <strong>Data/Hora:</strong> {new Date(agendamento.data_hora).toLocaleString('pt-BR')} <br />
                <strong>Observações:</strong> {agendamento.observacoes || 'Nenhuma'}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default Agendamentos