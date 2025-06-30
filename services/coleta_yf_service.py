import pandas as pd
import yfinance as yf
from app.domain.modelo_acao import Acao


def buscar_dados_historicos(
    ativo: str, data_inicio: str, data_fim: str
) -> pd.DataFrame:
    ticker = yf.Ticker(ativo)
    df = ticker.history(start=data_inicio, end=data_fim)

    if df.empty:
        return pd.DataFrame()

    df = df.reset_index()
    df["ticker"] = ativo
    df["data"] = df["Date"].dt.date
    df = df[["ticker", "data", "Close"]]
    df.rename(columns={"Close": "preco_fechamento"}, inplace=True)

    return df


def calcular_volatilidade(df: pd.DataFrame, janela: int = 21) -> pd.DataFrame:
    if df.empty:
        return df

    df = df.sort_values("data")
    df["retorno_log"] = (
        df["preco_fechamento"] / df["preco_fechamento"].shift(1)
    ).apply(lambda x: 0 if x <= 0 else pd.np.log(x))
    df["volatilidade"] = df["retorno_log"].rolling(window=janela).std() * (252**0.5)
    df = df.dropna(subset=["volatilidade"])
    df = df[["ticker", "data", "preco_fechamento", "volatilidade"]]

    return df


def buscar_dados_e_calcular_volatilidade(
    ativo: str, data_inicio: str, data_fim: str
) -> list[Acao]:
    df = buscar_dados_historicos(ativo, data_inicio, data_fim)
    df = calcular_volatilidade(df)

    acoes = [
        Acao(
            ticker=row["ticker"],
            data=row["data"],
            preco_fechamento=row["preco_fechamento"],
            volatilidade=row["volatilidade"],
        )
        for _, row in df.iterrows()
    ]

    return acoes
