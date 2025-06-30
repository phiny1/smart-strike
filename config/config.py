# config/config.py
import os

from dotenv import load_dotenv

load_dotenv()

PROJETO_ID = os.getenv("BQ_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET_ID")
TABELA_ID = os.getenv("BQ_TABELA_ID")

ATIVOS_FIXOS = ["PETR4.SA", "VALE3.SA", "ITUB4.SA"]
