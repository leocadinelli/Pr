
from pathlib import Path
import pandas as pd
import pyarrow


### Definindo as camadas:
BASE = Path(__file__).resolve().parent.parent.parent

ARQUIVO_BRONZE = BASE / "DATA" / "Bronze"
ARQUIVO_PRATA = BASE / "DATA" / "Prata"
ARQUIVO_PRATA.mkdir(parents=True, exist_ok=True)

   
# ################### Função para extrair os municpios
def parquet_municipios():

    caminho_arquivo_municipios = ARQUIVO_BRONZE / "municipios_bruto_IBGE.parquet"
    dados = pd.read_parquet(caminho_arquivo_municipios)

    return dados

def data_quality(df):
    resumo = pd.DataFrame({
        "Tipo": df.dtypes.astype(str),
        "Nulos": df.isna().sum(),
        "% Nulos": (df.isna().mean() * 100).round(2),
        "Únicos": df.nunique()
    })
    return resumo

# ###############  executando a função de salvar os dados em parquet na camada bronze 
def run():

    df_municipio = parquet_municipios()
    df_municipio = pd.json_normalize(df_municipio.to_dict(orient="records"))
    print(df_municipio.head())
    df_municipio = df_municipio.rename(columns={"id": "id_municipio", "nome": "nome_municipio" , "microrregiao.mesorregiao.UF.id":"id_uf"})
    df_municipio = df_municipio[["id_municipio", "nome_municipio" , "id_uf"]]
    #Tratamento de dados:
    df_municipio["id_municipio"] = df_municipio["id_municipio"].astype(str).str[1:]
    df_municipio["id_municipio"] = pd.to_numeric(df_municipio["id_municipio"], errors="coerce").astype("Int64")
    df_municipio["id_uf"] = pd.to_numeric(df_municipio["id_uf"], errors="coerce").astype("Int64") 
   
# ##### Salvando o arquivo em parquet na camada prata
    df_municipio.to_parquet(ARQUIVO_PRATA / "municipios.parquet", index=False)
    df_data_quality = data_quality(df_municipio)
    df_data_quality.to_parquet(ARQUIVO_PRATA / "data_quality_municipios.parquet", index=False)
    df_data_quality.to_csv(BASE /"Outputs" / "data_quality_municipios.csv", index=False)

if __name__ == "__main__":
    run() 


    

