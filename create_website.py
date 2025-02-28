import os
import re
import locale
from datetime import datetime

# Définir la locale en français pour le formatage des dates
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Répertoire contenant les images
images_dir = 'images'
# Fichier HTML de sortie
output_file = 'index.html'

def extract_date(filename):
    # Recherche d'une date au format "DD_MM_YYYY" dans le nom du fichier
    match = re.search(r'(\d{2}_\d{2}_\d{4})', filename)
    if match:
        return datetime.strptime(match.group(1), '%d_%m_%Y')
    return datetime.min

# Récupérer la liste des fichiers images
image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

# Trier les images par date (extrait du nom du fichier) de la plus récente à la plus ancienne
sorted_images = sorted(image_files, key=extract_date, reverse=True)

# Créer le contenu HTML avec affichage en grille et vue détaillée
html_content = '<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
html_content += '  <meta charset="UTF-8">\n'
html_content += '  <title>BP Gallery</title>\n'
html_content += '  <link rel="stylesheet" type="text/css" href="style.css">\n'
html_content += '</head>\n<body>\n'

# Section grille
html_content += '  <div class="container" id="grid-container">\n'
html_content += '    <h1>Balance Patch Note Gallery</h1>\n'
# Barre de recherche
# html_content += '    <div class="search-container">\n'
# html_content += '      <input type="text" id="monster-search" placeholder="Rechercher un monstre">\n'
# html_content += '      <button id="search-button">Rechercher</button>\n'
# html_content += '      <button id="reset-button">Réinitialiser</button>\n'
# html_content += '    </div>\n'

# Afficher les images dans une grille
html_content += '    <div class="grid">\n'
for image in sorted_images:
    # Extraire la date depuis le nom du fichier (ex : "skill_balance_29_05_2024.png")
    match = re.search(r'(\d{2}_\d{2}_\d{4})', image)
    if match:
        date_str = match.group(1)
        date_obj = datetime.strptime(date_str, '%d_%m_%Y')
        formatted_date = date_obj.strftime('%d %B %Y')
    else:
        formatted_date = "Date inconnue"
    html_content += f'      <div class="card" data-image="{images_dir}/{image}" data-date="{formatted_date}">\n'
    html_content += f'        <p class="date">{formatted_date}</p>\n'
    html_content += '        <p class="title">Balance Patch</p>\n'
    html_content += '      </div>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'

# Section vue détaillée (cachée par défaut)
html_content += '  <div class="detail-view" id="detail-view" style="display: none;">\n'
html_content += '    <button id="back-button">Retour</button>\n'
html_content += '    <div id="detail-caption"></div>\n'
html_content += '    <img id="detail-img" src="" alt="Balance Patch en grand">\n'
html_content += '  </div>\n'

html_content += '  <script src="script.js"></script>\n'
html_content += '</body>\n</html>\n'

# Écrire le contenu HTML dans le fichier de sortie
with open(output_file, 'w') as f:
    f.write(html_content)

print(f"Index file created: {output_file}")
