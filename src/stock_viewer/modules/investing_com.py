#!/usr/bin/python3

import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta


def is_etf_investing(ticker: str, timeout=10) -> bool:
    ticker = ticker.lower()
    if ticker.endswith(".sa"):
        ticker = ticker[:-3]

    url = f"https://br.investing.com/etfs/{ticker}-historical-data"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        if r.status_code != 200:
            return False

        # Se conseguir ler tabela, é ETF
        tables = pd.read_html(StringIO(r.text))
        return len(tables) > 0

    except Exception:
        return False

def get_etf_history_1mo(ticker: str) -> list[float]:
    """
    Fetch daily historical Close prices for a B3 ETF from Investing.com
    for the last 1 month.

    Returns empty list if ticker does not exist or is not an ETF.
    """
    # Normalize ticker
    ticker = ticker.lower()
    if ticker.endswith(".sa"):
        ticker = ticker[:-3]

    url = f"https://br.investing.com/etfs/{ticker}-historical-data"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        tables = pd.read_html(StringIO(response.text))
        if not tables:
            return []  # Nenhuma tabela encontrada → ticker inválido

        df = tables[0]

        # Padronizar colunas (verifica se tem as colunas esperadas)
        if len(df.columns) < 7:
            return []  # Estrutura inesperada → não é ETF

        df.columns = ["Date", "Close", "Open", "High", "Low", "Volume", "Change"]
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

        # Converter valores numéricos
        df["Close"] = df["Close"].astype(str).astype(float)/100.0

        # Filtrar últimos 31 dias
        cutoff_date = datetime.now() - timedelta(days=31)
        df = df[df["Date"] >= cutoff_date]

        return df.sort_values("Date")["Close"].tolist()

    except (requests.RequestException, ValueError, IndexError):
        # Qualquer problema de conexão ou leitura de tabela retorna lista vazia
        return []

if __name__ == "__main__":
    print(get_etf_history_1mo("BSOX39.SA"))  # ETF válido
    print(get_etf_history_1mo("PETR4.SA"))   # Não ETF → []
    print(get_etf_history_1mo("ABCD123"))    # Ticker inexistente → []
    
    print(is_etf_investing("BSOX39.SA"))
    print(is_etf_investing("PETR4.SA"))
    print(is_etf_investing("ABCD123"))

