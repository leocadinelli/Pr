import time
from Bronze import Extracao_IBGE , Extrair_SUS
from Prata import Tabela_Estado,Tabela_Municipio,Tabela_Estabelecimentos_SUS
from Ouro import Analise_Final


def rodar_pipeline():
    inicio = time.time()
    print("=== INICIANDO PIPELINE ===")

    # 1. Camada Bronze
    print("1/6 - Baixando IBGE...")
    Extracao_IBGE.run()

    print("2/6 - Baixando DATASUS...")
    Extrair_SUS.run()

    # 2. Camada Prata
    print("3/6 - Tratando Estabelecimentos...")
    Tabela_Estabelecimentos_SUS.run()

    print("4/6 - Tratando Estados...")
    Tabela_Estado.run()

    print("5/6 - Tratando Municípios...")
    Tabela_Municipio.run()

    # 3. Camada Ouro
    print("6/6 - Gerando Camada Ouro...")
    Analise_Final.run()

    print(f"=== CONCLUÍDO EM {time.time() - inicio:.1f}s ===")
    input("Pressione ENTER para sair...")


if __name__ == "__main__":
    rodar_pipeline()
