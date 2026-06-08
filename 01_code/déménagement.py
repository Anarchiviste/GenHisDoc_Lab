import os
import shutil
from pathlib import Path
import pandas as pd

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

df = pd.DataFrame(columns=['Images origine', 'Images renommées'])


def process_pair(img_path: Path, label_dir: Path, index: int, df: pd.DataFrame):
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

    new_row = pd.DataFrame([{
        'Images origine':   str(img_path),
        'Images renommées': str(dest_img)
    }])
    df = pd.concat([df, new_row], ignore_index=True)

    return index + 1, df  # ✅ retourne les deux


def collect_flat(dataset_path: Path, index: int, df: pd.DataFrame):
    """Traite un dataset à structure plate (images/ et labels/ à la racine)."""
    img_dir   = dataset_path / "images"
    label_dir = dataset_path / "labels"

    if not img_dir.exists():
        print(f"  [SKIP] Pas de dossier images/ dans {dataset_path}")
        stats["skipped_dir"] += 1
        return index, df

    images = sorted(p for p in img_dir.iterdir() if p.suffix.lower() in IMG_EXT)
    print(f"  Structure plate → {len(images)} image(s)")

    for img_path in images:
        index, df = process_pair(img_path, label_dir, index, df)  # ✅ df passé et récupéré

    return index, df


def collect_subdirs(dataset_path: Path, index: int, df: pd.DataFrame):
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
            index, df = process_pair(img_path, label_dir, index, df)  # ✅ corrigé

    return index, df


index = 1

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
        index, df = collect_flat(dataset_path, index, df)      # ✅ tuple dépaqueté
    elif mode == "subdirs":
        index, df = collect_subdirs(dataset_path, index, df)   # ✅ tuple dépaqueté
    else:
        print(f"  [ERREUR] Mode inconnu : {mode}")

df.to_csv(output_dir / "renommage.csv", index=False)
print("CSV exporté → GenHisDoc/renommage.csv")

print(f"\n{'═' * 52}")

total = index - 1

print(f"Terminé — {total} image(s) traitée(s) au total")
print(f"Paires complètes (image + label)  : {stats['copied']}")
print(f"Annotations manquantes            : {stats['missing_label']}")
print(f"Dossiers ignorés                  : {stats['skipped_dir']}")
print(f"{'═' * 52}")