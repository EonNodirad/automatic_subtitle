import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import threading
import os

API_URL = "http://localhost:8001/subtitles"
current_srt = ""

def select_file():
    filepath = filedialog.askopenfilename(
        title="Choisir un fichier audio ou vidéo",
        filetypes=[("Fichiers médias", "*.mp3 *.wav *.mp4 *.mkv *.avi"), ("Tous les fichiers", "*.*")]
    )
    if filepath:
        process_file(filepath)

def process_file(filepath):
    btn_browse.config(state=tk.DISABLED, text="Génération en cours...")
    text_result.delete(1.0, tk.END)
    
    # On récupère la valeur choisie par l'utilisateur
    max_chars = int(spin_chars.get())
    
    filename = os.path.basename(filepath)
    text_result.insert(tk.END, f"Envoi de '{filename}' au serveur...\nDécoupage max: {max_chars} caractères.\nL'IA Whisper travaille, patiente un instant ⏳\n")
    
    threading.Thread(target=call_api, args=(filepath, max_chars), daemon=True).start()

def call_api(filepath, max_chars):
    try:
        with open(filepath, 'rb') as f:
            files = {'file': (filepath, f)}
            # ON ENVOIE LA LIMITE ICI !
            data = {'max_chars': max_chars} 
            response = requests.post(API_URL, files=files, data=data)
        
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                show_result(f"❌ Erreur du serveur: {data['error']}")
            else:
                srt_text = data.get("srt", "Pas de SRT reçu.")
                show_result(srt_text, is_success=True)
        else:
            show_result(f"❌ Erreur HTTP: {response.status_code}")
            
    except Exception as e:
        show_result(f"❌ Impossible de joindre le serveur.\nErreur: {e}")

def show_result(result_text, is_success=False):
    def update_ui():
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, result_text)
        btn_browse.config(state=tk.NORMAL, text="Choisir un fichier")
        
        if is_success:
            btn_save.config(state=tk.NORMAL)
            global current_srt
            current_srt = result_text
        else:
            btn_save.config(state=tk.DISABLED)
            
    window.after(0, update_ui)

def save_srt():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".srt",
        filetypes=[("Fichier Sous-titres", "*.srt")],
        title="Enregistrer le fichier SRT"
    )
    if filepath:
        with open(filepath, "w", encoding="utf-8-sig") as f:
            f.write(current_srt)
        messagebox.showinfo("Succès", "Fichier SRT sauvegardé avec succès !")

# --- INTERFACE GRAPHIQUE ---
window = tk.Tk()
window.title("Jean-Heude Subtitles Client - DaVinci Style")
window.geometry("750x550")

# Zone des options et boutons (en haut)
frame_top = tk.Frame(window)
frame_top.pack(pady=15)

# NOUVEAU : Le sélecteur de caractères
lbl_chars = tk.Label(frame_top, text="Caractères max / ligne :", font=("Arial", 11))
lbl_chars.pack(side=tk.LEFT, padx=(0, 5))

spin_chars = tk.Spinbox(frame_top, from_=5, to=100, width=5, font=("Arial", 11))
spin_chars.delete(0, tk.END)
spin_chars.insert(0, 15)  # Valeur par défaut (15, parfait pour les vidéos shorts/TikTok)
spin_chars.pack(side=tk.LEFT, padx=(0, 20))

btn_browse = tk.Button(frame_top, text="Choisir un fichier", command=select_file, font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
btn_browse.pack(side=tk.LEFT, padx=10)

btn_save = tk.Button(frame_top, text="💾 Sauvegarder en .srt", command=save_srt, state=tk.DISABLED, font=("Arial", 11), padx=10, pady=5)
btn_save.pack(side=tk.LEFT, padx=10)

# Zone de texte (au milieu)
text_result = tk.Text(window, wrap=tk.WORD, font=("Consolas", 11), bg="#f4f4f4")
text_result.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 20))
text_result.insert(tk.END, "Prêt ! \n1. Ajuste le nombre de caractères (ex: 13 pour du format vertical dynamique).\n2. Sélectionne ton fichier.")

window.mainloop()