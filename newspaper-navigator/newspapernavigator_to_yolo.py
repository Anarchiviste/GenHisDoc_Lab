"""
python newspapernavigator_to_yolo.py --labels beyond_words_data/trainval.json --output-dir yolo_dataset
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

CATEGORIES = {
    0: "Photograph",
    1: "Illustration",
    2: "Map",
    3: "Comics/Cartoon",
    4: "Editorial Cartoon",
    5: "Headline",
    6: "Advertisement",
}


def bbox_to_yolo(bbox, img_w, img_h):
    """
    COCO [x, y, w, h]
    YOLO [cx, cy, w, h]
    """
    x, y, w, h = bbox
    cx = (x + w / 2) / img_w
    cy = (y + h / 2) / img_h
    w_n = w / img_w
    h_n = h / img_h
    return cx, cy, w_n, h_n


def load_coco(json_path):
    with open(json_path) as f:
        data = json.load(f)
    ann_by_image = {}
    for ann in data["annotations"]:
        ann_by_image.setdefault(ann["image_id"], []).append(ann)
    return data["images"], ann_by_image


def write_anno(label_path, annotations, img_w, img_h):

    CATEGORY_REMAP = {
        0: 0,  # Photograph → Illustration
        1: 0,  # Illustration → Illustration
        2: 0,  # Map → Illustration
        3: 0,  # Comics/Cartoon → Illustration
        4: 0,  # Editorial Cartoon → Illustration
        5: None,  # Headline → drop
        6: 0,  # Advertisement → Illustration
    }
    lines = []
    for ann in annotations:
        new_id = CATEGORY_REMAP.get(ann["category_id"])
        if new_id is None:
            continue  # skip dropped categories

        cx, cy, w_n, h_n = bbox_to_yolo(ann["bbox"], img_w, img_h)
        cx, cy = max(0.0, min(1.0, cx)), max(0.0, min(1.0, cy))
        w_n, h_n = max(0.0, min(1.0, w_n)), max(0.0, min(1.0, h_n))
        lines.append(f"{new_id} {cx:.6f} {cy:.6f} {w_n:.6f} {h_n:.6f}")

    with open(label_path, "w") as f:
        f.write("\n".join(lines))


def convert_split(images, ann_by_image, images_dir, out_dir):
    img_out = out_dir / "images"
    lbl_out = out_dir / "labels"
    img_out.mkdir(parents=True, exist_ok=True)
    lbl_out.mkdir(parents=True, exist_ok=True)

    missing = 0
    converted = 0

    for img_info in images:
        src = images_dir / img_info["file_name"]
        if not src.exists():
            missing += 1
            continue

        stem = Path(img_info["file_name"]).stem
        shutil.copy2(src, img_out / img_info["file_name"])

        anns = ann_by_image.get(img_info["id"], [])
        write_anno(lbl_out / f"{stem}.txt", anns, img_info["width"], img_info["height"])
        converted += 1

    print(f"Converted {converted} images, skipped {missing} missing.")


def write_classes_txt(out_dir, categories):
    path = out_dir / "classes.txt"
    with open(path, "w") as f:
        for i in sorted(categories):
            f.write(categories[i] + "\n")
    print(f"Written: {path}")


def main():
    p = argparse.ArgumentParser(
        description="Convert Newspaper Navigator COCO annotations to YOLO format.",
    )
    p.add_argument("--labels", default="beyond_words_data/trainval.json")
    p.add_argument("--images-dir", default="beyond_words_data/images")
    p.add_argument("--output-dir", default="yolo_dataset")
    args = p.parse_args()

    labels_path = Path(args.labels)
    images_dir = Path(args.images_dir)
    out_dir = Path(args.output_dir)

    if not labels_path.exists():
        sys.exit(f"ERROR: annotation file not found: {labels_path}")
    if not images_dir.exists():
        sys.exit(f"ERROR: images directory not found: {images_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)
    images, ann_by_image = load_coco(labels_path)
    convert_split(images, ann_by_image, images_dir, out_dir)
    write_classes_txt(out_dir, CATEGORIES)


if __name__ == "__main__":
    main()
