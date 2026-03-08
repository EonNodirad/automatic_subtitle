#!/bin/bash

echo " Démarrage de l'outil de sous-titrage automatique..."

# --- NOUVEAU : Vérification de FFmpeg ---
if ! command -v ffmpeg &> /dev/null; then
    echo "ERREUR : FFmpeg n'est pas installé ou n'est pas dans le PATH."
    echo "FFmpeg est indispensable pour lire l'audio des vidéos."
    echo ""
    echo "Pour l'installer :"
    echo "   - Arch Linux : sudo pacman -S ffmpeg"
    echo "   - Ubuntu/Debian : sudo apt install ffmpeg"
    echo "   - macOS (via Homebrew) : brew install ffmpeg"
    echo     "et si marche toujours pas demande à chatGPT"
    echo ""
    exit 1
fi
# ----------------------------------------

# 1. Création de l'environnement virtuel s'il n'existe pas
if [ ! -d ".venv" ]; then
    echo " Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# 2. Activation de l'environnement
source .venv/bin/activate

# 3. Installation des dépendances (Racine + dossier stt)
echo "Vérification et installation des dépendances..."
pip install -r requirements.txt
pip install -r stt/requirements.txt

# 4. Lancement du serveur en arrière-plan
echo "Lancement du serveur STT en arrière-plan..."
cd stt
python stt_service.py &
SERVER_PID=$! # On sauvegarde l'ID du processus pour pouvoir le tuer plus tard
cd ..

# Petite pause pour laisser le temps à Uvicorn/FastAPI de démarrer
sleep 3

# 5. Lancement de l'interface client
echo "Lancement de l