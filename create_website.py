import os
import re
import locale
import json
import unicodedata
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

# Fonction de normalisation d'une chaîne (minuscule, suppression des accents)
def normalize_monster_name(name):
    name = name.lower()
    normalized = unicodedata.normalize('NFKD', name)
    return ''.join(c for c in normalized if not unicodedata.combining(c))

# Fonction pour vérifier que la chaîne est composée uniquement de caractères ASCII
def is_ascii(s):
    return all(ord(c) < 128 for c in s)

# Chargement du fichier JSON contenant les dates associées aux monstres
with open('monster_dates.json', 'r', encoding='utf-8') as f:
    monster_dates = json.load(f)

# Liste des monstres (les clés du fichier monster_dates) triée par ordre alphabétique
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

# Récupérer et trier les fichiers images par date (du plus récent au plus ancien)
image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]
sorted_images = sorted(image_files, key=extract_date, reverse=True)

# ------------------------------------------------------------
# Chargement du fichier data/monsters.json pour récupérer tous les monstres du jeu
with open(os.path.join('data', 'monsters.json'), 'r', encoding='utf-8') as f:
    all_monsters_data = json.load(f)
all_monsters = all_monsters_data["monsters"]

# Filtrer les monstres ayant natural_stars == 5 et awaken_level > 0
# et éliminer ceux dont le nom contient des caractères non-ASCII
monsters_natural5 = [
    monster for monster in all_monsters
    if monster.get("natural_stars") == 5
       and monster.get("awaken_level") > 0
       and is_ascii(monster["name"])
]

# Construire l'ensemble des noms disponibles dans monsters_natural5 (normalisés)
available_monsters = {normalize_monster_name(monster["name"]) for monster in monsters_natural5}

# Dictionnaire de correspondance pour les monstres collab.
# La clé est le nom collab composé de l'élément et du nom (normalisés),
# et la valeur est le nom (normalisé) du "copain" associé.
collab_mapping = {
    # STREET_FIGHTER - DHALSIM
    "water dhalsim": "kyle",
    "fire dhalsim": "todd",
    "wind dhalsim": "jarrett",
    "light dhalsim": "hekerson",
    "dark dhalsim": "cayde",
    # STREET_FIGHTER - CHUN LI
    "water chun li": "lariel",
    "fire chun li": "berenice",
    "wind chun li": "cordelia",
    "light chun li": "leah",
    "dark chun li": "vereesa",
    # STREET_FIGHTER - KEN
    "fire ken": "bernadotte",
    # STREET_FIGHTER - RYU
    "water ryu": "moore",
    "fire ryu": "douglas",
    "wind ryu": "kashmir",
    "light ryu": "talisman",
    "dark ryu": "vancliffe",
    # STREET_FIGHTER - MBISON
    "water m. bison": "borgnine",
    "fire m. bison": "karnal",
    "wind m. bison": "sagar",
    "light m. bison": "craig",
    "dark m. bison": "gurkha",
    # COOKIE_RUN_KINGDOM - ESPRESSO
    "water espresso": "rosemary",
    "fire espresso": "hibiscus",
    "wind espresso": "chamomile",
    "light espresso": "jasmine",
    "dark espresso": "lavender",
    # COOKIE_RUN_KINGDOM - MADELEINE COOKIE
    "water madeleine cookie": "ganache",
    "fire madeleine cookie": "pave",
    "wind madeleine cookie": "praline",
    "light madeleine cookie": "fudge",
    "dark madeleine cookie": "truffle",
    # COOKIE_RUN_KINGDOM - GINGERBRAVE
    "wind gingerbrave": "thomas",
    # COOKIE_RUN_KINGDOM - PURE VANILLA COOKIE
    "water pure vanilla cookie": "adriana",
    "fire pure vanilla cookie": "lucia",
    "wind pure vanilla cookie": "angela",
    "light pure vanilla cookie": "ariana",
    "dark pure vanilla cookie": "elena",
    # COOKIE_RUN_KINGDOM - HOLLYBERRY COOKIE
    "water hollyberry cookie": "manon",
    "fire hollyberry cookie": "alice",
    "wind hollyberry cookie": "jade",
    "light hollyberry cookie": "audrey",
    "dark hollyberry cookie": "giselle",
    # ASSASSINS CREED - Altaïr
    "light altair": "frederic",
    # ASSASSINS CREED - EZIO
    "water ezio": "lionel",
    "fire ezio": "patrick",
    "wind ezio": "hector",
    "light ezio": "ian",
    "dark ezio": "evan",
    # ASSASSINS CREED - BAYEK
    "water bayek": "omar",
    "fire bayek": "ashour",
    "wind bayek": "shahat",
    "light bayek": "ahmed",
    "dark bayek": "salah",
    # ASSASSINS CREED - KASSANDRA
    "water kassandra": "kalantatze",
    "fire kassandra": "federica",
    "wind kassandra": "eleni",
    "light kassandra": "aurelia",
    "dark kassandra": "kiara",
    # ASSASSINS CREED - EIVOR
    "water eivor": "brita",
    "fire eivor": "solveig",
    "wind eivor": "astrid",
    "light eivor": "berghild",
    "dark eivor": "sigrid",
    # THE WITCHER 3 - GERALT
    "water geralt": "anders",
    "fire geralt": "patrick",
    "wind geralt": "magnus",
    "light geralt": "lars",
    "dark geralt": "valdemar",
    # THE WITCHER 3 - YENNEFER
    "water yennefer": "johanna",
    "fire yennefer": "tarnisha",
    "wind yennefer": "hexarina",
    "light yennefer": "arcana",
    "dark yennefer": "hilda",
    # THE WITCHER 3 - TRISS
    "water triss": "lumina",
    "fire triss": "enshia",
    "wind triss": "nobella",
    "light triss": "groa",
    "dark triss": "celestara",
    # THE WITCHER 3 - CIRI
    "water ciri": "rigna",
    "fire ciri": "reyka",
    "wind ciri": "tirsa",
    "light ciri": "birgitta",
    "dark ciri": "fiona",
    # JUJUTSU KAISEN - YUJI ITADORI
    "water yuji itadori": "mark",
    "fire yuji itadori": "rick",
    "wind yuji itadori": "sean",
    "light yuji itadori": "guy",
    "dark yuji itadori": "jack",
    # JUJUTSU KAISEN - MEGUMI fushiguro
    "water megumi fushiguro": "hiroyuki",
    "fire megumi fushiguro": "tetsuya",
    "wind megumi fushiguro": "kuroshu",
    "light megumi fushiguro": "ginjo",
    "dark megumi fushiguro": "doburoku",
    # JUJUTSU KAISEN - NOBARA KUGISAKI
    "water nobara kugisaki": "mizuki",
    "fire nobara kugisaki": "sayumi",
    "wind nobara kugisaki": "aya",
    "light nobara kugisaki": "haruka",
    "dark nobara kugisaki": "yuko",
    # JUJUTSU KAISEN - SATORU GOJO
    "water satoru gojo": "jurgen",
    "fire satoru gojo": "hartmann",
    "wind satoru gojo": "vincent",
    "light satoru gojo": "werner",
    "dark satoru gojo": "sigmund",
    # JUJUTSU KAISEN - DARK RYOMEN SUKUNA
    "dark ryomen sukuna": "hayato",
}

# Normaliser les clés du fichier monster_dates
normalized_monster_dates = {normalize_monster_name(name) for name in monster_dates}

# Filtrer : ne conserver que les monstres Natural 5 dont le nom est entièrement ASCII,
# qui ne figurent pas déjà dans monster_dates et qui ne doivent pas être exclus via le mapping collab.
monsters_not_in_dates = []
for monster in monsters_natural5:
    norm_name = normalize_monster_name(monster["name"])
    norm_element = normalize_monster_name(monster["element"])
    # Si le nom original contient des caractères non-ASCII, on l'ignore
    if not is_ascii(monster["name"]):
        continue
    # Construction de la clé collab, par ex. "dark ryomen sukuna"
    collab_key = f"{norm_element} {norm_name}"
    # Exclure le monstre s'il est déjà présent dans monster_dates (comparaison sur le nom seul)
    if norm_name in normalized_monster_dates:
        continue
    # Si c'est un monstre collab, vérifier si son "copain" est disponible dans available_monsters
    if collab_key in collab_mapping:
        counterpart = collab_mapping[collab_key]
        if counterpart in available_monsters:
            continue
    monsters_not_in_dates.append(monster)

# Trier la liste par nom normalisé
monsters_not_in_dates_sorted = sorted(monsters_not_in_dates, key=lambda m: normalize_monster_name(m["name"]))

# Retirer les monstres "homunculus" de la liste
monsters_not_in_dates_sorted = [monster for monster in monsters_not_in_dates_sorted if "homunculus" not in monster["name"].lower()]
# ------------------------------------------------------------

# Création du contenu HTML sans les scripts liés à Google Analytics/Tag Manager
html_content = '<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
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
html_content += '<body>\n'

# Navigation
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
html_content += '  </div>\n'

# Onglet Stats
html_content += '  <div id="stats-container" style="display: none;">\n'
html_content += '    <div class="container">\n'
html_content += '      <div class="stats-columns">\n'
# Colonne 1 : Balance Patch Stats
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
# Colonne 2 : Monsters Stats
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
# Colonne 3 : Monsters Natural 5 (Not in Dates)
html_content += '        <div class="stats-column">\n'
html_content += '          <h2>Monsters that never made it to the BPs</h2>\n'
html_content += '          <ul id="monsters-not-in-dates">\n'
for i, monster in enumerate(monsters_not_in_dates_sorted):
    norm_name = normalize_monster_name(monster["name"]).capitalize() + " (" + monster["element"] + ")"
    if i < 15:
        html_content += f'            <li>{norm_name}</li>\n'
    else:
        html_content += f'            <li class="more-non-bp hidden">{norm_name}</li>\n'
html_content += '          </ul>\n'
html_content += '          <button id="more-non-bp-button">More</button>\n'
html_content += '        </div>\n'
html_content += '      </div>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'

# Onglet Liste
html_content += '  <div id="list-container" style="display: none;">\n'
html_content += '    <div class="container">\n'
html_content += '      <h2>Monsters List</h2>\n'
html_content += '      <h3>Click on a monster to display his list of BPs !</h3>\n'
html_content += '      <ul>\n'
for monster in monsters_list:
    html_content += f'        <li>{monster}</li>\n'
html_content += '      </ul>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'

# Onglet About Me
html_content += '  <div id="about-container" style="display: none;">\n'
html_content += '    <div class="container">\n'
html_content += '      <h2>About Me</h2>\n'
html_content += "      <p>I'm B4tiste, a SW player that love creating tools for the community. Feel free to reach out to me on Discord @b4tiste to chat. You can support my work using the Donation button below, this will be very much appreciated !!</p>\n"
html_content += '      <form action="https://www.paypal.com/donate" method="post" target="_top">\n'
html_content += '        <input type="hidden" name="hosted_button_id" value="7MQNCEX6C3B4C" />\n'
html_content += '        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />\n'
html_content += '        <img alt="" border="0" src="https://www.paypal.com/en_FR/i/scr/pixel.gif" width="1" height="1" />\n'
html_content += '      </form>\n'
html_content += '    </div>\n'
html_content += '  </div>\n'

# Footer
html_content += '  <footer>\n'
html_content += '    <p>By B4tiste (@b4tiste on Discord)</p>\n'
html_content += '  </footer>\n'
html_content += '  <script src="script.js"></script>\n'
html_content += '</body>\n</html>\n'

# Écriture du contenu HTML dans le fichier de sortie
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Index file created: {output_file}")
