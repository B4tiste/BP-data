import os
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

# Créer le contenu HTML
html_content = '<html>\n<head>\n<title>BP Gallery</title>\n</head>\n<body>\n'
html_content += '<h1>Balance Patch Note Gallery</h1>\n<ul>\n'
for image in sorted_images:
    html_content += f'<li><a href="{images_dir}/{image}">{image}</a></li>\n'
html_content += '</ul>\n</body>\n</html>'

# Écrire le contenu HTML dans le fichier de sortie
with open(output_file, 'w') as f:
    f.write(html_content)

print(f"Index file created: {output_file}")
