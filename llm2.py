#!/usr/bin/env python3
"""
Script pour envoyer plusieurs images à une API de résolution de CAPTCHA
et déterminer laquelle contient l'emoji ☺, puis obtenir le résultat du calcul.
"""

import requests
import time
import base64
from urllib.parse import urlencode

# Configuration
API_KEY = "4od3CGlzIDzSgORGYyrPirHP7JkmNXQR"
API_IN_URL = "https://157.180.15.203/in.php"
API_RES_URL = "https://157.180.15.203/res.php"

# Liste des chemins d'images (à modifier selon vos fichiers)
image_paths = [
    "20260214_082832.jpg",
    "20260218_074055.jpg",
    "24dd109f-0b52-4d5a-b49b-6ce2a7aaf17f.jpeg"
]

# Instruction pour l'IA (adaptée à l'emoji ☺ et au format de réponse attendu)
instruction = (
    "Does this image contain the emoji : ☺? "
    "If yes, extract the calculation result (a number) and respond with only that number (e.g., '42'). "
    "If no, respond with exactly 'no'."
)

def process_image(image_path):
    """Envoie une image à l'API et retourne la réponse finale."""
    print(f"\n--- Traitement de {image_path} ---")
    # Lire et encoder l'image en base64
    with open(image_path, "rb") as f:
        image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # Paramètres de la requête
    data = {
        "key": API_KEY,
        "method": "aireqdata",
        "body": image_base64,
        "textinstructions": instruction,
    }

    print(f"→ Envoi de l'image à {API_IN_URL}...")
    try:
        response = requests.post(API_IN_URL, data=data, timeout=30)
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")
        return None

    print(f"Statut: {response.status_code}")
    print(f"Réponse brute: {response.text}")

    result = response.text.strip()
    if "|" not in result:
        print("Erreur : pas d'ID de tâche.")
        return None

    status, task_id = result.split("|", 1)
    print(f"ID de la tâche: {task_id}")

    # Polling jusqu'à obtention du résultat
    max_wait = 300  # 5 minutes
    poll_interval = 5
    start_time = time.time()

    while (time.time() - start_time) < max_wait:
        time.sleep(poll_interval)

        poll_params = {
            "key": API_KEY,
            "id": task_id,
            "action": "get"
        }
        poll_url = f"{API_RES_URL}?{urlencode(poll_params)}"
        try:
            poll_response = requests.get(poll_url, timeout=30)
        except Exception as e:
            print(f"Erreur de polling : {e}")
            continue

        poll_result = poll_response.text.strip()
        elapsed = time.time() - start_time
        print(f"  [{elapsed:.1f}s] Statut: {poll_result[:50]}...")

        if "NOT_READY" not in poll_result and "PROCESSING" not in poll_result:
            print(f"✓ Réponse finale : {poll_result}")
            return poll_result
    else:
        print("⚠ Délai d'attente dépassé.")
        return None

def main():
    results = {}
    for path in image_paths:
        answer = process_image(path)
        results[path] = answer
        # Petit délai entre les requêtes pour éviter de surcharger le serveur
        time.sleep(2)

    print("\n--- Résultats obtenus ---")
    for path, ans in results.items():
        print(f"{path}: {ans}")

    # Identifier l'image contenant l'emoji (réponse différente de "no")
    found = None
    for path, ans in results.items():
        if ans and ans.lower() != "no":
            found = ans
            print(f"\nL'image contenant l'emoji ☺ a donné le résultat : {found}")
            break
    if not found:
        print("Aucune image n'a été identifiée avec l'emoji ☺.")

if __name__ == "__main__":
    main()