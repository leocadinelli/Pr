@echo off
chcp 65001 > nul

set REPO_URL=https://github.com/leocadinelli/Pr
set PASTA_PROJETO=Pr

echo ==================================================
echo    EXECUTANDO PIPELINE - REPOSITORIO Pr
echo ==================================================

if not exist "%PASTA_PROJETO%" (
    echo [1/4] Clonando repositorio do GitHub...
    git clone "%REPO_URL%"
) else (
    echo [1/4] Atualizando repositorio existente...
    cd "%PASTA_PROJETO%"
    git pull origin main
    cd ..
)

if not exist "%PASTA_PROJETO%" (
    echo [ERRO] Nao foi possivel encontrar a pasta %PASTA_PROJETO%.
    pause
    exit /b 1
)

cd "%PASTA_PROJETO%"

if not exist "venv" (
    echo [2/4] Criando ambiente virtual...
    python -m venv venv
)

echo [3/4] Instalando dependencias...
call venv\Scripts\activate
python -m pip install --upgrade pip -q:
python -m pip install -r requirements.txt -q

echo [4/4] Rodando SRC\main.py...
python SRC\main.py

echo.
echo ==================================================
echo    PROCESSO FINALIZADO!
echo ==================================================
pause
