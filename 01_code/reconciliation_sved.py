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

DATASET_DIR = Path("S-VED/")

df = pd.read_csv(DATASET_DIR / "SVED.csv")
column = df.iloc[:, 1]
counts = column.value_counts()
print(counts)

def recreation_yolo_txt(df: pd.DataFrame) -> None:
    index_des_images = []
    index_des_jpg = 0

    for index, row in df.iterrows():
        label_dict = {
            "Illustration": 0,
            "Decoration": 1,
            "Initial": 2,
            "Stamps": 3,
            "Table": 4,
            }
    
        image = row['image']
        label = row['label']
        x = row['x']
        y = row['y']
        width = row['width']
        height = row['height']
    
        path_to_image = DATASET_DIR / image    
    
        if str(image) in str(index_des_images):

            with open(f'{image}.txt', 'a', encoding='utf-8') as f:
                label = label.replace(label, str(label_dict[label]))
                f.writelines(f"\n{label} {x} {y} {width} {height}")
            
            index_des_jpg = index_des_jpg + 1

        else:
            index_des_images.append(image)

            with open(f'{image}.txt', 'w', encoding='utf-8') as f:
                label = label.replace(label, str(label_dict[label]))
                f.writelines(f"{label} {x} {y} {width} {height}")
                
            index_des_jpg = index_des_jpg + 1
        
    print(f"{index_des_jpg} fichiers textes ont été créés")
    
    

recreation_yolo_txt(df)