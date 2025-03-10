import os
import re
import json
import unicodedata
from datetime import datetime
import config

# Extraction de la date à partir du nom de fichier
def extract_date(filename):
    match = re.search(r'(\d{2}_\d{2}_\d{4})', filename)
    if match:
        return datetime.strptime(match.group(1), '%d_%m_%Y')
    return datetime.min

# Normalisation d'une chaîne (minuscule, suppression des accents)
def normalize_monster_name(name):
    name = name.lower()
    normalized = unicodedata.normalize('NFKD', name)
    return ''.join(c for c in normalized if not unicodedata.combining(c))

# Vérification que la chaîne est composée uniquement de caractères ascii ou dérivés
def is_ascii(s):
    return all(ord(c) < 255 for c in s)

# Chargement du fichier JSON contenant les dates associées aux monstres
def load_monster_dates():
    with open(config.MONSTER_DATES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Chargement du fichier JSON contenant tous les monstres du jeu
def load_all_monsters():
    with open(config.MONSTERS_DATA_FILE, 'r', encoding='utf-8') as f:
        all_monsters = json.load(f)
        return [monster for monster in all_monsters["monsters"] if monster.get("obtainable", True)]

# Chargement des urls d'images des monstres
def load_monster_images(all_monsters):
    base_image_url = "https://swarfarm.com/static/herders/images/monsters/"
    monster_images = {normalize_monster_name(monster["name"]): base_image_url + monster["image_filename"] for monster in all_monsters}
    return monster_images

# Liste des monstres présents dans le fichier monster_dates, triée par ordre alphabétique
def get_monsters_list(monster_dates):
    return sorted(monster_dates.keys())

# Calcul du nombre de monstres par BP à partir de monster_dates
def compute_bp_counts(monster_dates):
    bp_counts = {}
    for dates in monster_dates.values():
        for date_str in dates:
            bp_counts[date_str] = bp_counts.get(date_str, 0) + 1
    return bp_counts

# Classement des BP par nombre décroissant de monstres
def compute_bp_stats(bp_counts):
    return sorted(bp_counts.items(), key=lambda x: x[1], reverse=True)

# Classement des monstres par nombre d'apparitions décroissant
def compute_monster_stats(monster_dates):
    return sorted(monster_dates.items(), key=lambda x: len(x[1]), reverse=True)

# Récupérer et trier les fichiers images par date (du plus récent au plus ancien)
def get_sorted_images():
    image_files = [f for f in os.listdir(config.IMAGES_DIR) if os.path.isfile(os.path.join(config.IMAGES_DIR, f))]
    return sorted(image_files, key=extract_date, reverse=True)

# Filtrer les monstres avec natural_stars == 5, awaken_level > 0 et nom en ASCII
def filter_monsters_natural5(all_monsters):
    return [
        monster for monster in all_monsters
        if monster.get("natural_stars") == 5 and monster.get("awaken_level", 0) > 0 and is_ascii(monster["name"])
    ]

# Filtrer les monstres avec natural_stars == 4, awaken_level > 0 et nom en ASCII
def filter_monsters_natural4(all_monsters):
    return [
        monster for monster in all_monsters
        if monster.get("natural_stars") == 4 and monster.get("awaken_level", 0) > 0 and is_ascii(monster["name"])
    ]

# Construire l'ensemble des noms disponibles dans monsters_natural5 (normalisés)
def get_available_monsters(monsters):
    return {normalize_monster_name(monster["name"]) for monster in monsters}

# Filtrer les monstres Natural 5 qui ne figurent pas déjà dans monster_dates et qui ne sont pas à exclure via le mapping collab
def filter_monsters_not_in_dates(monsters, monster_dates, collab_mapping, available_monsters):
    normalized_monster_dates = {normalize_monster_name(name) for name in monster_dates}
    monsters_not_in_dates = []
    for monster in monsters:
        norm_name = normalize_monster_name(monster["name"])
        norm_element = normalize_monster_name(monster["element"])
        if norm_name in normalized_monster_dates:
            continue
        collab_key = f"{norm_element} {norm_name}"
        if collab_key in collab_mapping:
            counterpart = collab_mapping[collab_key]
            if counterpart in available_monsters:
                continue
        monsters_not_in_dates.append(monster)
    # Trier par "id"
    monsters_not_in_dates_sorted = sorted(monsters_not_in_dates, key=lambda x: x["id"])
    # Retirer les monstres "homunculus"
    return [monster for monster in monsters_not_in_dates_sorted if "homunculus" not in monster["name"].lower()]
