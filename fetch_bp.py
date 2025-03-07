import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime

BASE_URL = "https://summonerswar.spokland.com"
IMAGES_DIR = "images"

def update_checker():
    # Créer le dossier images s'il n'existe pas
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    update_list_url = urljoin(BASE_URL, "/game/update")

    # Charger les URLs d'updates existantes depuis le fichier (si présent)
    urls_file = "update_urls.txt"
    existing_urls = set()
    if os.path.exists(urls_file):
        with open(urls_file, "r") as f:
            for line in f:
                existing_urls.add(line.strip())

    # Récupérer la page listant les updates
    response = requests.get(update_list_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extraire les URLs des updates à partir de la page (en utilisant l'attribut "onclick")
    update_divs = soup.find_all("div", class_="update")
    new_updates = []
    for div in update_divs:
        onclick = div.get("onclick")
        if onclick:
            match = re.search(r"window\.location\s*=\s*['\"](.*?)['\"]", onclick)
            if match:
                rel_url = match.group(1)
                full_url = urljoin(BASE_URL, rel_url)
                if full_url not in existing_urls:
                    new_updates.append(full_url)

    # Ajouter les nouvelles URLs d'update au fichier (si il y en a)
    if new_updates:
        with open(urls_file, "a") as f:
            for url in new_updates:
                f.write(url + "\n")
        print(f"Added {len(new_updates)} new update URL(s) to {urls_file}.")
    else:
        print("No new update URLs found.")

    # Traiter chaque nouvelle update
    for update_url in new_updates:
        print(f"Processing update page: {update_url}")
        upd_response = requests.get(update_url)
        upd_soup = BeautifulSoup(upd_response.text, "html.parser")

        # Vérifier si "Skill Balance" apparaît dans le texte
        if re.search(r"skill\s*_?\s*balance", upd_response.text, re.IGNORECASE):
            print("Skill Balance update found.")
            # Chercher une image dont le src contient "skill_balance"
            skill_img = upd_soup.find("img", src=re.compile(r"skill_?balance", re.IGNORECASE))
            if skill_img and skill_img.get("src"):
                img_src = skill_img.get("src")
                # Construire l'URL complète de l'image par rapport à l'URL de la page
                img_url = urljoin(update_url, img_src)

                # Extraire la date de mise à jour depuis la page (format YYYY-MM-DD)
                date_match = re.search(r"(\d{4}-\d{2}-\d{2})", upd_response.text)
                if date_match:
                    # Convertir la date au format DD MM YYYY
                    date_str = date_match.group(1)
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    update_date = date_obj.strftime('%d_%m_%Y')
                else:
                    update_date = "unknown_date"

                # Déterminer l'extension du fichier à partir de l'URL (par défaut .jpg)
                ext = os.path.splitext(img_url)[1] or ".jpg"
                # Définir le nom de fichier (par exemple, "skill_balance_24 01 2025.jpg")
                img_filename = f"skill_balance_{update_date}{ext}"
                file_path = os.path.join(IMAGES_DIR, img_filename)

                # Vérifier si le fichier existe déjà
                if os.path.exists(file_path):
                    print(f"The image {img_filename} already exists in '{IMAGES_DIR}', download skipped.")
                    continue

                # Télécharger et sauvegarder l'image
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(file_path, "wb") as img_file:
                        img_file.write(img_response.content)
                    print(f"Saved Skill Balance image as {file_path}.")
                else:
                    print(f"Failed to download image from {img_url}")
            else:
                print("No Skill Balance image found on the page.")
        else:
            print("No Skill Balance update detected on this page.")

if __name__ == "__main__":
    update_checker()
