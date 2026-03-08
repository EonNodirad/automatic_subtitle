@echo off
title Client Automatic Subtitle
echo Lancement de l'interface graphique (Mode Docker)...

IF NOT EXIST ".venv" (
    echo Creation de l'environnement virtuel...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
echo Verification des dependances du client...
pip install -r requirements.txt

python soustitre.py
pause