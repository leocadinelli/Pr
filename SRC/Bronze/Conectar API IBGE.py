
from pathlib import Path
import requests
import pandas as pd
import pyarrow

API_URL = (
    "https://servicodados.ibge.gov.br/"
    "api/v1/localidades/municipios"
)

### Definindo as camadas:
OUTPUT_BRONZE = Path("C:\\Projeto 3 FT\\DATA\\Bronze") 

   
# ################### Função para extrair os municpios
def extrair_municipios():

    print("Consultando à API do IBGE...")

    response = requests.get(
        API_URL,
        timeout=60
    )

    response.raise_for_status() # Alerta para caso de erro na requisição

    dados = response.json()

    print(f"Registros recebidos: {len(dados)}")

    return dados

# ###############  executando a função de salvar os dados em parquet na camada bronze 
if __name__ == "__main__":

    dados_api = extrair_municipios()
    
    # Tabela Municípios
    df_municipios = pd.DataFrame(dados_api)
    caminho_arquivo_municipios = OUTPUT_BRONZE / "municipios_bruto_IBGE.parquet"
    df_municipios.to_parquet(caminho_arquivo_municipios, index=False)


