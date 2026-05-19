import json
import os
from pathlib import Path
from Lujes.yolo import draw_yolo_annotations

path = Path('newspaper navigator')
i_index = []

with open(f'{path}/trainval.json','r') as f:
    trainval = json.load(f)
    images = trainval['images']
    annotations = trainval['annotations']
    
    
img_dict = {}
    
for i in images:
    img_dict[i['id']] = {
        "name": i['file_name'],
        "height": i['height'],
        "width": i['width']
    }
    
    
for a in annotations:
    img_id = a['image_id']
    img = img_dict[img_id]
    if img:
        a_id = a['id']
        x_1, x_2, y_1, y_2 = a['bbox']
        x_tl = x_1
        print(x_tl)
        
        y_tl = y_1
        print(y_tl)
        
        w = x_2 - x_1   
        h = y_2 - y_1
        
        x_center = (x_tl + w / 2) / img["width"]   
        y_center = (y_tl + h / 2) / img["height"]    
        w_norm = w / img["width"]                   
        h_norm = h / img["height"] 
        
        label = 0
        line = f'{label} {x_center} {y_center} {w_norm} {h_norm}'
        if img_id in i_index:
            with open(f'{path}/labels/{img_id}.txt', 'a', encoding='utf-8') as f:
                f.write(f"\n{line}")
            print('already in jpg_id')                         
        else:
            with open(f'{path}/labels/{img_id}.txt', 'w', encoding='utf-8') as f:
                f.write(line)
            i_index.append(img_id)
            print('new entry')
print(f'{len(i_index)} fichiers annotations créés')