# pipelines/execucao_diaria.py
from repositories.bigquery_repo import salvar_no_bigquery
from services.coleta_yf_service import coletar_precos_volatilidade


def executar_pipeline_diaria(tickers, projeto, dataset, tabela):
    df_resultado = coletar_precos_volatilidade(
        tickers, projeto_id=projeto, dataset_id=dataset, tabela_id=tabela
    )
    salvar_no_bigquery(df_resultado, projeto, dataset, tabela)
