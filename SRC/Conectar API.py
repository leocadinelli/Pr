
import requests
import pandas as pd

from pathlib import Path


API_URL = (
    "https://servicodados.ibge.gov.br/"
    "api/v1/localidades/municipios"
)

OUTPUT_DIR = Path("data/gold")

def extrair_municipios():

    print("Iniciando consulta à API do IBGE...")

    response = requests.get(
        API_URL,
        timeout=60
    )

    response.raise_for_status()

    dados = response.json()

    print(f"Registros recebidos: {len(dados)}")

    return dados
