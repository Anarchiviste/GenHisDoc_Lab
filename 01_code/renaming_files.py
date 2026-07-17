import os
import sys
from utilitaires.yolo import numeral_renamer                

path = sys.argv[1]
id = int(sys.argv[2])
numeral_renamer(path, id)