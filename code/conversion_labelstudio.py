from pathlib import Path
import os
import glob

dir = Path("/home/lunes/Documents/labelstudio/yolo/datasets/one/labels")

for entry in glob.iglob(f'{dir}/*.txt'):
        filename = entry.replace('.jpg', '')
        
        with open(entry, 'r') as f:
                lines = f.readlines()
                for line in lines:
                        with open(filename, 'a') as file:
                                file.write(line)
        
        os.remove(entry)

