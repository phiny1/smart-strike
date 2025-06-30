# app/repositories/monitor_execucao.py

from datetime import date

from app.config import carregar_config
from google.cloud import bigquery

CONFIG = carregar_config()

NOME_TABELA_MONITOR = (
    f"{CONFIG['BIGQUERY_PROJECT_ID']}.{CONFIG['BIGQUERY_DATASET']}.monitor_execucao"
)


def obter_ultima_data_disponivel(ticker: str) -> date | None:
    client = bigquery.Client()
    query = f"""
        SELECT MAX(data) AS ultima_data
        FROM `{NOME_TABELA_MONITOR}`
        WHERE ticker = @ticker
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("ticker", "STRING", ticker),
        ]
    )
    result = client.query(query, job_config=job_config).result()

    row = next(result, None)
    return row["ultima_data"] if row and row["ultima_data"] else None


def atualizar_ultima_data(ticker: str, data: date):
    client = bigquery.Client()
    table = client.get_table(NOME_TABELA_MONITOR)

    linhas = [{"ticker": ticker, "data": data}]
    client.insert_rows_json(table, linhas)
