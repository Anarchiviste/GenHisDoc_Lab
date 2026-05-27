from pathlib import Path
import glob
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
import os


DATASET_DIR = Path("/home/lunes/Documents/GenHisDoc/HoraeV2/")

def reconciliation_Horae(directory: Path) -> None:
    
    label_mapping = {
        0: 0, # miniature => Illustration
        1: 1, # marginal medallion => Decoration
        2: 1, # marginal decoration => Decoration
        3: 2, # ornemented initial => Initial
        4: 2, # historiated initial => Initial
        5: None, # simple initial
        6: None, # transfert
        7: None, # text line
        8: None, # single page
        9: None, # rubrification
        10: None, # line filler
        11: None, # music notation
        12: 1, # ornament => decoration
        13: None, # text zone
    }
    input_dir  = directory / "labels"   # dossier contenant vos .txt originaux
    output_dir = directory / "label_output"  # dossier de sortie
    os.makedirs(output_dir, exist_ok=True)

    total_files   = 0
    total_kept    = 0
    total_deleted = 0

    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue

        total_files += 1
        input_path  = os.path.join(input_dir,  filename)
        output_path = os.path.join(output_dir, filename)

        with open(input_path, "r") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue

            original_label = int(parts[0])
            new_label = label_mapping.get(original_label)

            if new_label is None:       # annotation à supprimer
                total_deleted += 1
                continue

            parts[0] = str(new_label)   # on remplace uniquement le label
            new_lines.append(" ".join(parts))
            total_kept += 1

        # On écrit le fichier même s'il est vide (image sans annotation utile)
        with open(output_path, "w") as f:
            f.write("\n".join(new_lines))
            if new_lines:
                f.write("\n")

    print(f"Fichiers traités  : {total_files}")
    print(f"Annotations gardées  : {total_kept}")
    print(f"Annotations supprimées : {total_deleted}")
    print("Conversion terminée !")

reconciliation_Horae(DATASET_DIR)