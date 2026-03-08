# Automatic Subtitle (STT Whisper)

Ce projet permet de générer automatiquement des sous-titres précis à partir de fichiers audio ou vidéo en utilisant le modèle d'IA **Faster-Whisper**. 

Il est composé de deux parties :
1. **Un serveur (API REST)** : Fait le travail lourd de transcription et gère le découpage dynamique.
2. **Une interface graphique (Client)** : Permet de choisir le fichier, de régler le nombre de caractères par ligne, et de sauvegarder un `.srt`.


---

##  Prérequis

Pour utiliser ce projet en local, vous avez besoin de :
* **Python 3.10** ou supérieur.
* **FFmpeg** (Indispensable pour que l'IA puisse lire l'audio).
  * *Windows* : `winget install ffmpeg`
  * *Arch Linux* : `sudo pacman -S ffmpeg`
  * *Ubuntu/Debian* : `sudo apt install ffmpeg`
  * *macOS* : `brew install ffmpeg`
* **Docker** (Optionnel, mais recommandé pour isoler le serveur).

---

## Comment lancer le projet ? (3 Méthodes)

Choisissez la méthode qui correspond le mieux à vos besoins :

### Méthode 1 : Tout automatique en local (Le plus simple)
Pas besoin de configurer quoi que ce soit, le script gère la création de l'environnement virtuel, installe les dépendances, lance le serveur en tâche de fond, puis ouvre l'interface.

* **Sous Windows** : Double-cliquez sur `run.bat`
* **Sous Linux/macOS** : Lancez `./run.sh` dans votre terminal.

### Méthode 2 : Serveur via Docker + Interface locale (Recommandé)
Cette méthode est la plus propre. Elle enferme le lourd modèle Whisper et ses dépendances dans un conteneur Docker, laissant votre machine propre.

1. **Lancer le serveur STT :**
   Ouvrez un terminal à la racine du projet et tapez :
   ```
   bash
   docker compose up --build -d 
   ```
   
   
2. **Lancer l'interface client :** Une fois le serveur démarré, utilisez les scripts dédiés :
    
    - _Windows_ : Double-cliquez sur `run_client_only.bat`
        
    - _Linux/macOS_ : Lancez `./run_client_only.sh`
        

### Méthode 3 : 100% Manuel (Pour les développeurs)

Si vous voulez tout contrôler étape par étape.

1. **Créer et activer l'environnement virtuel :**
    
    Bash
    
    ```
    python -m venv .venv
    source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate.bat
    ```
    
2. **Installer toutes les dépendances :**
    
    Bash
    
    ```
    pip install -r requirements.txt
    pip install -r stt/requirements.txt
    ```
    
3. **Lancer le serveur :**
    
    Bash
    
    ```
    cd stt
    python stt_service.py
    ```
    
4. **Lancer l'interface (dans un nouveau terminal, avec le venv activé) :**
    
    Bash
    
    ```
    cd ..
    python soustitre.py
    ```
    

---

## Paramétrage du découpage

Dans l'interface graphique, vous pouvez définir le nombre maximum de caractères par ligne de sous-titre. L'algorithme se chargera de ne jamais couper un mot en son milieu, tout en gardant une synchronisation parfaite avec l'audio.

