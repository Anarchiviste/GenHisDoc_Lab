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

DATASET_DIR = Path("illuhisdoc/msd/")

for entry in glob.iglob(f'{DATASET_DIR}/*.png'):
    print(entry)
    labeled_image = cv2.imread(entry)
    gray = cv2.cvtColor(labeled_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 75, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        x_center = (x + w / 2) / labeled_image.shape[1]
        y_center = (y + h / 2) / labeled_image.shape[0]
        width    = w / labeled_image.shape[1]
        height   = h / labeled_image.shape[0]
        print(f"{x_center} {y_center} {width} {height}")
        

        
        




