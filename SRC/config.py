import sys
from pathlib import Path

def obter_raiz_projeto() -> Path:
    if getattr(sys, "frozen", False):
        # Quando rodar como executável (.exe), salva ao lado do .exe
        return Path(sys.executable).resolve().parent
    # Quando rodar como script Python normal (.py), sobe até a raiz do projeto
    return Path(__file__).resolve().parent.parent

BASE_DIR = obter_raiz_projeto()
BRONZE_DIR = BASE_DIR / "DATA" / "Bronze"
PRATA_DIR = BASE_DIR / "DATA" / "Prata"
OURO_DIR = BASE_DIR / "DATA" / "Ouro"
