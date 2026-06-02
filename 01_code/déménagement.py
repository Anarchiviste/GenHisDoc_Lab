import os
from pathlib import Path

input_dir : Path(.)

for filename in os.listdir(input_dir):
    if filename.endswith(".jpg"):
        filename.cwd()
        