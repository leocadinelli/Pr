
from pathlib import Path
import requests
import pandas as pd
import pyarrow

API_URL = (
    "https://servicodados.ibge.gov.br/"
    "api/v1/localidades/municipios"
)

### Definindo as camadas:
OUTPUT_BRONZE = Path("C:\\Projeto 3 FT\\SRC\\Data\\Bronze") 

   
# ################### Função para extrair os municpios
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

# ###############  executando a função de municípios
if __name__ == "__main__":

    dados_api = extrair_municipios()
    
    # 2. Transforma em um DataFrame do Pandas para você poder manipular
    df_municipios = pd.DataFrame(dados_api)

   
    caminho_arquivo = OUTPUT_BRONZE / "municipios_bruto.parquet"
    df_municipios.to_parquet(caminho_arquivo, index=False)

    
    # Teste: exibe as 5 primeiras linhas no terminal para checar se deu certo
    print("\nVisualizando os primeiros municípios carregados:")
    print(df_municipios.head())