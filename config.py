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
MONSTERS_DATA_FILE = os.path.join(DATA_DIR, 'monsters.json')
OUTPUT_HTML_FILE = os.path.join(BASE_DIR, 'index.html')

# Dictionnaire de correspondance pour les monstres collab
COLLAB_MAPPING = {
    # STREET_FIGHTER - DHALSIM
    "water dhalsim": "kyle",
    "fire dhalsim": "todd",
    "wind dhalsim": "jarrett",
    "light dhalsim": "hekerson",
    "dark dhalsim": "cayde",
    # STREET_FIGHTER - CHUN LI
    "water chun-li": "lariel",
    "fire chun-li": "berenice",
    "wind chun-li": "cordelia",
    "light chun-li": "leah",
    "dark chun-li": "vereesa",
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
