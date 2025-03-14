import re
from datetime import datetime
import config

def generate_html(sorted_images, bp_stats, monster_stats, monsters_not_in_dates_sorted, monsters_list, monster_images):
    # Conversion de bp_stats en dictionnaire pour faciliter la recherche : date -> count
    bp_dict = dict(bp_stats)

    html_content = '<!DOCTYPE html>\n<html lang="fr">\n<head>\n'
    html_content += '  <meta charset="UTF-8">\n'
    html_content += '  <title>Balance Patch Gallery</title>\n'
    html_content += '  <link rel="icon" type="image/x-icon" href="favicon.ico">\n'
    html_content += '  <link rel="stylesheet" type="text/css" href="style.css">\n'
    html_content += '  <meta property="og:title" content="Summoners War Balance Patch Gallery" />\n'
    html_content += '  <meta property="og:description" content="Looking for a specific Balance Patch Note ? This gallery is made for you !" />\n'
    html_content += '  <meta property="og:image" content="https://bp-archive.netlify.app/preview.png" />\n'
    html_content += '  <meta property="og:url" content="https://bp-archive.netlify.app/" />\n'
    html_content += '</head>\n'
    html_content += '<body>\n'

    # Navigation
    html_content += '  <div class="tab-container">\n'
    html_content += '    <button class="tab-button active" id="gallery-tab">BP List</button>\n'
    html_content += '    <button class="tab-button" id="stats-tab">BP & Monsters Stats</button>\n'
    html_content += '    <button class="tab-button" id="list-tab">Monsters List</button>\n'
    html_content += '    <button class="tab-button" id="about-tab">About</button>\n'
    html_content += '  </div>\n'

    # Onglet Galerie
    html_content += '  <div id="gallery-container">\n'
    html_content += '    <div class="container" id="grid-container">\n'
    html_content += '      <h1>Summoners War Balance Patch Gallery</h1>\n'
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
        # Récupération du nombre de monstres pour ce BP (par date)
        count = bp_dict.get(formatted_date, 0)
        html_content += f'        <div class="card" data-image="{config.IMAGES_DIR}/{image}" data-date="{formatted_date}">\n'
        html_content += f'          <p class="date">{formatted_date}</p>\n'
        html_content += f'          <p class="count">{count} monsters</p>\n' if count > 1 else f'          <p class="count">{count} monster</p>\n'
        html_content += '        </div>\n'
    html_content += '      </div>\n'
    html_content += '    </div>\n'
    html_content += '    <div class="detail-view hidden" id="detail-view">\n'
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
    html_content += '      <div id="loader" class="loader hidden"></div>\n'
    html_content += '      <!-- L\'image sera affichée après chargement -->\n'
    html_content += '      <img id="detail-img" src="" alt="Balance Patch en grand">\n'
    html_content += '    </div>\n'
    html_content += '  </div>\n'

    # Onglet Stats
    html_content += '  <div id="stats-container" class="hidden">\n'
    html_content += '    <div class="container">\n'
    html_content += '      <div class="stats-columns">\n'
    # Colonne 1 : Balance Patch Stats
    html_content += '        <div class="stats-column">\n'
    html_content += '          <h2>BPs with the most changes</h2>\n'
    html_content += '          <h3>Total: ' + str(len(bp_stats)) + ' monster related BPs</h3>\n'
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
    html_content += '          <h2>Monsters sorted by BPs amount</h2>\n'
    html_content += '          <ul id="monster-stats-list">\n'
    for i, (monster, dates) in enumerate(monster_stats):
        count = len(dates)
        img_url = monster_images[monster.lower()]
        if i < 15:
            html_content += f'            <li><img src={img_url} alt="{monster}"> {monster} : {count} BPs</li>\n'
        else:
            html_content += f'            <li class="more-monsters hidden"><img data-src="{img_url}" alt="{monster}"> {monster} : {count} BPs</li>\n'
    html_content += '          </ul>\n'
    html_content += '          <button id="more-monster-button">More</button>\n'
    html_content += '        </div>\n'
    # Colonne 3 : Monsters not in dates
    html_content += '        <div class="stats-column">\n'
    html_content += '          <h2>Oldest 4*/5* Monsters that never made it to the BPs</h2>\n'
    html_content += f'         <h3>Total: {len(monsters_not_in_dates_sorted)} monsters</h3>\n'
    html_content += '          <ul id="monsters-not-in-dates">\n'
    for i, monster in enumerate(monsters_not_in_dates_sorted):
        norm_name = f"{monster['name'].capitalize()}"
        img_url = monster_images[monster["name"].lower()]
        if i < 10:
            html_content += f'            <li><img src={img_url} alt="{monster["name"]}"> {norm_name} </li>\n'
        else:
            html_content += f'            <li class="more-non-bp hidden"><img data-src="{img_url}" alt="{monster["name"]}"> {norm_name} </li>\n'
    html_content += '          </ul>\n'
    html_content += '          <button id="more-non-bp-button">More</button>\n'
    html_content += '        </div>\n'
    html_content += '      </div>\n'
    html_content += '    </div>\n'
    html_content += '  </div>\n'

    # Onglet Liste
    html_content += '  <div id="list-container" class="hidden">\n'
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
    html_content += '  <div id="about-container" class="hidden">\n'
    html_content += '    <div class="container">\n'
    html_content += '      <h2>About</h2>\n'
    html_content += "      <p>I'm B4tiste, a SW player that love creating tools for the community. Feel free to reach out to me on Discord @b4tiste to chat. You can support my work using the Donation button below, this will be very much appreciated !!</p>\n"
    html_content += '      <form action="https://www.paypal.com/donate" method="post" target="_top">\n'
    html_content += '        <input type="hidden" name="hosted_button_id" value="7MQNCEX6C3B4C" />\n'
    html_content += '        <input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />\n'
    html_content += '        <img alt="" border="0" src="https://www.paypal.com/en_FR/i/scr/pixel.gif" width="1" height="1" />\n'
    html_content += '      </form>\n'
    html_content += '      <p>My other project: <a href="https://github.com/B4tiste/bot-swbox" target="_blank">BOT-swbox</a> is a Discord RTA Bot</p>\n'
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
