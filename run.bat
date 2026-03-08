@echo off
title Démarrage Automatic Subtitle
echo Demarrage de l'outil de sous-titrage automatique...

:: --- NOUVEAU : Vérification de FFmpeg ---
where ffmpeg >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo ERREUR : FFmpeg n'est pas installe ou n'est pas dans le PATH.
    echo FFmpeg est indispensable pour extraire l'audio des videos.
    echo.
    echo Pour l'installer facilement, ouvrez un terminal PowerShell et tapez :
    echo    winget install ffmpeg
    echo     et si marche toujours pas demande à chatGPT
    echo.
    pause
    exit /b 1
)
:: -----------------------------------------

:: 1. Création de l'environnement virtuel s'il n'existe pas
IF NOT EXIST ".venv" (
    echo Creation de l'environnement virtuel...
    python -m venv .venv
)

:: 2. Activation de l'environnement
call .venv\Scripts\activate.bat

:: 3. Installation des dépendances
echo Verification et installation des dependances...
pip install -r requirements.txt
pip install -r stt\requirements.txt

:: 4. Lancement du serveur dans une nouvelle fenêtre minimisée
echo Lancement du serveur STT...
start "Serveur STT (Ne pas fermer)" /MIN cmd /c "call .venv\Scripts\activate.bat && cd stt && python stt_service.py"

:: Petite pause (timeout)
timeout /t 3 /nobreak > NUL

:: 5. Lancement de l'interface client
echo Lancement de l'interface graphique...
python soustitre.py

:: 6. Nettoyage à la fermeture
echo  Fermeture de l'application...
:: Tue le processus Python qui fait tourner stt_service.py
taskkill /FI "WindowTitle eq Serveur STT*" /T /F > NUL 2>&1

echo Fini. A bientot !
pause