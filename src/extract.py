"""
Módulo de Extração (Extract)
"Responsável por se comunicar com a XIVAPI v2 e baixar dados butos de itens via requisições HTTP."
"""

from typing import Any, Dict, List
import requests

XIVAPI_BASE_URL = "https://v2.xivapi.com/api/sheet/Item"

def fetch_ffxiv_items(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Busca uma lista de itens do Final Fantasy XIV via XIVAPO v2.

    Args:
       limit (int): Quantidade de itens a serem buscados por requisição (máximo e padrão sugerido).

    Returns:
       List[dict[str, Any]]: Lista contendo os itens brutos no formato de dicionário Python.
    """

    # 1. Parâmetros da URL (Query Parameters
    # Equivalente a digitar na barra do navegador: ?limit=50
    params = {
        "limit": limit,
    }

    headers = {
        "User-Agent": "FFXIV-ETL-Pipeline/1.0",
        "Accept": "application/json",
    }

    print(f"[EXTRACT] Requisitando {limit} itens de {XIVAPI_BASE_URL}...")

    try:
        response = requests.get(
            XIVAPI_BASE_URL,
            params=params,
            headers=headers,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        rows = data.get("rows", [])

        print(f"[EXTRACT] Sucesso! {len(rows)} itens brutos recebidos.")
        return rows
    except requests.exceptions.Timeout:
        print("[EXTRACT ERRO] A requisição excedeu o tempo limite (timeout de 10s).")
        raise
    except requests.exceptions.HTTPError as http_err:
        print(f"[EXTRACT ERRO] Erro retornado pela API: {http_err}")
        raise
    except requests.exceptions.RequestException as err:
        print(f"[EXTRACT ERRO] Falha geral de conexão de rede: {err}")
        raise

if __name__ == "__main__":

    itens_de_teste = fetch_ffxiv_items(limit=3)

    if itens_de_teste:
        print("\nExemplo de primeiro item recebido:")

        primeiro_item = itens_de_teste[0]
        print(f"ID: {primeiro_item.get('row_id')}")
        print(f"Campos disponíveis: {list(primeiro_item.get('fields', {}).keys())[:10]}...")