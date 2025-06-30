# repositories/bigquery_repo.py
from google.cloud import bigquery


def obter_ultima_data_por_ticker(projeto_id, dataset_id, tabela_id, ticker):
    client = bigquery.Client(project=projeto_id)
    tabela_ref = f"{projeto_id}.{dataset_id}.{tabela_id}"
    query = f"""
        SELECT MAX(data) AS ultima_data
        FROM `{tabela_ref}`
        WHERE Ticker = '{ticker}'
    """
    try:
        resultado = client.query(query).result()
        for row in resultado:
            return row.ultima_data
    except Exception as e:
        print(f"Erro ao consultar ultima data de {ticker}: {e}")
    return None


def criar_tabela_particionada(client, projeto_id, dataset_id, tabela_id):
    tabela_ref = f"{projeto_id}.{dataset_id}.{tabela_id}"
    try:
        client.get_table(tabela_ref)
        print(f"Tabela {tabela_ref} já existe.")
    except Exception:
        print(f"Criando tabela {tabela_ref} particionada por data...")
        schema = [
            bigquery.SchemaField("data", "DATE"),
            bigquery.SchemaField("Ticker", "STRING"),
            bigquery.SchemaField("Close", "FLOAT64"),
            bigquery.SchemaField("Volatilidade", "FLOAT64"),
        ]
        table = bigquery.Table(tabela_ref, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY, field="data"
        )
        client.create_table(table)
        print(f"Tabela {tabela_ref} criada com particionamento por data.")


def salvar_no_bigquery(df, projeto_id, dataset_id, tabela_id):
    if df.empty:
        print("Nenhum dado novo para salvar.")
        return

    client = bigquery.Client(project=projeto_id)
    criar_tabela_particionada(client, projeto_id, dataset_id, tabela_id)

    tabela_ref = f"{projeto_id}.{dataset_id}.{tabela_id}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        autodetect=False,
    )
    job = client.load_table_from_dataframe(df, tabela_ref, job_config=job_config)
    job.result()
    print(f"Dados salvos na tabela: {tabela_ref}")
