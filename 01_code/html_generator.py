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
from utilitaires.yolo import draw_yolo_annotations

output_dir = Path("generated_html")

dirlist= ["illustrations", "sved_bb_dir", "horae_bb_dir", "illushisdoc_bb_dir", "aikon_bb_dir"]

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
    1: "Ornament",
    2: "Initial",
    3: "Stamp",
    4: "Table",
    }

# GENERATING THE PIE ILLUSTRATIONS

illuhisdoc_dir = Path("illuhisdoc/all_labels")
horae_dir = Path("HoraeV2/label_output")
sved_dir = Path("S-VED/labels")
aikon_dir = Path("Aikon")

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

    global counts_illu
    counts_illu = Counter(total_labels)
    print(counts_illu)
    
    labels_illu = [labels_dict[k] for k in counts_illu.keys()]
    values_illu = list(counts_illu.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values_illu, labels=labels_illu, autopct="%1.1f%%")
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

    global counts_horae
    counts_horae = Counter(total_labels)
    print(counts_horae)

    labels_horae = [labels_dict[k] for k in counts_horae.keys()]
    values_horae = list(counts_horae.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values_horae, labels=labels_horae, autopct="%1.1f%%")
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

    global counts_sved
    counts_sved = Counter(total_labels)
    print(counts_sved)

    labels_sved = [labels_dict[k] for k in counts_sved.keys()]
    values_sved = list(counts_sved.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values_sved, labels=labels_sved, autopct="%1.1f%%")
    plt.title("sved Class distribution")
    plt.savefig("generated_html/illustrations/sved_class_distribution.png")

def aikon_visualisation(input_dir: Path, labels_dict: dict) -> None:
    total_files  = 0
    total_labels = []

    for subdir in Path(input_dir).iterdir():
        if not subdir.is_dir():
            continue
        labels_dir = subdir / "labels"
        if not labels_dir.exists():
            continue

        for filename in os.listdir(labels_dir):
            if not filename.endswith(".txt"):
                continue
            total_files += 1
            input_path = labels_dir / filename

            with open(input_path, "r") as f:
                lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if not parts:
                    continue
                label = int(parts[0])
                total_labels.append(label)

    global counts_aikon
    counts_aikon = Counter(total_labels)
    print(f"{total_files} fichiers traités")
    print(counts_aikon)

    labels_aikon = [labels_dict[k] for k in counts_aikon.keys()]
    values_aikon = list(counts_aikon.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values_aikon, labels=labels_aikon, autopct="%1.1f%%")
    plt.title("Aikon Class distribution")
    plt.savefig("generated_html/illustrations/aikon_class_distribution.png")

illuhisdoc_visualisation(illuhisdoc_dir, label_map)
horae_visualisation(horae_dir, label_map)
sved_visualisation(sved_dir, label_map)
aikon_visualisation(aikon_dir, label_map)

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
                background-color: white;
            }
            
            img {
                width : 70%;
                height: auto;
            }
            ''')

def generating_index_html(directory: Path) -> None:
    counts_total = counts_horae + counts_illu + counts_sved + counts_aikon

    labels_total = [label_map[k] for k in counts_total.keys()]
    values_total = list(counts_total.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values_total, labels=labels_total, autopct="%1.1f%%")
    plt.title("Total class distribution")
    plt.savefig("generated_html/illustrations/total_class_distribution.png")

    with open(f'{directory}/index.html', 'w') as f:
        f.write('''<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <link type="text/css" rel="stylesheet" href="style.css">
                </head>
                <body>
                    <header>
                        <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
                        <h2>generalistic historical datasets</h2>
                    </header>
                    <main>
                        <p>GenHisDoc is a generalistic datasets for historical documents layout recognition and detection. GenHisDoc use a combination of several previously published datasets which have been adapted and re-annotated to work together and our own annotated data.</p>
                        <article><a href="illuhisdoc.html">illuhisdoc</a></article>
                        <article><a href="horae.html">Horae LSv2</a></article>
                        <article><a href="sved.html">S-VED</a></article>
                        <article><a href="aikon.html">Aikon</a></article
                    </main>
                    <img src="illustrations/total_class_distribution.png">
                </body>
                <footer>
                    <a href="#top">Back to top</a>
                </footer>
           </html>
           ''')

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
        identifier = filename.replace(".txt", "")
        output_path = Path(f'generated_html/sved_bb_dir/{identifier}.jpg')
        
        image = draw_yolo_annotations(
                images_dir / f'{identifier}.jpg',
                labels_dir / f'{identifier}.txt',
                label_map,
                )
        
        if not output_path.is_file():
            image.save((output_path))
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        
        identifier_list.append(f'{identifier}')
    
    selection = random.sample(identifier_list, 50)

    total_value = sum(counts_sved.values())

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
                    <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
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
                        <li>Total : {total_value}</li>
                        <hr>
                        <li>Illustrations : {counts_sved[0]}</li>
                        <li>Initials: {counts_sved[2]}</li>
                        <li>Ornaments: {counts_sved[1]}</li>
                    </ul>
                </main>
                </body>
                <footer>
                    <a href="#top">Back to top</a>
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
                        <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
                    </header>
                    <body>
                ''')
        for i in selection:
            f.write(f'<p>image : {i}.jpg</p>\n')
            f.write(f'<img src="sved_bb_dir/{i}.jpg">\n')

        f.write('''</body>
                    <footer>
                        <a href="#top">Back to top</a>
                    </footer>
                </html>
                ''')

        print(f"images annotées crées : {annotations_crées}")
        print(f"annotations ignorées : {annotations_ignorées}")     

def generating_illuhisdoc_html(directory: Path) -> None:
    
    images_dir_msd = Path("illuhisdoc/msd/images")
    labels_dir_msd = Path("illuhisdoc/msd/labels")
    
    images_dir_msi = Path("illuhisdoc/msi/images")
    labels_dir_msi = Path("illuhisdoc/msi/labels")
    
    images_dir_mss = Path("illuhisdoc/mss/images")
    labels_dir_mss = Path("illuhisdoc/mss/labels")

    images_dir_p = Path("illuhisdoc/p/images")
    labels_dir_p = Path("illuhisdoc/p/labels")

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
        
        if not output_path.is_file():
            image.save((output_path))
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        
        identifier_list.append(f'{identifier}')

    print("génération des annotations pour illuhisdoc initial")

    for filename in tqdm(random.sample(os.listdir(labels_dir_msi), 25)):
        if not filename.endswith(".txt"):
            continue
        identifier = filename.replace(".txt", "")
        output_path = Path(f'generated_html/illushisdoc_bb_dir/{identifier}.jpg')
        
        image = draw_yolo_annotations(
                images_dir_msi / f'{identifier}.jpg',
                labels_dir_msi / f'{identifier}.txt',
                label_map,
                )
        
        if not output_path.is_file():
            image.save((output_path))
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        
        identifier_list.append(f'{identifier}')
 
    print("génération des annotations pour illuhisdoc science")

    for filename in tqdm(random.sample(os.listdir(labels_dir_mss), 25)):
        if not filename.endswith(".txt"):
            continue
        identifier = filename.replace(".txt", "")
        output_path = Path(f'generated_html/illushisdoc_bb_dir/{identifier}.jpg')
        
        image = draw_yolo_annotations(
                images_dir_mss / f'{identifier}.jpg',
                labels_dir_mss / f'{identifier}.txt',
                label_map,
                )
        
        if not output_path.is_file():
            image.save((output_path))
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        
        identifier_list.append(f'{identifier}')
        
    print("génération des annotations pour illuhisdoc printed")

    for filename in tqdm(random.sample(os.listdir(labels_dir_p), 25)):
        if not filename.endswith(".txt"):
            continue
        identifier = filename.replace(".txt", "")
        output_path = Path(f'generated_html/illushisdoc_bb_dir/{identifier}.jpg')
        
        image = draw_yolo_annotations(
                images_dir_p / f'{identifier}.jpg',
                labels_dir_p / f'{identifier}.txt',
                label_map,
                )
        
        if not output_path.is_file():
            image.save((output_path))
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        
        identifier_list.append(f'{identifier}')
    
    total_value = sum(counts_illu.values())
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
                    <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
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
                    <img src="illustrations/illushisdoc_class_distribution.png">
                    <ul>
                        <li>Total : {total_value}</li>
                        <hr>
                        <li>Illustrations : {counts_illu[0]}</li>
                        <li>Initials: {counts_illu[2]}</li>
                    </ul>
                </main>
                </body>
                <footer>
                    <a href="#top">Back to top</a>
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
                        <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
                    </header>
                    <body>
                ''')
        for i in selection:
            f.write(f'<p>image : {i}.jpg</p>\n')
            f.write(f'<img src="illushisdoc_bb_dir/{i}.jpg">\n')

        f.write('''</body>
                    <footer>
                        <a href="#top">Back to top</a>
                    </footer>
                </html>
                ''')

        print(f"images annotées crées : {annotations_crées}")
        print(f"annotations ignorées : {annotations_ignorées}")   
        
def generating_horae_html(directory: Path) -> None:
      
    images_dir_horae = Path("HoraeV2/images")
    labels_dir_horae = Path("HoraeV2/label_output")
    
    identifier_list = []
    annotations_crées = 0
    annotations_ignorées = 0
    
    print("génération des annotations pour Horae LSv2")
    
    for filename in tqdm(random.sample(os.listdir(labels_dir_horae), 100)):
        if not filename.endswith(".txt"):
            continue
        identifier = filename.replace(".txt", "")
        output_path = Path(f'generated_html/horae_bb_dir/{identifier}.jpg')
        
        image = draw_yolo_annotations(
                images_dir_horae / f'{identifier}.jpg',
                labels_dir_horae / f'{identifier}.txt',
                label_map,
                )
        
        if not output_path.is_file():
            image.save((output_path))
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        
        identifier_list.append(f'{identifier}')
    
    total_value = sum(counts_horae.values())
    selection = random.sample(identifier_list, 25)
        
    with open(f'{output_dir}/horae.html', 'w') as f:
        f.write(f'''<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <link type="text/css" rel="stylesheet" href="style.css">
                    <script src="visualisation.js" defer></script>
                </head>
                <body>
                <header>
                    <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
                    <h2>Horae LSv2</h2>
                    <p><a href="illu_image.html">visualisation des images</a></p>
                </header>
                <main>
                    <p>Published by Stutzmann Dominique 1, Bernard Leterme Lise 1, Boillet Mélodie 2, Bonhomme Marie-Laurence, Kermorvant Christopher 2.</p>
                    <ul>
                        <li>1 : Institut de recherche et d'histoire des textes du Centre national de la recherche scientifique, Paris - Aubervilliers, 14, cours des Humanités, 93322 Aubervilliers</li>
                        <li>2 : Teklia, 30 rue Raymond Losserand, 75014 Paris, France</li>
                    </ul>
                    <p>Datasets : <a href="https://zenodo.org/records/16919911">Horae LsV2</a></p>
                    <p>Modifications : Horae use a deep annotation system usefull only for manuscript, we reunited this classes into our segmentation ontology. We kept 4244 annotations about ornements, illustrations and initials, and suppressed 18720 annotations about text segmentation.</p>
                    <img src="illustrations/horae_class_distribution.png">
                    <ul>
                        <li>Total : {total_value}</li>
                        <hr>
                        <li>Initials: {counts_horae[2]}</li>
                        <li>Ornaments: {counts_horae[1]}</li>
                        <li>Illustrations : {counts_horae[0]}</li>
                    </ul>
                </main>
                </body>
                <footer>
                    <a href="#top">Back to top</a>
                </footer>    
            </html>
            ''')
        
    with open(f'{output_dir}/horae_image.html', 'w') as f:
        f.write('''<!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <link type="text/css" rel="stylesheet" href="style.css">
                        <script src="visualisation.js" defer></script>
                    </head>
                    <header>
                        <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
                    </header>
                    <body>
                ''')
        for i in selection:
            f.write(f'<p>image : {i}.jpg</p>\n')
            f.write(f'<img src="horae_bb_dir/{i}.jpg">\n')

        f.write('''</body>
                    <footer>
                        <a href="#top">Back to top</a>
                    </footer>
                </html>
                ''')

        print(f"images annotées crées : {annotations_crées}")
        print(f"annotations ignorées : {annotations_ignorées}")

def generating_aikon_html(directory: Path) -> None:
    aikon_dir = "Aikon"
    
    identifier_list = []
    annotations_crées = 0
    annotations_ignorées = 0
    
    print("génération des annotations pour Aikon")
    
    all_labels = []
    for subdir in Path(aikon_dir).iterdir():
        if subdir.is_dir():
            labels_dir = subdir / "labels"
            images_dir = subdir / "images"
            if labels_dir.exists() and images_dir.exists():
                for label_file in labels_dir.glob("*.txt"):
                    all_labels.append((label_file, images_dir / f"{label_file.stem}.jpg"))
    
    one_hundred_labels = random.sample(all_labels, 100)
    
    for label_path, image_path in tqdm(one_hundred_labels):
        identifier = label_path.stem
        output_path = Path(f'generated_html/aikon_bb_dir/{identifier}.jpg')
    
        image = draw_yolo_annotations(
            image_path,
            label_path,
            label_map,
        )
    
        if not output_path.is_file():
            image.save(output_path)
            annotations_crées += 1
        else:
            annotations_ignorées += 1
        identifier_list.append(identifier)
    
    selection = random.sample(identifier_list, 100)  

    with open(f'{output_dir}/aikon.html', 'w') as f:
        f.write(f'''<!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <link type="text/css" rel="stylesheet" href="style.css">
                    <script src="visualisation.js" defer></script>
                </head>
                <body>
                <header>
                    <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
                    <h2>Horae LSv2</h2>
                    <p><a href="aikon_image.html">visualisation des images</a></p>
                </header>
                <main>
                    <p>Paper : <a href="https://hal.science/hal-05248250/">AIKON : A Modular Computer Vision Platform for Historical Corpora</a></p>
                    <p>Published by  Ségolène Albouy (1) , Somkeo Norindr (2) , Paul Kervegan (1) , Fouad Aouinti (3) , Rémy Delanaux (4) , Robin Champenois (1) , Stavros Lazaris (3, 5) , Alexandre Guilbaud (6, 7) , Matthieu Husson (8, 2) , Mathieu Aubry (1) </p>
                    <ul>
                        <li>1 : IMAGINE [Marne-la-Vallée] (6 avenue Blaise Pascal - Cité Descartes - Champs-sur-Marne, 77455 Marne-la-Vallée cedex 2 - France) </li>
                        <li>2 : LTE - Laboratoire Temps Espace (61 avenue de l’Observatoire de Paris 75014 Paris - France)</li>
                        <li>3 : OM - ORIENT ET MÉDITERRANÉE : Textes, Archéologie, Histoire (Campus CNRS de Villejuif, 7 rue Guy Môquet, 94800 Villejuif - France)</li>
                        <li>4 : IMJ-PRG (UMR_7586) - Institut de Mathématiques de Jussieu - Paris Rive Gauche (Sorbonne Université - IMJ - Case 247 - 4 place Jussieu 75252 Paris cedex 05 / Université Paris Diderot - Bât. Sophie Germain, case 7012 - France)</li>
                        <li>5 : ICP - Institut Catholique de Paris (ICP) (21 Rue d'Assas, 75006 Paris - France)</li>
                        <li>6 : SU - Sorbonne Université (21 rue de l’École de médecine - 75006 Paris - France) </li>
                        <li>7 : IMJ-PRG (UMR_7586) - Institut de Mathématiques de Jussieu - Paris Rive Gauche (UPMC - 4 place Jussieu, Case 247 - 75252 Paris Cedex 5 UP7D - Campus des Grands Moulins - Bâtiment Sophie Germain, Case 7012- 75205 PARIS Cedex 13 - France)</li>
                        <li>8 : SYRTE - Systèmes de Référence Temps Espace (61 Av de l'Observatoire 75014 PARIS - France)</li>                        
                    </ul>
                    <p>Annotation Project : <a href="https://vhs.huma-num.fr/vhs-admin/">VHS</a></p>
                    <p>Annotation Project : <a href="https://eida.obspm.fr/eida-admin/login/?next=/eida-admin/">Eida</a></p>
                
                    <p>Modifications : Extraction and convertion from AIkon project website to yolo for reannotation and enrichement</p>

                    <img src="illustrations/aikon_class_distribution.png">

                    <article>
                        <p><a href="https://vhs.huma-num.fr/vhs-admin/">VHS</a></p>
                        <ul>
                            <li>Witness #2320 : Cyclopaedia, 5e éd., Vol. 2 - annotated by Alexandre</li>
                            <li>Witness #2365 : Latin 7416 | Paris, BnF - annotated by Alexandre</li>
                            <li>Witness #2377 : Cod. 44 | Österreichische Nationalbibliothek - annotated by Alexandre</li>
                            <li>Witness #2416 : Lat. Q. 9 | Universiteitsbibliotheek - annotated by Alexandre</li>
                            <li>Witness #2418 : Voss. Lat. Q. 40 | Universiteitsbibliotheek - annotated by Alexandre</li>
                            <li>Witness #2420 : 187 | Wien, Österreichische Nationalbibliothek - annotated by Alexandre</li>
                            <li>Witness #2421 : T. 47 | Biblioteca Ambrosiana - annotated by Alexandre</li>
                            <li>Witness #2387 : Latin 13955 | Paris, BnF - annotated by Alexandre </li>
                            <li>Witness #2423 : Dc 183 | Dresden, Sächsische Landesbibliothek - annotated by Alexandre </li>
                        </ul> 
                    </article>
                </main>
                </body>
                <footer>
                    <a href="#top">Back to top</a>
                </footer>    
            </html>
            ''')        

    with open(f'{output_dir}/aikon_image.html', 'w') as f:
        f.write('''<!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="UTF-8">
                        <link type="text/css" rel="stylesheet" href="style.css">
                        <script src="visualisation.js" defer></script>
                    </head>
                    <header>
                        <h1 id="top"><a href="index.html">GenHisDoc</a></h1>
                    </header>
                    <body>
                ''')
        for i in selection:
            f.write(f'<p>image : {i}.jpg</p>\n')
            f.write(f'<img src="aikon_bb_dir/{i}.jpg">\n')

        f.write('''</body>
                    <footer>
                        <a href="#top">Back to top</a>
                    </footer>
                </html>
                ''')

generating_index_html(output_dir)
generating_style_css(output_dir)
generating_sved_html(output_dir)
generating_illuhisdoc_html(output_dir)
generating_horae_html(output_dir)
generating_aikon_html(output_dir)
    