import re
from datetime import datetime
import config

def generate_html(sorted_images, bp_stats, monster_stats, monsters_not_in_dates_sorted, monsters_list):
    html_content = '<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
    html_content += '  <meta charset="UTF-8">\n'
    html_content += '  <title>BP Gallery</title>\n'
    html_content += '  <link rel="stylesheet" type="text/css" href="style.css">\n'
    html_content += '  <style>\n'
    html_content += '    /* Styles pour les onglets et la mise en page des colonnes dans Stats */\n'
    html_content += '    .tab-container { display: flex; justify-content: center; margin-top: 20px; }\n'
    html_content += '    .tab-button { padding: 10px 20px; margin: 0 5px; font-size: 1rem; cursor: pointer; background-color: #3a3a3a; color: #e0e0e0; border: none; border-radius: 4px; transition: background-color 0.3s; }\n'
    html_content += '    .tab-button.active { background-color: #28a745; color: #fff; }\n'
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

    # Onglet Galerie
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
        html_content += f'        <div class="card" data-image="{config.IMAGES_DIR}/{image}" data-date="{formatted_date}">\n'
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
    html_content += '      <div class="detail-navigation">\n'
    html_content += '        <button id="prev-button">←</button>\n'
    html_content += '        <span id="detail-index"></span>\n'
    html_content += '        <button id="next-button">→</button>\n'
    html_content += '      </div>\n'
    html_content += '      <!-- Loader -->\n'
    html_content += '      <div id="loader" class="loader" style="display: none;"></div>\n'
    html_content += '      <!-- L\'image sera affichée après chargement -->\n'
    html_content += '      <img id="detail-img" src="" alt="Balance Patch en grand" style="filter: invert(1); display: none;">\n'
    html_content += '    </div>\n'
    html_content += '  </div>\n'

    # Onglet Stats
    html_content += '  <div id="stats-container" style="display: none;">\n'
    html_content += '    <div class="container">\n'
    html_content += '      <div class="stats-columns">\n'
    # Colonne 1 : Balance Patch Stats
    html_content += '        <div class="stats-column">\n'
    html_content += '          <h2>Balance Patch Stats</h2>\n'
    html_content += '          <h3>Total: ' + str(len(bp_stats)) + ' BPs</h3>\n'
    html_content += '          <ul id="bp-stats-list">\n'
    for i, (bp, count) in enumerate(bp_stats):
        if i < 15:
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
    # Colonne 3 : Monsters not in dates
    html_content += '        <div class="stats-column">\n'
    html_content += '          <h2>4*/5* Monsters that never made it to the BPs</h2>\n'
    html_content += f'         <h3>Total: {len(monsters_not_in_dates_sorted)} monsters</h3>\n'
    html_content += '          <ul id="monsters-not-in-dates">\n'
    for i, monster in enumerate(monsters_not_in_dates_sorted):
        # On affiche le nom normalisé avec la première lettre en majuscule et l'élément
        norm_name = f"{monster['name'].capitalize()} ({monster['element']})"
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
    html_content += '      <h3>Total: ' + str(len(monsters_list)) + ' monsters</h3>\n'
    html_content += '      <ul>\n'
    for monster in monsters_list:
        html_content += f'        <li>{monster}</li>\n'
    html_content += '      </ul>\n'
    html_content += '    </div>\n'
    html_content += '  </div>\n'

    # Onglet About Me
    html_content += '  <div id="about-container" style="display: none;">\n'
    html_content += '    <div class="container">\n'
    html_content += '      <h2>About</h2>\n'
    html_content += "      <p>I'm B4tiste, a SW player that love creating tools for the community. Feel free to reach out to me on Discord @b4tiste to chat. You can support my work using the Donation button below, this will be very much appreciated !!</p>\n"
    html_content += '      <form action="https://www.paypal.com/donate" method="post" target="_top">\n'
    html_content += '        <input type="hidden" name="hosted_button_id" value="7MQNCEX6C3B4C" />\n'
    html_content += '        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />\n'
    html_content += '        <img alt="" border="0" src="https://www.paypal.com/en_FR/i/scr/pixel.gif" width="1" height="1" />\n'
    html_content += '      </form>\n'
    html_content += "      <p>Thanks to Spokland for the update gathering over the years</p>\n"
    html_content += '    </div>\n'
    html_content += '  </div>\n'

    # Footer
    html_content += '  <footer>\n'
    html_content += '    <p>By <strong>B4tiste</strong> (@b4tiste on Discord)</p>\n'
    html_content += '  </footer>\n'
    html_content += '  <script src="script.js"></script>\n'
    html_content += '</body>\n</html>\n'

    return html_content
