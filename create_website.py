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
# Insertion du code Google Tag Manager dans le <head>
html_content += '  <!-- Google Tag Manager -->\n'
html_content += '  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({\'gtm.start\':\n'
html_content += '  new Date().getTime(),event:\'gtm.js\'});var f=d.getElementsByTagName(s)[0],\n'
html_content += '  j=d.createElement(s),dl=l!=\'dataLayer\'?\'&l=\'+l:\'\';j.async=true;j.src=\n'
html_content += '  \'https://www.googletagmanager.com/gtm.js?id=\'+i+dl;f.parentNode.insertBefore(j,f);\n'
html_content += '  })(window,document,\'script\',\'dataLayer\',\'GTM-WNZ8DLWF\');</script>\n'
html_content += '  <!-- End Google Tag Manager -->\n'
html_content += '  <meta charset="UTF-8">\n'
html_content += '  <title>BP Gallery</title>\n'
html_content += '  <link rel="stylesheet" type="text/css" href="style.css">\n'
html_content += '  <style>\n'
html_content += '    /* Styles pour les onglets et la mise en page des colonnes dans Stats */\n'
html_content += '    .tab-container { display: flex; justify-content: center; margin-top: 20px; }\n'
html_content += '    .tab-button { padding: 10px 20px; margin: 0 5px; font-size: 1rem; cursor: pointer; background-color: #3a3a3a; color: #e0e0e0; border: none; border-radius: 4px; transition: background-color 0.3s; }\n'
html_content += '    .tab-button.active { background-color: #007bff; color: #fff; }\n'
html_content += '    .stats-columns { display: flex; justify-content: space-between; flex-wrap: wrap; }\n'
html_content += '    .stats-column { flex: 1; margin: 10px; min-width: 300px; }\n'
html_content += '    .hidden { display: none; }\n'
html_content += '  </style>\n'
html_content += '</head>\n'
# Insertion du code Google Tag Manager (noscript) juste après l'ouverture du <body>
html_content += '<body>\n'
html_content += '  <!-- Google Tag Manager (noscript) -->\n'
html_content += '  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WNZ8DLWF"\n'
html_content += '  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
html_content += '  <!-- End Google Tag Manager (noscript) -->\n'

# Navigation avec 4 onglets
html_content += '  <div class="tab-container">\n'
html_content += '    <button class="tab-button active" id="gallery-tab">BP List</button>\n'
html_content += '    <button class="tab-button" id="stats-tab">BP & Monsters Stats</button>\n'
html_content += '    <button class="tab-button" id="list-tab">Monsters List</button>\n'
html_content += '    <button class="tab-button" id="about-tab">About Me</button>\n'
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
# Colonne de gauche : Balance Patch Stats
html_content += '        <div class="stats-column">\n'
html_content += '          <h2>Balance Patch Stats</h2>\n'
html_content += '          <ul id="bp-stats-list">\n'
for i, (bp, count) in enumerate(bp_stats):
    if i < 10:
        html_content += f'            <li>{bp} : {count} monsters</li>\n'
    else:
        html_content += f'            <li class="more-bp hidden">{bp} : {count} monsters</li>\n'
html_content += '          </ul>\n'
html_content += '          <button id="more-bp-button">More</button>\n'
html_content += '        </div>\n'
# Colonne de droite : Monsters Stats
html_content += '        <div class="stats-column">\n'
html_content += '          <h2>Monsters Stats</h2>\n'
html_content += '          <ul id="monster-stats-list">\n'
for i, (monster, dates) in enumerate(monster_stats):
    count = len(dates)
    if i < 15:
        html_content += f'            <li>{monster} : {count} BPs</li>\n'
    else:
        html_content += f'            <li class="more-monsters hidden">{monster} : {count} BPs</li>\n'
html_content += '          </ul>\n'
html_content += '          <button id="more-monster-button">More</button>\n'
html_content += '        </div>\n'
html_content += '      </div>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'  # Fin onglet Stats

# Onglet Liste (liste alphabétique)
html_content += '  <div id="list-container" style="display: none;">\n'
html_content += '    <div class="container">\n'
html_content += '      <h2>Monsters List</h2>\n'
html_content += '      <h3>Click on a monster to display his list of BPs !</h3>\n'
html_content += '      <ul>\n'
for monster in monsters_list:
    html_content += f'        <li>{monster}</li>\n'
html_content += '      </ul>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'  # Fin onglet Liste

# Nouvel onglet About Me
html_content += '  <div id="about-container" style="display: none;">\n'
html_content += '    <div class="container">\n'
html_content += '      <h2>About Me</h2>\n'
html_content += "      <p>I'm B4tiste, a SW player that love creating tools for the community. Feel free to reeach to me on Discord @b4tiste to chat. You can support my work using the Donation button below, this will be very much appreciated !!</p>\n"
html_content += '      <form action="https://www.paypal.com/donate" method="post" target="_top">\n'
html_content += '        <input type="hidden" name="hosted_button_id" value="7MQNCEX6C3B4C" />\n'
html_content += '        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />\n'
html_content += '        <img alt="" border="0" src="https://www.paypal.com/en_FR/i/scr/pixel.gif" width="1" height="1" />\n'
html_content += '      </form>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'  # Fin onglet About Me

# Footer (sans bouton de donation)
html_content += '  <footer>\n'
html_content += '    <p>By B4tiste (@b4tiste on Discord)</p>\n'
html_content += '  </footer>\n'
html_content += '  <script src="script.js"></script>\n'
html_content += '</body>\n</html>\n'

# Écriture du contenu HTML dans le fichier de sortie
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Index file created: {output_file}")
