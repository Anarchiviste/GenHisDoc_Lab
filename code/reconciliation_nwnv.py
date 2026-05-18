import json
import os
from pathlib import Path

dir_path = Path('newspaper navigator/')

# Créer le dossier labels s'il n'existe pas
os.makedirs(f'{dir_path}/labels', exist_ok=True)

with open(f'{dir_path}/trainval.json', 'r') as f:
    json_file = json.load(f)

# Construire un dict images indexé par image_id (et non par position dans la liste)
images_by_id = {img['id']: img for img in json_file['images']}

jpg_id = []

# format COCO : [x_top_left, y_top_left, width, height]
for annotation in json_file['annotations']:
    image_id  = annotation['image_id']
    label     = 0 # La seule de nos catégorie qui décrit les annotations de newspaper navigator est la 0 : Illustration
    bbox      = annotation['bbox'] 

    # Vérifier que l'image existe bien
    if image_id not in images_by_id:
        print(f'image_id {image_id} introuvable, on passe')
        continue

    image        = images_by_id[image_id]
    image_width  = image['width']
    image_height = image['height']

    # Conversion COCO vers YOLO
    x_tl, y_tl, w, h = bbox

    x_center = (x_tl + w / 2) / image_width  
    y_center = (y_tl + h / 2) / image_height   
    w_norm   = w / image_width                  
    h_norm   = h / image_height                 

    print(f'image_id={image_id} | label={label} | '
          f'x_c={x_center:.4f} y_c={y_center:.4f} w={w_norm:.4f} h={h_norm:.4f}')

    # Écriture dans le fichier label
    line = f"{label} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}"

    if image_id in jpg_id:
        with open(f'{dir_path}/labels/{image_id}.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{line}")
        print('already in jpg_id')
    else:
        with open(f'{dir_path}/labels/{image_id}.txt', 'w', encoding='utf-8') as f:
            f.write(line)
        jpg_id.append(image_id)
        print('new entry')

print(f'\n{len(jpg_id)} fichiers labels créés')