import os
import re
from datetime import datetime

# Répertoire contenant les images
images_dir = 'images'
# Fichier HTML de sortie
output_file = 'index.html'

# Récupérer la liste des fichiers images
image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

# Trier les images par date (extraite du nom de fichier) de la plus récente à la plus ancienne
sorted_images = sorted(
    image_files,
    key=lambda x: datetime.strptime(os.path.splitext(x)[0].split('_')[-1], '%Y-%m-%d'),
    reverse=True
)

# Créer le contenu HTML avec affichage en grille et vue détaillée
html_content = '<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
html_content += '  <meta charset="UTF-8">\n'
html_content += '  <title>BP Gallery</title>\n'
html_content += '  <link rel="stylesheet" type="text/css" href="style.css">\n'
html_content += '</head>\n<body>\n'

# Section grille
html_content += '  <div class="container" id="grid-container">\n'
html_content += '    <h1>Balance Patch Note Gallery</h1>\n'
html_content += '    <div class="grid">\n'
for image in sorted_images:
    # Extraire la date du nom du fichier, ex : "skill_balance_2025-01-24.png"
    match = re.search(r'(\d{4}-\d{2}-\d{2})', image)
    date_str = match.group(1) if match else "Date inconnue"
    html_content += f'      <div class="card" data-image="{images_dir}/{image}" data-date="{date_str}">\n'
    html_content += f'        <p class="date">{date_str}</p>\n'
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
