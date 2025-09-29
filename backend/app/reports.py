# app/reports.py
from sqlmodel import Session, select, func, and_
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from app.models import Agendamento, Cliente, User

class ReportService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_general_stats(self) -> Dict[str, Any]:
        """Estatísticas gerais do sistema"""
        # Total de clientes
        total_clientes = self.session.exec(select(func.count(Cliente.id))).first()
        
        # Total de agendamentos
        total_agendamentos = self.session.exec(select(func.count(Agendamento.id))).first()
        
        # Agendamentos do mês atual
        hoje = datetime.now()
        inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        agendamentos_mes = self.session.exec(
            select(func.count(Agendamento.id)).where(
                Agendamento.data_hora >= inicio_mes
            )
        ).first()
        
        # Clientes novos este mês
        clientes_novos_mes = self.session.exec(
            select(func.count(Cliente.id)).where(
                Cliente.created_at >= inicio_mes
            )
        ).first()
        
        # Agendamentos de hoje
        inicio_hoje = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
        fim_hoje = hoje.replace(hour=23, minute=59, second=59, microsecond=999999)
        agendamentos_hoje = self.session.exec(
            select(func.count(Agendamento.id)).where(
                and_(
                    Agendamento.data_hora >= inicio_hoje,
                    Agendamento.data_hora <= fim_hoje
                )
            )
        ).first()
        
        return {
            "total_clientes": total_clientes or 0,
            "total_agendamentos": total_agendamentos or 0,
            "agendamentos_mes": agendamentos_mes or 0,
            "clientes_novos_mes": clientes_novos_mes or 0,
            "agendamentos_hoje": agendamentos_hoje or 0,
            "taxa_ocupacao": self._calcular_taxa_ocupacao()
        }
    
    def _calcular_taxa_ocupacao(self) -> float:
        """Calcula taxa de ocupação média (simulação)"""
        # Supondo 8 horas de trabalho por dia, 20 dias por mês
        horas_trabalho_mes = 8 * 20
        # Supondo 1 hora por serviço
        horas_agendadas = self.session.exec(
            select(func.count(Agendamento.id)).where(
                Agendamento.data_hora >= datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            )
        ).first() or 0
        
        taxa = (horas_agendadas / horas_trabalho_mes) * 100 if horas_trabalho_mes > 0 else 0
        return round(taxa, 1)
    
    def get_agendamentos_por_servico(self, dias: int = 30) -> List[Dict[str, Any]]:
        """Agendamentos agrupados por serviço"""
        data_inicio = datetime.now() - timedelta(days=dias)
        
        statement = select(
            Agendamento.servico,
            func.count(Agendamento.id).label('quantidade')
        ).where(
            Agendamento.data_hora >= data_inicio
        ).group_by(Agendamento.servico)
        
        resultados = self.session.exec(statement).all()
        
        return [
            {
                "servico": servico,
                "quantidade": quantidade,
                "percentual": round((quantidade / sum(r[1] for r in resultados)) * 100, 1) if resultados else 0
            }
            for servico, quantidade in resultados
        ]
    
    def get_agendamentos_por_dia(self, dias: int = 7) -> List[Dict[str, Any]]:
        """Agendamentos por dia (últimos N dias)"""
        data_inicio = datetime.now() - timedelta(days=dias)
        
        statement = select(
            func.date(Agendamento.data_hora).label('data'),
            func.count(Agendamento.id).label('quantidade')
        ).where(
            Agendamento.data_hora >= data_inicio
        ).group_by(func.date(Agendamento.data_hora))
        
        resultados = self.session.exec(statement).all()
        
        # Preencher dias sem agendamentos
        dados_completos = []
        for i in range(dias + 1):
            data = (datetime.now() - timedelta(days=dias - i)).date()
            quantidade = next((q for d, q in resultados if d == data), 0)
            dados_completos.append({
                "data": data.isoformat(),
                "data_formatada": data.strftime("%d/%m"),
                "quantidade": quantidade
            })
        
        return dados_completos
    
    def get_clientes_novos_por_periodo(self, dias: int = 30) -> List[Dict[str, Any]]:
        """Clientes novos por período"""
        data_inicio = datetime.now() - timedelta(days=dias)
        
        statement = select(
            func.date(Cliente.created_at).label('data'),
            func.count(Cliente.id).label('quantidade')
        ).where(
            Cliente.created_at >= data_inicio
        ).group_by(func.date(Cliente.created_at))
        
        resultados = self.session.exec(statement).all()
        
        # Preencher dias sem novos clientes
        dados_completos = []
        for i in range(dias + 1):
            data = (datetime.now() - timedelta(days=dias - i)).date()
            quantidade = next((q for d, q in resultados if d == data), 0)
            dados_completos.append({
                "data": data.isoformat(),
                "data_formatada": data.strftime("%d/%m"),
                "quantidade": quantidade
            })
        
        return dados_completos
    
    def get_agendamentos_por_mes(self, meses: int = 12) -> List[Dict[str, Any]]:
        """Agendamentos por mês (últimos N meses)"""
        data_inicio = datetime.now() - timedelta(days=meses*30)
        
        statement = select(
            func.strftime('%Y-%m', Agendamento.data_hora).label('mes'),
            func.count(Agendamento.id).label('quantidade')
        ).where(
            Agendamento.data_hora >= data_inicio
        ).group_by(func.strftime('%Y-%m', Agendamento.data_hora))
        
        resultados = self.session.exec(statement).all()
        
        return [
            {
                "mes": mes,
                "mes_formatado": datetime.strptime(mes + '-01', '%Y-%m-%d').strftime('%b/%Y'),
                "quantidade": quantidade
            }
            for mes, quantidade in resultados
        ]
    
    def get_top_clientes(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Top clientes por número de agendamentos"""
        statement = select(
            Cliente.nome,
            Cliente.email,
            func.count(Agendamento.id).label('total_agendamentos')
        ).join(Agendamento).group_by(Cliente.id).order_by(
            func.count(Agendamento.id).desc()
        ).limit(limite)
        
        resultados = self.session.exec(statement).all()
        
        return [
            {
                "nome": nome,
                "email": email,
                "total_agendamentos": total_agendamentos,
                "posicao": idx + 1
            }
            for idx, (nome, email, total_agendamentos) in enumerate(resultados)
        ]