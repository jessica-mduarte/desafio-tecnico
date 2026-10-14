import sqlite3
from pathlib import Path
import re

CAMINHO_BANCO = Path(__file__).resolve().parent / "database.db"

demandas = [
    {
        "titulo": "Computador não inicia",
        "descricao": "Erro ao iniciar o computador da recepção.",
        "data": "2026-10-01",
        "setor": "TI",
        "status": "Novo",
    },
    {
        "titulo": "Acesso ao sistema financeiro",
        "descricao": "Solicito acesso ao sistema financeiro.",
        "data": "2026-10-02",
        "setor": "Financeiro",
        "status": "Em andamento",
    },
    {
        "titulo": "Atualização de cadastro de colaborador",
        "descricao": "Atualizar os dados cadastrais de um colaborador.",
        "data": "2026-10-02",
        "setor": "Recursos Humanos",
        "status": "Concluído",
    },
    {
        "titulo": "Falha urgente no servidor",
        "descricao": "Urgente: servidor interno indisponível.",
        "data": "2026-10-03",
        "setor": "TI",
        "status": "Em andamento",
    },
    {
        "titulo": "Material para campanha",
        "descricao": "Solicitação de material para campanha promocional.",
        "data": "2026-10-03",
        "setor": "Marketing",
        "status": "Novo",
    },
    {
        "titulo": "Erro no relatório de vendas",
        "descricao": "Erro nos valores apresentados no relatório mensal.",
        "data": "2026-10-04",
        "setor": "Vendas",
        "status": "Novo",
    },
    {
        "titulo": "Solicitação de férias",
        "descricao": "Registrar solicitação de férias de colaborador.",
        "data": "2026-10-05",
        "setor": "Recursos Humanos",
        "status": "Concluído",
    },
    {
        "titulo": "Nota fiscal pendente",
        "descricao": "Verificar o lançamento de uma nota fiscal pendente.",
        "data": "2026-10-05",
        "setor": "Financeiro",
        "status": "Em andamento",
    },
    {
        "titulo": "Urgente: acesso bloqueado",
        "descricao": "Urgente: usuário bloqueado sem acesso ao sistema.",
        "data": "2026-10-06",
        "setor": "TI",
        "status": "Novo",
    },
    {
        "titulo": "Publicação nas redes sociais",
        "descricao": "Preparar publicação para as redes sociais.",
        "data": "2026-10-06",
        "setor": "Marketing",
        "status": "Concluído",
    },
    {
        "titulo": "Atualização de tabela de preços",
        "descricao": "Atualizar a tabela de preços dos produtos.",
        "data": "2026-10-07",
        "setor": "Vendas",
        "status": "Em andamento",
    },
    {
        "titulo": "Erro no cálculo de despesas",
        "descricao": "Erro no cálculo das despesas do departamento.",
        "data": "2026-10-07",
        "setor": "Financeiro",
        "status": "Novo",
    },
    {
        "titulo": "Solicitação de novo monitor",
        "descricao": "Solicito um monitor para a estação de trabalho.",
        "data": "2026-10-08",
        "setor": "TI",
        "status": "Concluído",
    },
    {
        "titulo": "Agendamento de treinamento",
        "descricao": "Organizar treinamento interno para a equipe.",
        "data": "2026-10-08",
        "setor": "Recursos Humanos",
        "status": "Em andamento",
    },
    {
        "titulo": "Campanha de lançamento",
        "descricao": "Criar materiais para o lançamento de produto.",
        "data": "2026-10-09",
        "setor": "Marketing",
        "status": "Novo",
    },
    {
        "titulo": "Cliente sem retorno",
        "descricao": "Urgente: cliente aguarda retorno sobre pedido.",
        "data": "2026-10-10",
        "setor": "Vendas",
        "status": "Em andamento",
    },
    {
        "titulo": "Reembolso de despesas",
        "descricao": "Solicitação de reembolso de despesas de viagem.",
        "data": "2026-10-10",
        "setor": "Financeiro",
        "status": "Concluído",
    },
    {
        "titulo": "Erro na impressora",
        "descricao": "Erro de impressão no equipamento compartilhado.",
        "data": "2026-10-11",
        "setor": "TI",
        "status": "Novo",
    },
    {
        "titulo": "Atualização de benefícios",
        "descricao": "Atualizar informações sobre benefícios internos.",
        "data": "2026-10-12",
        "setor": "Recursos Humanos",
        "status": "Novo",
    },
    {
        "titulo": "Relatório de desempenho comercial",
        "descricao": "Preparar relatório de desempenho comercial.",
        "data": "2026-10-13",
        "setor": "Vendas",
        "status": "Concluído",
    },
]

conexao = sqlite3.connect(CAMINHO_BANCO)

try:
    # Garante que a tabela exista sem apagar os registros.
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data_solicitacao TEXT NOT NULL,
            setor TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Novo',
            prioridade TEXT NOT NULL
        )
    """)

    inseridas = 0
    ignoradas = 0

    for demanda in demandas:
        # Evita duplicar os títulos deste conjunto de dados.
        existe = conexao.execute("""
            SELECT 1
            FROM tickets
            WHERE titulo = ?
            LIMIT 1
        """, (demanda["titulo"],)).fetchone()

        if existe:
            ignoradas += 1
            continue

        # Mantém a mesma regra de prioridade do Flask.
        descricao_busca = demanda["descricao"].casefold()

        if re.search(r"\b(urgente|erro)\b", descricao_busca):
            prioridade = "Alta"
        else:
            prioridade = "Normal"

        conexao.execute("""
            INSERT INTO tickets (
                titulo,
                descricao,
                data_solicitacao,
                setor,
                status,
                prioridade
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            demanda["titulo"],
            demanda["descricao"],
            demanda["data"],
            demanda["setor"],
            demanda["status"],
            prioridade
        ))

        inseridas += 1

    conexao.commit()

    print(f"Demandas inseridas: {inseridas}")
    print(f"Demandas ignoradas por já existirem: {ignoradas}")
    print("Dados fictícios preparados com sucesso!")

except sqlite3.Error:
    conexao.rollback()
    raise

finally:
    conexao.close()
