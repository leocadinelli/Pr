
from pathlib import Path
import pandas as pd
import pyarrow


### Definindo as camadas:
BASE = Path(__file__).resolve().parent.parent.parent
ARQUIVO_BRONZE = BASE / "DATA" / "Bronze"
ARQUIVO_PRATA = BASE / "DATA" / "Prata"
ARQUIVO_PRATA.mkdir(parents=True, exist_ok=True)

   
# ################### Função para extrair os municpios
def parquet_estado():

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
if __name__ == "__main__":

    df_estado = parquet_estado()
    df_estado = pd.json_normalize(df_estado.to_dict(orient="records"))
    df_estado = df_estado.rename(columns={ "microrregiao.mesorregiao.UF.id":"id_uf" , "microrregiao.mesorregiao.UF.sigla":"nm_uf"})
    ### Tratamento de dados:
    df_estado["id_uf"] = pd.to_numeric(df_estado["id_uf"], errors="coerce").astype("Int64")
    df_estado = df_estado[["id_uf", "nm_uf" ]]
    df_estado = df_estado.drop_duplicates(subset=["id_uf", "nm_uf"])
    df_estado = df_estado.dropna() 

# ##### Salvando o arquivo em parquet na camada prata
    df_estado.to_parquet(ARQUIVO_PRATA / "estados.parquet", index=False)
    df_data_quality = data_quality(df_estado)
    df_data_quality.to_parquet(ARQUIVO_PRATA / "data_quality_estados.parquet", index=False)
    