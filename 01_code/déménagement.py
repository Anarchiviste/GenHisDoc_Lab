import os
import shutil
from pathlib import Path

datasets = [
    {"key": "aikon_dir", "path": Path("Aikon"),      "mode": "subdirs"},
    {"key": "horae_dir", "path": Path("HoraeV2"),    "mode": "flat"},
    {"key": "illu_dir",  "path": Path("illuhisdoc"), "mode": "flat"},
    {"key": "sved_dir",  "path": Path("S-VED"),      "mode": "flat"},
]
 
output_dir        = Path("../GenHisDoc")
IMG_EXT           = {".jpg"}
output_images_dir = output_dir / "images"
output_labels_dir = output_dir / "labels"
 
output_images_dir.mkdir(parents=True, exist_ok=True)
output_labels_dir.mkdir(parents=True, exist_ok=True)
 
print(f"Dossier de sortie : {output_dir.resolve()}")
print(f"  ├── images/")
print(f"  └── labels/")
 
stats = {"copied": 0, "missing_label": 0, "skipped_dir": 0}
 
 
def process_pair(img_path: Path, label_dir: Path, index: int) -> int:
    """Copie une image et son annotation en les renommant avec `index`."""
    label_path = label_dir / (img_path.stem + ".txt")
    dest_img   = output_images_dir / f"{index}{img_path.suffix.lower()}"
    dest_label = output_labels_dir / f"{index}.txt"
 
    shutil.copy2(img_path, dest_img)
 
    if label_path.exists():
        shutil.copy2(label_path, dest_label)
        stats["copied"] += 1
    else:
        stats["missing_label"] += 1
        print(f"  [WARN] Annotation manquante : {img_path.name}")
 
    return index + 1  # retourne le prochain index disponible
 
 
def collect_flat(dataset_path: Path, index: int) -> int:
    """Traite un dataset à structure plate (images/ et labels/ à la racine)."""
    img_dir   = dataset_path / "images"
    label_dir = dataset_path / "labels"
 
    if not img_dir.exists():
        print(f"  [SKIP] Pas de dossier images/ dans {dataset_path}")
        stats["skipped_dir"] += 1
        return index
 
    images = sorted(p for p in img_dir.iterdir() if p.suffix.lower() in IMG_EXT)
    print(f"  Structure plate → {len(images)} image(s)")
 
    for img_path in images:
        index = process_pair(img_path, label_dir, index)  # màj de l'index
 
    return index
 
 
def collect_subdirs(dataset_path: Path, index: int) -> int:
    """Parcourt chaque sous-dossier qui contient images/ et labels/."""
    subdirs = sorted(
        p for p in dataset_path.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )
    print(f"  Structure sous-dossiers → {len(subdirs)} sous-dossier(s)")
 
    for subdir in subdirs:
        img_dir   = subdir / "images"
        label_dir = subdir / "labels"
 
        if not img_dir.exists():
            print(f"  [SKIP] {subdir.name} — pas de dossier images/")
            stats["skipped_dir"] += 1
            continue
 
        images = sorted(p for p in img_dir.iterdir() if p.suffix.lower() in IMG_EXT)
        print(f"    {subdir.name} : {len(images)} image(s)")
 
        for img_path in images:
            index = process_pair(img_path, label_dir, index)  # màj de l'index
 
    return index

index = 1    

"""Traite un dataset à structure plate (images/ et labels/ à la racine)."""
 
for ds in datasets:
    key          = ds["key"]
    dataset_path = ds["path"]
    mode         = ds["mode"]
 
    print(f"\n{'─' * 52}")
    print(f"[{key}]  {dataset_path}  (mode: {mode})")
 
    if not dataset_path.exists():
        print(f"  [SKIP] Dossier introuvable : {dataset_path.resolve()}")
        stats["skipped_dir"] += 1
        continue
 
    if mode == "flat":
        index = collect_flat(dataset_path, index)      # récupération de l'index
    elif mode == "subdirs":
        index = collect_subdirs(dataset_path, index)   # récupération de l'index
    else:
        print(f"  [ERREUR] Mode inconnu : {mode}")
 
print(f"\n{'═' * 52}")

total = index - 1

print(f"Terminé — {total} image(s) traitée(s) au total")
print(f"Paires complètes (image + label)  : {stats['copied']}")
print(f"Annotations manquantes            : {stats['missing_label']}")
print(f"Dossiers ignorés                  : {stats['skipped_dir']}")
print(f"{'═' * 52}")
 
