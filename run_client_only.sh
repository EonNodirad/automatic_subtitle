#!/bin/bash
echo " Lancement de l'interface graphique (Mode Docker)..."

if [ ! -d ".venv" ]; then
    echo " Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

source .venv/bin/activate
echo "Vérification des dépendances du client..."
pip install requirements.txt

python soustitre.py