
from datetime import time
from pathlib import Path
import requests
import pandas as pd
import pyarrow
import time

API_URL = (
    "https://servicodados.ibge.gov.br/"
    "api/v1/localidades/municipios"
)

### Definindo as camadas:
OUTPUT_BRONZE = Path("C:\\Projeto 3 FT\\DATA\\Bronze") 

   
# ################### Função para extrair os municpios
def extrair_municipios(tentativas = 3 , espera = 2):

    for tentativa in range(1,tentativas + 1):
        try:
            print(f"Tentativa {tentativa} de {tentativas}...")
            time.sleep(1)
            response = requests.get(API_URL,timeout=60)
            response.raise_for_status
            dados = response.json()

            return dados
        except requests.exceptions.RequestException as e:
            print(f"Erro na tentativa {tentativa}: {e}")
            if tentativa < tentativas:
                print(f"Aguarde {espera} segundos antes da próxima tentativa...")
                time.sleep(espera)
            else:
                print("Total de tentativas atingido")
                raise
# ###############  executando a função de salvar os dados em parquet na camada bronze 
if __name__ == "__main__":

    dados_api = extrair_municipios()
    
    # Tabela Municípios
    df_municipios = pd.DataFrame(dados_api)
    caminho_arquivo_municipios = OUTPUT_BRONZE / "municipios_bruto_IBGE.parquet"
    df_municipios.to_parquet(caminho_arquivo_municipios, index=False)


