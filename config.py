import os
import locale

# Définir la locale en français pour le formatage des dates
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Répertoires et chemins
BASE_DIR = "."
DATA_DIR = "data"
IMAGES_DIR = "images"

# Fichiers de données
MONSTER_DATES_FILE = os.path.join(BASE_DIR, 'monster_dates.json')
MONSTERS_DATA_FILE = os.path.join(DATA_DIR, 'monsters_elements.json')
OUTPUT_HTML_FILE = os.path.join(BASE_DIR, 'index.html')

# Dictionnaire de correspondance pour les monstres collab
COLLAB_MAPPING = {
    # STREET_FIGHTER - DHALSIM
    "water dhalsim - water": "kyle - water",
    "fire dhalsim - fire": "todd - fire",
    "wind dhalsim - wind": "jarrett - wind",
    "light dhalsim - light": "hekerson - light",
    "dark dhalsim - dark": "cayde - dark",
    # STREET_FIGHTER - CHUN LI
    "water chun-li - water": "lariel - water",
    "fire chun-li - fire": "berenice - fire",
    "wind chun-li - wind": "cordelia - wind",
    "light chun-li - light": "leah - light",
    "dark chun-li - dark": "vereesa - dark",
    # STREET_FIGHTER - KEN
    "fire ken - fire": "bernadotte - fire",
    # STREET_FIGHTER - RYU
    "water ryu - water": "moore - water",
    "fire ryu - fire": "douglas - fire",
    "wind ryu - wind": "kashmir - wind",
    "light ryu - light": "talisman - light",
    "dark ryu - dark": "vancliffe - dark",
    # STREET_FIGHTER - MBISON
    "water m. bison - water": "borgnine - water",
    "fire m. bison - fire": "karnal - fire",
    "wind m. bison - wind": "sagar - wind",
    "light m. bison - light": "craig - light",
    "dark m. bison - dark": "gurkha - dark",
    # COOKIE_RUN_KINGDOM - ESPRESSO
    "water espresso cookie - water": "rosemary - water",
    "fire espresso cookie - fire": "hibiscus - fire",
    "wind espresso cookie - wind": "chamomile - wind",
    "light espresso cookie - light": "jasmine - light",
    "dark espresso cookie - dark": "lavender - dark",
    # COOKIE_RUN_KINGDOM - MADELEINE COOKIE
    "water madeleine cookie - water": "ganache - water",
    "fire madeleine cookie - fire": "pave - fire",
    "wind madeleine cookie - wind": "praline - wind",
    "light madeleine cookie - light": "fudge - light",
    "dark madeleine cookie - dark": "truffle - dark",
    # COOKIE_RUN_KINGDOM - GINGERBRAVE
    "wind gingerbrave - wind": "thomas - wind",
    # COOKIE_RUN_KINGDOM - PURE VANILLA COOKIE
    "water pure vanilla cookie - water": "adriana - water",
    "fire pure vanilla cookie - fire": "lucia - fire",
    "wind pure vanilla cookie - wind": "angela - wind",
    "light pure vanilla cookie - light": "ariana - light",
    "dark pure vanilla cookie - dark": "elena - dark",
    # COOKIE_RUN_KINGDOM - HOLLYBERRY COOKIE
    "water hollyberry cookie - water": "manon - water",
    "fire hollyberry cookie - fire": "alice - fire",
    "wind hollyberry cookie - wind": "jade - wind",
    "light hollyberry cookie - light": "audrey - light",
    "dark hollyberry cookie - dark": "giselle - dark",
    # ASSASSINS CREED - Altaïr
    "light altair - light": "frederic - light",
    # ASSASSINS CREED - EZIO
    "water ezio - water": "lionel - water",
    "fire ezio - fire": "patrick - fire",
    "wind ezio - wind": "hector - wind",
    "light ezio - light": "ian - light",
    "dark ezio - dark": "evan - dark",
    # ASSASSINS CREED - BAYEK
    "water bayek - water": "omar - water",
    "fire bayek - fire": "ashour - fire",
    "wind bayek - wind": "shahat - wind",
    "light bayek - light": "ahmed - light",
    "dark bayek - dark": "salah - dark",
    # ASSASSINS CREED - KASSANDRA
    "water kassandra - water": "kalantatze - water",
    "fire kassandra - fire": "federica - fire",
    "wind kassandra - wind": "eleni - wind",
    "light kassandra - light": "aurelia - light",
    "dark kassandra - dark": "kiara - dark",
    # ASSASSINS CREED - EIVOR
    "water eivor - water": "brita - water",
    "fire eivor - fire": "solveig - fire",
    "wind eivor - wind": "astrid - wind",
    "light eivor - light": "berghild - light",
    "dark eivor - dark": "sigrid - dark",
    # THE WITCHER 3 - GERALT
    "water geralt - water": "anders - water",
    "fire geralt - fire": "patrick - fire",
    "wind geralt - wind": "magnus - wind",
    "light geralt - light": "lars - light",
    "dark geralt - dark": "valdemar - dark",
    # THE WITCHER 3 - YENNEFER
    "water yennefer - water": "johanna - water",
    "fire yennefer - fire": "tarnisha - fire",
    "wind yennefer - wind": "hexarina - wind",
    "light yennefer - light": "arcana - light",
    "dark yennefer - dark": "hilda - dark",
    # THE WITCHER 3 - TRISS
    "water triss - water": "lumina - water",
    "fire triss - fire": "enshia - fire",
    "wind triss - wind": "nobella - wind",
    "light triss - light": "groa - light",
    "dark triss - dark": "celestara - dark",
    # THE WITCHER 3 - CIRI
    "water ciri - water": "rigna - water",
    "fire ciri - fire": "reyka - fire",
    "wind ciri - wind": "tirsa - wind",
    "light ciri - light": "birgitta - light",
    "dark ciri - dark": "fiona - dark",
    # JUJUTSU KAISEN - YUJI ITADORI
    "water yuji itadori - water": "exorcist association fighter - water",
    "fire yuji itadori - fire": "exorcist association fighter - fire",
    "wind yuji itadori - wind": "exorcist association fighter - wind",
    "light yuji itadori - light": "exorcist association fighter - light",
    "dark yuji itadori - dark": "exorcist association fighter - dark",
    # JUJUTSU KAISEN - MEGUMI fushiguro
    "water megumi fushiguro - water": "exorcist association conjurer - water",
    "fire megumi fushiguro - fire": "exorcist association conjurer - fire",
    "wind megumi fushiguro - wind": "exorcist association conjurer - wind",
    "light megumi fushiguro - light": "exorcist association conjurer - light",
    "dark megumi fushiguro - dark": "exorcist association conjurer - dark",
    # JUJUTSU KAISEN - NOBARA KUGISAKI
    "water nobara kugisaki - water": "exorcist association hunter - water",
    "fire nobara kugisaki - fire": "exorcist association hunter - fire",
    "wind nobara kugisaki - wind": "exorcist association hunter - wind",
    "light nobara kugisaki - light": "exorcist association hunter - light",
    "dark nobara kugisaki - dark": "exorcist association hunter - dark",
    # JUJUTSU KAISEN - SATORU GOJO
    "water satoru gojo - water": "exorcist association resolver - water",
    "fire satoru gojo - fire": "exorcist association resolver - fire",
    "wind satoru gojo - wind": "exorcist association resolver - wind",
    "light satoru gojo - light": "exorcist association resolver - light",
    "dark satoru gojo - dark": "exorcist association resolver - dark",
    # JUJUTSU KAISEN - DARK RYOMEN SUKUNA
    "dark ryomen sukuna - dark": "exorcist association arbitrer - dark",

    # Demon Slayer - Tanjiro Kamado
    "water tanjiro kamado - water": "azure dragon swordsman - water",
    "fire tanjiro kamado - fire": "azure dragon swordsman - fire",
    "wind tanjiro kamado - wind": "azure dragon swordsman - wind",
    "light tanjiro kamado - light": "azure dragon swordsman - light",
    "dark tanjiro kamado - dark": "azure dragon swordsman - dark",

    # Demon Slayer - Nezuko Kamado
    "water nezuko kamado - water": "vermilion bird dancer - water",
    "fire nezuko kamado - fire": "vermilion bird dancer - fire",
    "wind nezuko kamado - wind": "vermilion bird dancer - wind",
    "light nezuko kamado - light": "vermilion bird dancer - light",
    "dark nezuko kamado - dark": "vermilion bird dancer - dark",

    # Demon Slayer - Zenitsu Agatsuma
    "water zenitsu agatsuma - water": "qilin slasher - water",
    "fire zenitsu agatsuma - fire": "qilin slasher - fire",
    "wind zenitsu agatsuma - wind": "qilin slasher - wind",
    "light zenitsu agatsuma - light": "qilin slasher - light",
    "dark zenitsu agatsuma - dark": "qilin slasher - dark",

    # Demon Slayer - Inosuke Hashibira
    "water inosuke hashibira - water": "white tiger blade master - water",
    "fire inosuke hashibira - fire": "white tiger blade master - fire",
    "wind inosuke hashibira - wind": "white tiger blade master - wind",
    "light inosuke hashibira - light": "white tiger blade master - light",
    "dark inosuke hashibira - dark": "white tiger blade master - dark",

    # Demon Slayer - Gyomei himejima
    "wind gyomei himejima - wind": "black tortoise champion - wind",
}
