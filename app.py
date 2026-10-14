from flask import Flask, render_template, request, flash, redirect, url_for, Response
from pathlib import Path
import csv
import io
import re
import sqlite3
import unicodedata

app = Flask(__name__)
app.secret_key = "chave-temporaria"

# Mantém o banco na pasta do projeto, independentemente de onde o Flask for iniciado.
CAMINHO_BANCO = Path(__file__).resolve().parent / "database.db"


def conectar_banco():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar_banco()

    try:
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
        conexao.commit()
    finally:
        conexao.close()


def definir_prioridade(descricao):
    # Padroniza maiúsculas/minúsculas e separa os acentos das letras.
    descricao_busca = unicodedata.normalize("NFD", descricao.casefold())

    # Remove as marcas de acentuação.
    descricao_busca = "".join(
        caractere
        for caractere in descricao_busca
        if unicodedata.category(caractere) != "Mn"
    )

    # Identifica apenas as palavras completas "urgente" ou "erro".
    if re.search(r"\b(urgente|erro)\b", descricao_busca):
        return "Alta"

    return "Normal"


criar_tabela()


@app.route("/")
def home():
    conexao = conectar_banco()

    try:
        tickets = conexao.execute("""
            SELECT *
            FROM tickets
            ORDER BY id DESC
        """).fetchall()

        total_tickets = conexao.execute("""
            SELECT COUNT(*)
            FROM tickets
        """).fetchone()[0]

        tickets_novos = conexao.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE status = 'Novo'
        """).fetchone()[0]

        prioridade_alta = conexao.execute("""
            SELECT COUNT(*)
            FROM tickets
            WHERE prioridade = 'Alta'
        """).fetchone()[0]

        setores_atendidos = conexao.execute("""
            SELECT COUNT(DISTINCT setor)
            FROM tickets
        """).fetchone()[0]

    finally:
        conexao.close()

    return render_template(
        "cadastrar.html",
        tickets=tickets,
        total_tickets=total_tickets,
        tickets_novos=tickets_novos,
        prioridade_alta=prioridade_alta,
        setores_atendidos=setores_atendidos
    )


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    setor = request.form.get("setor", "").strip()
    data_solicitacao = request.form.get(
        "data_solicitacao", ""
    ).strip()

    # Valida os campos obrigatórios.
    if not all([
        titulo,
        descricao,
        setor,
        data_solicitacao
    ]):
        flash(
            "Preencha todos os campos obrigatórios.",
            "error"
        )
        return redirect(url_for("home"))

    # Define automaticamente a prioridade com base na descrição.
    prioridade = definir_prioridade(descricao)
    status = "Novo"

    conexao = conectar_banco()

    try:
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
            titulo,
            descricao,
            data_solicitacao,
            setor,
            status,
            prioridade
        ))

        conexao.commit()

    except sqlite3.Error:
        conexao.rollback()
        app.logger.exception("Erro ao cadastrar ticket.")

        flash(
            "Não foi possível cadastrar o ticket. Tente novamente.",
            "error"
        )
        return redirect(url_for("home"))

    finally:
        conexao.close()

    flash(
        f"Demanda '{titulo}' cadastrada com sucesso!",
        "success"
    )

    return redirect(url_for("home"))


@app.route("/exportar-csv")
def exportar_csv():
    conexao = conectar_banco()

    try:
        # Total geral de demandas.
        total = conexao.execute("""
            SELECT COUNT(*)
            FROM tickets
        """).fetchone()[0]

        # Quantidade de demandas por status.
        por_status = conexao.execute("""
            SELECT status, COUNT(*) AS quantidade
            FROM tickets
            GROUP BY status
            ORDER BY status
        """).fetchall()

        # Quantidade de demandas por setor.
        por_setor = conexao.execute("""
            SELECT setor, COUNT(*) AS quantidade
            FROM tickets
            GROUP BY setor
            ORDER BY setor
        """).fetchall()

        # Quantidade de demandas por prioridade.
        por_prioridade = conexao.execute("""
            SELECT prioridade, COUNT(*) AS quantidade
            FROM tickets
            GROUP BY prioridade
            ORDER BY prioridade
        """).fetchall()

    finally:
        conexao.close()

    arquivo = io.StringIO(newline="")

    escritor = csv.writer(
        arquivo,
        delimiter=";",
        lineterminator="\n"
    )

    # Estrutura tabular para facilitar a análise no Power BI.
    escritor.writerow([
        "tipo_indicador",
        "categoria",
        "quantidade"
    ])

    escritor.writerow([
        "Total de demandas",
        "Total",
        total
    ])

    for item in por_status:
        escritor.writerow([
            "Demandas por status",
            item["status"],
            item["quantidade"]
        ])

    for item in por_setor:
        escritor.writerow([
            "Demandas por setor",
            item["setor"],
            item["quantidade"]
        ])

    for item in por_prioridade:
        escritor.writerow([
            "Demandas por prioridade",
            item["prioridade"],
            item["quantidade"]
        ])

    # BOM UTF-8 para melhorar a compatibilidade com o Excel.
    conteudo = "\ufeff" + arquivo.getvalue()

    resposta = Response(
        conteudo,
        content_type="text/csv; charset=utf-8"
    )

    resposta.headers["Content-Disposition"] = (
        'attachment; filename="relatorio_demandas.csv"'
    )

    return resposta


if __name__ == "__main__":
    app.run( host="0.0.0.0", port=5000, debug=False )
