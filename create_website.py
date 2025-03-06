import os
import re
import locale
import json
from datetime import datetime

# Définir la locale en français pour le formatage des dates
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Répertoire contenant les images et fichier HTML de sortie
images_dir = 'images'
output_file = 'index.html'

def extract_date(filename):
    # Recherche d'une date au format "DD_MM_YYYY" dans le nom du fichier
    match = re.search(r'(\d{2}_\d{2}_\d{4})', filename)
    if match:
        return datetime.strptime(match.group(1), '%d_%m_%Y')
    return datetime.min

# Chargement du fichier JSON contenant les dates associées aux monstres
with open('monster_dates.json', 'r', encoding='utf-8') as f:
    monster_dates = json.load(f)

# Liste des monstres triée par ordre alphabétique
monsters_list = sorted(monster_dates.keys())

# Calcul du nombre de monstres par BP
bp_counts = {}
for monster, dates in monster_dates.items():
    for date_str in dates:
        bp_counts[date_str] = bp_counts.get(date_str, 0) + 1

# Classement des BP par nombre décroissant de monstres
bp_stats = sorted(bp_counts.items(), key=lambda x: x[1], reverse=True)

# Classement des monstres par nombre d'apparitions décroissant
monster_stats = sorted(monster_dates.items(), key=lambda x: len(x[1]), reverse=True)

# Récupérer la liste des fichiers images et trier par date (du plus récent au plus ancien)
image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
sorted_images = sorted(image_files, key=extract_date, reverse=True)

# Création du contenu HTML
html_content = '<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
html_content += '  <meta charset="UTF-8">\n'
html_content += '  <title>BP Gallery</title>\n'
html_content += '  <link rel="stylesheet" type="text/css" href="style.css">\n'
# Styles additionnels pour les onglets et la mise en page des colonnes dans Stats
html_content += '  <style>\n'
html_content += '    /* Styles pour les onglets */\n'
html_content += '    .tab-container { display: flex; justify-content: center; margin-top: 20px; }\n'
html_content += '    .tab-button { padding: 10px 20px; margin: 0 5px; font-size: 1rem; cursor: pointer; background-color: #3a3a3a; color: #e0e0e0; border: none; border-radius: 4px; transition: background-color 0.3s; }\n'
html_content += '    .tab-button.active { background-color: #007bff; color: #fff; }\n'
html_content += '    /* Styles pour les colonnes dans l\'onglet Stats */\n'
html_content += '    .stats-columns { display: flex; justify-content: space-between; flex-wrap: wrap; }\n'
html_content += '    .stats-column { flex: 1; margin: 10px; min-width: 300px; }\n'
html_content += '    .hidden { display: none; }\n'
html_content += '  </style>\n'
html_content += '</head>\n<body>\n'

# Navigation par onglets
html_content += '  <div class="tab-container">\n'
html_content += '    <button class="tab-button active" id="gallery-tab">BP List</button>\n'
html_content += '    <button class="tab-button" id="stats-tab">BP & Monsters Stats</button>\n'
html_content += '    <button class="tab-button" id="list-tab">Monsters List</button>\n'
html_content += '  </div>\n'

# Onglet Gallerie
html_content += '  <div id="gallery-container">\n'
html_content += '    <div class="container" id="grid-container">\n'
html_content += '      <h1>Balance Patch Note Gallery</h1>\n'
html_content += '      <div class="search-container">\n'
html_content += '        <input type="text" id="monster-search" placeholder="Type a monster name...">\n'
html_content += '        <button id="search-button">Search</button>\n'
html_content += '        <button id="reset-button">Reset</button>\n'
html_content += '      </div>\n'
html_content += '      <div id="search-results" class="search-results"></div>\n'
html_content += '      <div class="grid">\n'
for image in sorted_images:
    # Extraire la date depuis le nom du fichier (ex: "skill_balance_29_05_2024.png")
    match = re.search(r'(\d{2}_\d{2}_\d{4})', image)
    if match:
        date_str = match.group(1)
        date_obj = datetime.strptime(date_str, '%d_%m_%Y')
        formatted_date = date_obj.strftime('%d/%m/%Y')
    else:
        formatted_date = "Date inconnue"
    html_content += f'        <div class="card" data-image="{images_dir}/{image}" data-date="{formatted_date}">\n'
    html_content += f'          <p class="date">{formatted_date}</p>\n'
    html_content += '          <p class="title">Balance Patch</p>\n'
    html_content += '        </div>\n'
html_content += '      </div>\n'
html_content += '    </div>\n'
html_content += '    <div class="detail-view" id="detail-view" style="display: none;">\n'
html_content += '      <h2 id="detail-caption"></h2>\n'
html_content += '      <div class="detail-buttons">\n'
html_content += '        <button id="back-button">Back</button>\n'
html_content += '        <button id="toggle-negative-button">Show white picture</button>\n'
html_content += '      </div>\n'
html_content += '      <img id="detail-img" src="" alt="Balance Patch en grand" style="filter: invert(1);">\n'
html_content += '    </div>\n'
html_content += '  </div>\n'  # Fin onglet Gallerie

# Onglet Stats (deux colonnes)
html_content += '  <div id="stats-container" style="display: none;">\n'
html_content += '    <div class="container">\n'
html_content += '      <div class="stats-columns">\n'
# Colonne de gauche : Classement des BP
html_content += '        <div class="stats-column">\n'
html_content += '          <h2>Balance Patch Stats</h2>\n'
html_content += '          <ul id="bp-stats-list">\n'
for i, (bp, count) in enumerate(bp_stats):
    if i < 10:
        html_content += f'            <li>{bp} : {count} monstres</li>\n'
    else:
        html_content += f'            <li class="more-bp hidden">{bp} : {count} monstres</li>\n'
html_content += '          </ul>\n'
html_content += '          <button id="more-bp-button">More</button>\n'
html_content += '        </div>\n'
# Colonne de droite : Classement des monstres
html_content += '        <div class="stats-column">\n'
html_content += '          <h2>Monsters Stats</h2>\n'
html_content += '          <ul id="monster-stats-list">\n'
for i, (monster, dates) in enumerate(monster_stats):
    count = len(dates)
    if i < 15:
        html_content += f'            <li>{monster} : {count} apparitions</li>\n'
    else:
        html_content += f'            <li class="more-monsters hidden">{monster} : {count} apparitions</li>\n'
html_content += '          </ul>\n'
html_content += '          <button id="more-monster-button">More</button>\n'
html_content += '        </div>\n'
html_content += '      </div>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'  # Fin onglet Stats

# Onglet Liste
html_content += '  <div id="list-container" style="display: none;">\n'
html_content += '    <div class="container">\n'
html_content += '      <h2>Monsters List</h2>\n'
html_content += '      <ul>\n'
for monster in monsters_list:
    html_content += f'        <li>{monster}</li>\n'
html_content += '      </ul>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'  # Fin onglet Liste

# Footer
html_content += '  <footer>\n'
html_content += '    <p>By B4tiste</p>\n'
html_content += '  </footer>\n'

# Inclusion des scripts
html_content += '  <script src="script.js"></script>\n'
html_content += '  <script>\n'
html_content += '    // Gestion des onglets\n'
html_content += '    const galleryTab = document.getElementById("gallery-tab");\n'
html_content += '    const statsTab = document.getElementById("stats-tab");\n'
html_content += '    const listTab = document.getElementById("list-tab");\n'
html_content += '    const galleryContainer = document.getElementById("gallery-container");\n'
html_content += '    const statsContainer = document.getElementById("stats-container");\n'
html_content += '    const listContainer = document.getElementById("list-container");\n'
html_content += '    \n'
html_content += '    galleryTab.addEventListener("click", function() {\n'
html_content += '      galleryContainer.style.display = "block";\n'
html_content += '      statsContainer.style.display = "none";\n'
html_content += '      listContainer.style.display = "none";\n'
html_content += '      galleryTab.classList.add("active");\n'
html_content += '      statsTab.classList.remove("active");\n'
html_content += '      listTab.classList.remove("active");\n'
html_content += '    });\n'
html_content += '    \n'
html_content += '    statsTab.addEventListener("click", function() {\n'
html_content += '      galleryContainer.style.display = "none";\n'
html_content += '      statsContainer.style.display = "block";\n'
html_content += '      listContainer.style.display = "none";\n'
html_content += '      statsTab.classList.add("active");\n'
html_content += '      galleryTab.classList.remove("active");\n'
html_content += '      listTab.classList.remove("active");\n'
html_content += '    });\n'
html_content += '    \n'
html_content += '    listTab.addEventListener("click", function() {\n'
html_content += '      galleryContainer.style.display = "none";\n'
html_content += '      statsContainer.style.display = "none";\n'
html_content += '      listContainer.style.display = "block";\n'
html_content += '      listTab.classList.add("active");\n'
html_content += '      galleryTab.classList.remove("active");\n'
html_content += '      statsTab.classList.remove("active");\n'
html_content += '    });\n\n'
html_content += '    // Bouton More pour BP stats\n'
html_content += '    document.getElementById("more-bp-button").addEventListener("click", function() {\n'
html_content += '      var hiddenItems = document.querySelectorAll(".more-bp");\n'
html_content += '      hiddenItems.forEach(item => {\n'
html_content += '        if (item.style.display === "list-item") {\n'
html_content += '          item.style.display = "none";\n'
html_content += '          this.textContent = "More";\n'
html_content += '        } else {\n'
html_content += '          item.style.display = "list-item";\n'
html_content += '          this.textContent = "Less";\n'
html_content += '        }\n'
html_content += '      });\n'
html_content += '    });\n\n'
html_content += '    // Bouton More pour Monster stats\n'
html_content += '    document.getElementById("more-monster-button").addEventListener("click", function() {\n'
html_content += '      var hiddenItems = document.querySelectorAll(".more-monsters");\n'
html_content += '      hiddenItems.forEach(item => {\n'
html_content += '        if (item.style.display === "list-item") {\n'
html_content += '          item.style.display = "none";\n'
html_content += '          this.textContent = "More";\n'
html_content += '        } else {\n'
html_content += '          item.style.display = "list-item";\n'
html_content += '          this.textContent = "Less";\n'
html_content += '        }\n'
html_content += '      });\n'
html_content += '    });\n'
html_content += '  </script>\n'
html_content += '</body>\n</html>\n'

# Écriture du contenu HTML dans le fichier de sortie
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Index file created: {output_file}")
