# domain/modelo_acao.py
from dataclasses import dataclass
from datetime import date


@dataclass
class RegistroAcao:
    data: date
    ticker: str
    close: float
    volatilidade: float
