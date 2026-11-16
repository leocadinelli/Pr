import pandas as pd
import requests
import io
import json
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent.parent
BRONZE_DIR = BASE / "DATA" / "Bronze"



url = "https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/CNES/cnes_estabelecimentos_json.zip"

response = requests.get(url)
response.raise_for_status() 

# Abre o ZIP direto da memória
with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    # Pega o nome do arquivo .json 
    nome_arquivo = z.namelist()[0]
    
    with z.open(nome_arquivo) as f:
        # Carrega os dados JSON
        dados_sus = json.load(f)
        dados_sus = pd.json_normalize(dados_sus)  # Normaliza os dados para um DataFrame do pandas


    arquivo_sus = BRONZE_DIR / "dados_sus_bruto.parquet"
    dados_sus.to_parquet(arquivo_sus, index=False)
