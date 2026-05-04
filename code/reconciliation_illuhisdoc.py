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

DATASET_DIR = Path("illuhisdoc/p/")


def recreation_yolo_txt(Dataset_dir: str):
    label = 0
    for entry in glob.iglob(f'{Dataset_dir}/*.png'):
        name_1 = entry.replace('illuhisdoc/p/', '')
        name_2 = name_1.replace('_seg.png', '')
        labeled_image = cv2.imread(entry)
        b, g, r = cv2.split(labeled_image)
        red_mask = (r > 150) & (g < 80) & (b < 80)
        thresh = red_mask.astype(np.uint8) * 255

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours is None:
            pass

        else:
            with open(f'{DATASET_DIR}/{name_2}.txt', 'w', encoding='utf-8') as f:
                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    x_center = (x + w / 2) / labeled_image.shape[1]
                    y_center = (y + h / 2) / labeled_image.shape[0]
                    width    = w / labeled_image.shape[1]
                    height   = h / labeled_image.shape[0]

                    f.write(f'{label} {x_center} {y_center} {width} {height}\n')


recreation_yolo_txt(DATASET_DIR)
        
        




