
from pathlib import Path
import pandas as pd
import pyarrow


### Definindo as camadas:
BASE = Path(__file__).resolve().parent.parent.parent
BRONZE_DIR = BASE / "DATA" / "Bronze"
PRATA_DIR = BASE / "DATA" / "Prata"
# Aqui são os códigos de natureza jurídica que representam a administração pública, conforme a tabela do SUS. 
CODIGOS_ADM_PUBLICA = [
    "1000", "1015", "1023", "1031", "1040", "1058", "1066", "1074",
    "1082", "1104", "1112", "1120", "1139", "1147", "1155", "1163",
    "1171", "1180", "1201", "1210", "1228", "1236", "1244", "1260",
    "1279", "1333"]
arquivo_sus = BRONZE_DIR / "dados_sus_bruto.parquet"


   

def lendo_dados_sus():

    dados = pd.read_parquet(arquivo_sus)

    return dados


def data_quality(df):
    resumo = pd.DataFrame({
        "Tipo": df.dtypes.astype(str),
        "Nulos": df.isna().sum(),
        "% Nulos": (df.isna().mean() * 100).round(2),
        "Únicos": df.nunique()
    })
    return resumo

if __name__ == "__main__":

    df_sus = lendo_dados_sus()
    df_estab = df_sus[["CO_IBGE", "NU_CNPJ", "CO_NATUREZA_JUR", "NO_FANTASIA" ]]
    df_estab = df_estab.rename(columns={"CO_IBGE": "id_municipio", "NU_CNPJ": "cnpj", "CO_NATUREZA_JUR": "cd_tipo", "NO_FANTASIA": "nome_fantasia"})
    df_estab["id_municipio"] = pd.to_numeric(df_estab["id_municipio"], errors="coerce").astype("Int64")
    df_estab = df_estab[df_estab["cd_tipo"].isin(CODIGOS_ADM_PUBLICA)]
  
    df_estab.to_parquet(PRATA_DIR / "estabelecimentos_sus.parquet", index=False)
    df_quality = data_quality(df_estab)
    print(df_quality)
    df_quality.to_parquet(PRATA_DIR / "data_quality_estabelecimentos_sus.parquet", index=False)
  
    
    
  
            

