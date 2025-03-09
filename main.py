import config
import data_processing
import html_generator
import json

def main():
    # Chargement des données
    monster_dates = data_processing.load_monster_dates()
    all_monsters = data_processing.load_all_monsters()

    # Récupération des liens vers les images de tous les monstres
    monster_images = data_processing.load_monster_images(all_monsters)

    # Traitement des données
    monsters_list = data_processing.get_monsters_list(monster_dates)
    bp_counts = data_processing.compute_bp_counts(monster_dates)
    bp_stats = data_processing.compute_bp_stats(bp_counts)
    monster_stats = data_processing.compute_monster_stats(monster_dates)
    sorted_images = data_processing.get_sorted_images()

    monsters_natural5 = data_processing.filter_monsters_natural5(all_monsters)
    monsters_natural4 = data_processing.filter_monsters_natural4(all_monsters)
    available_monsters = data_processing.get_available_monsters(monsters_natural5 + monsters_natural4)
    monsters_not_in_dates_sorted = data_processing.filter_monsters_not_in_dates(
        monsters_natural5 + monsters_natural4,
        monster_dates,
        config.COLLAB_MAPPING,
        available_monsters
    )

    # Génération du contenu HTML
    html_content = html_generator.generate_html(sorted_images, bp_stats, monster_stats, monsters_not_in_dates_sorted, monsters_list, monster_images)

    # Écriture dans le fichier de sortie
    with open(config.OUTPUT_HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Index file created: {config.OUTPUT_HTML_FILE}")

if __name__ == "__main__":
    main()
