from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import cv2
import re
import numpy as np
import argparse
import matplotlib.gridspec as gridspec
from scipy.stats import gaussian_kde
from ultralytics.data.utils import visualize_image_annotations
from ultralytics.utils.plotting import Annotator, colors
import os
from collections import Counter
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import random

output_dir = Path("generated_html")

dirlist= ["illustrations", "sved_bb_dir", "horae_bb_dir", "illushisdoc_bb_dir"]

if Path(output_dir).is_dir():
    print(f'{output_dir} existe déjà')
    pass
else: 
    output_dir.mkdir()

for i in dirlist:
    subdir = Path(f'{output_dir}/{i}')
    if Path(subdir).is_dir():
        print(f'{subdir} existe déjà')
        pass
    else: 
        subdir.mkdir()
        print(f'{subdir} created')

label_map = {
    0: "Illustration",
    1: "Decoration",
    2: "Initial",
    3: "Stamps",
    4: "Table",
    }

# GENERATING THE PIE ILLUSTRATIONS

illuhisdoc_dir = Path("illuhisdoc/all_labels")
horae_dir = Path("HoraeV2/label_output")
sved_dir = Path("S-VED/labels")

def illuhisdoc_visualisation(input_dir: Path, labels_dict:dict) -> None:
    total_files   = 0

    total_labels = []

    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue
        
        total_files = total_files + 1
        input_path  = os.path.join(input_dir,  filename)

        with open(input_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            
            label = int(parts[0])

            total_labels.append(label)

    counts = Counter(total_labels)
    print(counts)

    labels = [labels_dict[k] for k in counts.keys()]
    values = list(counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("illuhisdoc Class distribution")
    plt.savefig("generated_html/illustrations/illushisdoc_class_distribution.png")

def horae_visualisation(input_dir:Path, labels_dict:dict) -> None:
    total_files   = 0

    total_labels = []

    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue
        
        total_files = total_files + 1
        input_path  = os.path.join(input_dir,  filename)

        with open(input_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            
            label = int(parts[0])

            total_labels.append(label)

    counts = Counter(total_labels)
    print(counts)

    labels = [labels_dict[k] for k in counts.keys()]
    values = list(counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Horae Class distribution")
    plt.savefig("generated_html/illustrations/horae_class_distribution.png")

def sved_visualisation(input_dir:Path, labels_dict:dict) -> None:
    total_files   = 0

    total_labels = []

    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue
        
        total_files = total_files + 1
        input_path  = os.path.join(input_dir,  filename)

        with open(input_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            
            label = int(parts[0])

            total_labels.append(label)

    counts = Counter(total_labels)
    print(counts)

    labels = [labels_dict[k] for k in counts.keys()]
    values = list(counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("sved Class distribution")
    plt.savefig("generated_html/illustrations/sved_class_distribution.png")

illuhisdoc_visualisation(illuhisdoc_dir, label_map)
horae_visualisation(horae_dir, label_map)
sved_visualisation(sved_dir, label_map)

# GENERATING HTML

def generating_style_css(directory: Path) -> None:
    with open(f'{directory}/style.css', 'w') as f:
        f.write('''body {
              font-family: courier;
              margin-left: 30%;
              margin-right: 30%;
              margin-bottom: 50%;
            }


            h1 {
              text-align: left;
              text-transform: uppercase;
              color: black;
            }

            h1 a{
                color: inherit;
                text-decoration: none;
            }

            h2{
                color: black;
            }

            h3 {
              color: black;
              font-size: 1.5em;
            }

            text {
              font-size: 16px;
              line-height: 1.5em;
            }

            a {
                color: cornflowerblue;
            }

            a:hover {
                color: red;
            }

            footer{
                position: fixed;
                left: 0;
                bottom: 0;    
                width: 100%;
                text-align: center;
            }
            
            img {
                width : 70%;
                height: auto;
            }
            ''')

def generating_index_html(directory: Path) -> None:
    with open(f'{directory}/index.html', 'w') as f:
        f.write('''<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <link type="text/css" rel="stylesheet" href="style.css">
                </head>
                <body>
                    <header>
                        <h1><a href="index.html">GenHisDoc</a></h1>
                        <h2>generalistic historical datasets</h2>
                    </header>
                    <main>
                        <p>GenHisDoc is a generalistic datasets for historical documents layout recognition and detection. GenHisDoc use a combination of several previously published datasets which have been adapted and re-annotated to work together and our own annotated data.</p>
                        <article><a href="illuhisdoc.html">illuhisdoc</a></article>
                        <article><a href="horae.html">Horae LSv2</a></article>
                        <article><a href="sved.html">S-VED</a></article>
                    </main>
                </body>
                <footer>
                    <a href="https://github.com/Anarchiviste">Jules Musquin</a>
                </footer>
           </html>
           ''')

def draw_yolo_annotations(image_path: Path, label_path: Path, label_map: dict) -> Image.Image | None:
   """Dessine les bounding boxes YOLO sur l'image et retourne une PIL Image."""
   if not image_path.exists():
       print(f"Image introuvable : {image_path}")
       return None
   if not label_path.exists():
       print(f"Label introuvable : {label_path}")
       return None
   img = np.array(Image.open(image_path).convert("RGB"))
   h, w = img.shape[:2]
   annotator = Annotator(img, line_width=2)
   with open(label_path, "r") as f:
       for line in f:
           parts = line.strip().split()
           if len(parts) < 5:
               continue
           cls_id = int(parts[0])
           cx, cy, bw, bh = map(float, parts[1:5])
           # Conversion YOLO (normalisé) → pixels (x1, y1, x2, y2)
           x1 = int((cx - bw / 2) * w)
           y1 = int((cy - bh / 2) * h)
           x2 = int((cx + bw / 2) * w)
           y2 = int((cy + bh / 2) * h)
           label = label_map.get(cls_id, str(cls_id))
           annotator.box_label([x1, y1, x2, y2], label=label, color=colors(cls_id, True))
   return Image.fromarray(annotator.result())

def generating_sved_html(directory: Path) -> None:
    
    images_dir = Path("S-VED/images")
    labels_dir = Path("S-VED/labels")
    identifier_list = []
    annotations_crées = 0
    annotations_ignorées = 0
    
    print("génération des annotations pour S-VED")

    for filename in tqdm(random.sample(os.listdir(labels_dir), 100)):
        if not filename.endswith(".txt"):
            continue
        identifier = filename.replace(".jpg.txt", "")
        output_path = Path(f'generated_html/sved_bb_dir/{identifier}.jpg')
        
        image = draw_yolo_annotations(
                images_dir / f'{identifier}.jpg',
                labels_dir / f'{identifier}.jpg.txt',
                label_map,
                )
        
        if image is not output_path.is_file():
            image.save((output_path))
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        
        identifier_list.append(f'{identifier}')
    
    selection = random.sample(identifier_list, 50)    
    with open(f'{output_dir}/sved.html', 'w') as f:
        f.write(f'''<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <link type="text/css" rel="stylesheet" href="style.css">
                    <script src="visualisation.js" defer></script>
                </head>
                <body>
                <header>
                    <h1><a href="index.html">GenHisDoc</a></h1>
                    <h2>S-VED (The sacrobosco datasets)</h2>
                    <p><a href="sved_image.html">visualisation des images</a></p>
                </header>
                <main>
                    <p>Paper : <a href="https://doi.org/10.3390/jimaging8100285">CorDeep and the Sacrobosco Dataset: Detection of Visual Elements in Historical Documents</a></p>
                    <p>Published by Jochen Büttner 1, Julius Martinetz 1,2, Hassan El-Hajj 1,2, Matteo Valleriani 1,2,3,4.</p>
                    <ul>
                        <li>1 : Max Planck Institute for the History of Science, Boltzmannstr. 22, 14195 Berlin, Germany</li>
                        <li>2 : BIFOLD—Berlin Institute for the Foundations of Learning and Data, 10587 Berlin, Germany</li>
                        <li>3 : Institute of History and Philosophy of Science, Technology, and Literature, Faculty I—Humanities and Educational Sciences, Technische Universität Berlin, Straße des 17. Juni 135, 10623 Berlin, Germany</li>
                        <li>4 : The Cohn Institute for the History and Philosophy of Science and Ideas, Faculty of Humanities, Tel Aviv University, P.O. Box 39040, Ramat Aviv, Tel Aviv 6139001, Israel</li>
                    </ul>
                    <p>Datasets : <a href="https://zenodo.org/record/7142456">Sacrobosco Dataset</a></p>
                    <p>Modifications : The printer's mark annotation classe has been transfered to the illustration annotation classe. The format of the annotation in csv as been transformed into yolo style format with a txt attached to the image.</p>
                    <img src="illustrations/sved_class_distribution.png">
                    <ul>
                        <li>Illustrations : 2095</li>
                        <li>Initials: 614</li>
                        <li>Decoration: 218</li>
                    </ul>
                </main>
                </body>
                <footer>
                    <a href="https://github.com/Anarchiviste">Jules Musquin</a>
                </footer>    
            </html>
            ''')
        
    with open(f'{output_dir}/sved_image.html', 'w') as f:
        f.write('''<!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <link type="text/css" rel="stylesheet" href="style.css">
                        <script src="visualisation.js" defer></script>
                    </head>
                    <header>
                        <h1><a href="index.html">GenHisDoc</a></h1>
                    </header>
                    <body>
                ''')
        for i in selection:
            f.write(f'<p>image : {i}.jpg</p>\n')
            f.write(f'<img src="sved_bb_dir/{i}.jpg">\n')

        f.write('''</body>
                    <footer>
                        <a href="https://github.com/Anarchiviste">Jules Musquin</a>
                    </footer>
                </html>
                ''')

        print(f"images annotées crées : {annotations_crées}")
        print(f"annotations ignorées : {annotations_ignorées}")     

def generating_illuhisdoc_html(directory: Path) -> None:
    
    images_dir_msd = Path("illuhisdoc/msd/images")
    labels_dir_msd = Path("illuhisdoc/msd/labels")
    identifier_list = []
    annotations_crées = 0
    annotations_ignorées = 0
    
    print("génération des annotations pour illuhisdoc drawing")

    for filename in tqdm(random.sample(os.listdir(labels_dir_msd), 25)):
        if not filename.endswith(".txt"):
            continue
        identifier = filename.replace(".txt", "")
        output_path = Path(f'generated_html/illushisdoc_bb_dir/{identifier}.jpg')
        
        image = draw_yolo_annotations(
                images_dir_msd / f'{identifier}.jpg',
                labels_dir_msd / f'{identifier}.txt',
                label_map,
                )
        
        if image is not output_path.is_file():
            image.save((output_path))
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        
        identifier_list.append(f'{identifier}')
    
    selection = random.sample(identifier_list, 25)    
    with open(f'{output_dir}/illuhisdoc.html', 'w') as f:
        f.write(f'''<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <link type="text/css" rel="stylesheet" href="style.css">
                    <script src="visualisation.js" defer></script>
                </head>
                <body>
                <header>
                    <h1><a href="index.html">GenHisDoc</a></h1>
                    <h2>illuhisdoc</h2>
                    <p><a href="illu_image.html">visualisation des images</a></p>
                </header>
                <main>
                    <p>Paper : <a href="https://arxiv.org/abs/2012.08191">docExtractor: An off-the-shelf historical document element extraction</a></p>
                    <p>Published by Tom Monnier 1 et Mathieu Aubry 1.</p>
                    <ul>
                        <li>1 : LIGM, École nationale des Ponts et chaussées, Université Gustave Eiffel, CNRS, Marne-la-vallée, France</li>
                    </ul>
                    <p>Datasets : <a href="https://www.dropbox.com/scl/fi/ql0yxqapyyl0adbzzgn1x/illuhisdoc.zip?rlkey=q7mqkd3ljzwrk3lelkm2rgico&e=1&dl=0">Dropbox link for illuhisdoc</a></p>
                    <p>Modifications : Illuhisdoc use a per pixel segmentation with 4 classes, we transformed this segmentation in yolo style format detection.</p>
                    <img src="illustrations/illuhisdoc_class_distribution.png">
                    <ul>
                        <li>Illustrations : 257</li>
                        <li>Initials: 54</li>
                    </ul>
                </main>
                </body>
                <footer>
                    <a href="https://github.com/Anarchiviste">Jules Musquin</a>
                </footer>    
            </html>
            ''')
        
    with open(f'{output_dir}/illu_image.html', 'w') as f:
        f.write('''<!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <link type="text/css" rel="stylesheet" href="style.css">
                        <script src="visualisation.js" defer></script>
                    </head>
                    <header>
                        <h1><a href="index.html">GenHisDoc</a></h1>
                    </header>
                    <body>
                ''')
        for i in selection:
            f.write(f'<p>image : {i}.jpg</p>\n')
            f.write(f'<img src="illushisdoc_bb_dir/{i}.jpg">\n')

        f.write('''</body>
                    <footer>
                        <a href="https://github.com/Anarchiviste">Jules Musquin</a>
                    </footer>
                </html>
                ''')

        print(f"images annotées crées : {annotations_crées}")
        print(f"annotations ignorées : {annotations_ignorées}")     

 
generating_index_html(output_dir)
generating_style_css(output_dir)
generating_sved_html(output_dir)
generating_illuhisdoc_html(output_dir)
    