#!/usr/bin/env python3
"""
Script pour envoyer une image à une API de résolution de CAPTCHA
et obtenir une réponse indiquant si l'image contient l'emoji ★.
"""

import requests
import time
import base64
from urllib.parse import urlencode

# Configuration
API_KEY = "4od3CGlzIDzSgORGYyrPirHP7JkmNXQR"
API_IN_URL = "https://157.180.15.203/in.php"
API_RES_URL = "https://157.180.15.203/res.php"
IMAGE_PATH = "24dd109f-0b52-4d5a-b49b-6ce2a7aaf17f.jpeg"  # ← À MODIFIER

# Lire et encoder l'image en base64
with open(IMAGE_PATH, "rb") as f:
    image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

# Instruction pour l'IA (en anglais pour plus de fiabilité)
instruction = (
    "Does this image contain an image like this '★'? "
    "If yes, answer exactly: 'oui, résultat du calcul' (replace 'résultat du calcul' with the actual calculation result). "
    "If no, answer exactly: 'non', résultat du calcul' (replace 'résultat du calcul' with the actual calculation result). "
)

# Paramètres de la requête
data = {
    "key": API_KEY,
    "method": "aireqdata",
    "body": image_base64,
    "textinstructions": instruction,
}

print(f"→ Envoi de l'image à {API_IN_URL}...")
response = requests.post(API_IN_URL, data=data, timeout=30)
print(f"Statut: {response.status_code}")
print(f"Réponse brute: {response.text}")

# Traitement de la réponse pour obtenir l'ID de tâche
result = response.text.strip()
if "|" in result:
    status, task_id = result.split("|", 1)
    print(f"\nID de la tâche: {task_id}")
    print("Attente du résultat...")

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
        poll_response = requests.get(poll_url, timeout=30)
        poll_result = poll_response.text.strip()

        elapsed = time.time() - start_time
        print(f"  [{elapsed:.1f}s] Statut: {poll_result[:50]}...")

        if "NOT_READY" not in poll_result and "PROCESSING" not in poll_result:
            print(f"\n✓ Réponse finale : {poll_result}")
            # Ici, vous pouvez exploiter poll_result pour la suite de votre script
            break
    else:
        print("\n⚠ Délai d'attente dépassé.")
else:
    print("Erreur : la réponse ne contient pas d'ID de tâche.")