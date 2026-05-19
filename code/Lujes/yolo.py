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