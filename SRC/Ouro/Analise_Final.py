import pandas as pd
from pathlib import Path

# 1. Definição dos caminhos das pastas
BASE = Path(__file__).resolve().parent.parent.parent
PRATA_DIR = BASE / "DATA" / "Prata"   
OURO_DIR = BASE / "DATA" / "Ouro"
OURO_DIR.mkdir(parents=True, exist_ok=True)



df_estab = pd.read_parquet(PRATA_DIR / "estabelecimentos_sus.parquet")
df_mun = pd.read_parquet(PRATA_DIR / "municipios.parquet")
df_uf = pd.read_parquet(PRATA_DIR / "estados.parquet")

# 3. Cruzamento das tabelas 
def run():
    df_localidades = pd.merge(
        df_mun,
        df_uf,
        on="id_uf",
        how="left"
    )

    # Estabelecimentos com Municipios 
    df_ouro_detalhado = pd.merge(
        df_estab,
        df_localidades[["id_municipio", "nome_municipio", "id_uf", "nm_uf"]],
        on="id_municipio",
        how="inner"
    )

    # Data Quality Check: Verifica se existem estabelecimentos sem município correspondente
    total_linhas = len(df_ouro_detalhado)
    sem_municipio = df_ouro_detalhado["nome_municipio"].isna().sum()



    # Tabela Base analítica 
    df_ouro_detalhado.to_parquet(
        OURO_DIR / "ouro_estabelecimentos_completo.parquet",index=False)

    # Tabela Ouro 2: Resumo de estabelecimentos por Estado e Tipo
    df_ouro_por_uf = (
        df_ouro_detalhado
        .groupby(["nm_uf", "cd_tipo"], dropna=False)
        .agg(
            qtd_estabelecimentos=("nome_fantasia", "count"),
            qtd_cnpjs_unicos=("cnpj", "nunique")
        )
        .reset_index()
        .sort_values(by=["nm_uf", "qtd_estabelecimentos"], ascending=[True, False])
    )
    df_ouro_por_uf.to_parquet(OURO_DIR / "ouro_resumo_por_uf.parquet", index=False)
    df_ouro_por_uf.to_csv(BASE / "Outputs" / "ouro_resumo_por_uf.csv", index=False)

    # Tabela Ouro 3: Top Municípios por volume de unidades de saúde
    df_ouro_por_municipio = (
        df_ouro_detalhado
        .groupby(["nm_uf","nome_municipio"], dropna=False)
        .agg(
            total_unidades=("nome_fantasia", "count"),
            tipos_atendimento=("cd_tipo", "nunique")
        )
        .reset_index()
        .sort_values(by="total_unidades", ascending=False)
    )
    df_ouro_por_municipio.to_parquet(OURO_DIR / "ouro_ranking_municipios.parquet", index=False)
    df_ouro_por_municipio.to_csv(BASE / "Outputs" / "ouro_ranking_municipios.csv", index=False)

if __name__ == "__main__":
    run()   
    
