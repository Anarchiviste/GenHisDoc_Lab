# HORAE_LSv2: Layout Segmentation Dataset for Medieval Books of Hours (Version 2)

## Overview

HORAE_LSv2 is an updated and corrected version of the HORAE_LS dataset originally published in 2019. This carefully curated dataset contains **557 images** from **335 different manuscripts and printed books**, fully annotated for page layout analysis of medieval and early modern Books of Hours.

Originally created to train automatic segmentation models for medieval manuscript analysis, this dataset has been republished with downloaded images and updated annotations to ensure long-term accessibility and reproducibility, addressing the fragility of IIIF URL references.

## Quick Facts

- **Total images**: 555
- **Sources**: 334 manuscripts and printed books
- **Total annotations**: 22,964 (including text lines)
- **Annotation types**: 7 element types with optional sub-classifications
- **Format**: CSV with polygon coordinates + JPEG images
- **Original format**: XML PAGE (2019), migrated to CSV via Arkindex
- **Resolution**: Maximum available via IIIF (downloaded)

## Version History

### HORAE_LS (2019)
- **Publication**: GitHub, June 2019, https://github.com/oriflamms/HORAE/tree/master/Doc_Analysis/Layout_annotation/HORAE_LS
- **Format**: XML PAGE with IIIF URL references
- **Annotation tool**: Transkribus
- **Issue**: IIIF URLs became obsolete; images resized or inaccessible

### HORAE_LSv2 (2025)
- **Publication**: Zenodo with persistent DOI
- **Format**: CSV + downloaded JPEG images
- **Source**: Arkindex database (intermediate conservation)
- **Improvements**: 
  - Downloaded images at maximum IIIF resolution
  - Corrected annotations (missing elements, label corrections)
  - Updated coordinates for resized images
  - Complete traceability with IIIF URLs preserved in metadata

## Dataset Structure

```
HORAE_LSv2/
├── images/                           # 555 JPEG images (max IIIF resolution)
├── labels/                           # 545 YOLO format label files (.txt)
├── metadata/                         # CSV files and splits
│   ├── HORAE_LSv2_elements.csv       # Complete annotation listing
│   ├── HORAE_LSv2_image_data.csv     # Image metadata (URLs, dimensions)
│   ├── train.csv                     # Training set split
│   ├── val.csv                       # Validation set split
│   └── test.csv                      # Test set split
├── extras/                           # HTML visualizations via IIIF
└── README.md
```

## Annotation Types and Classes

### Element Types (type_arkindex)

| Type | Description | Count | Optional Classes |
|------|-------------|-------|------------------|
| **single_page** | Page zone on the image | 852 | calendar (52) |
| **text** | Text zone | 896 | border_text (57) |
| **text_line** | Text line with transcription | 13,879 | calendar (88) |
| **rubrication** | Rubrics (colored text headers) | 1,224 | blue (1), gold (1), red (190) |
| **miniature** | Autonomous narrative decoration | 159 | — |
| **initial** | Distinctive initial letters | 3,542 | simple_initial (600), decorated_initial (2,917), historiated_initial (25) |
| **decoration** | Painted zones (not initials/miniatures) | 2,412 | line_filler (1,260), ornament (2), music_notation (9), decorated_border (980), illustrated_border (161) |

**Total annotations**: 22,964

### Detailed Definitions

**single_page**: Zone representing a manuscript page on the digitized image. May be classified as *calendar* for calendar pages.

**text**: Text block zone. The *border_text* class indicates text in the margin or border area.

**text_line**: Individual text lines, often with transcription data. 

**rubrication**: Text headers or sections highlighted with colored ink (red, blue, gold), distinguishing sections or liturgical elements.

**miniature**: Autonomous narrative decoration in the text field (not marginal scenes).

**initial**: Letters at the beginning of text distinguished by size or color:
- *simple_initial*: Colored letters without background or decoration
- *decorated_initial*: Decorated with filigree, backgrounds, or non-figurative elements
- *historiated_initial*: Containing animated or figurative scenes

**decoration**: Painted elements that are neither initials nor miniatures:
- *line_filler*: Decorative elements filling line ends
- *ornament*: General decorative elements
- *music_notation*: Musical notation
- *decorated_border*: Non-animated decorative borders
- *illustrated_border*: Borders with figurative elements

## Data Format

### Metadata CSV (HORAE_LSv2_elements.csv)

Each annotation is represented by one row containing:

**Annotation information**:
- `element_id`: Unique identifier
- `type_arkindex`: Element type (see table above)
- `class_name`: Optional sub-classification
- `class_name_arkindex`: More precise classification (may be empty)
- `polygon`: Absolute coordinates as list of [x,y] pairs: `[[x1,y1], [x2,y2], ..., [xn,yn]]`

**Image information**:
- `page_name`: Systematic filename: `{country}_{city}_{institution}_{shelfmark}_{folio}.jpg`
- `url_image`: Original IIIF URL
- `width`, `height`: Image dimensions
- `image_id`, `name`: Arkindex database identifiers

**Example row**:
```csv
element_id,type_arkindex,class_name,polygon,page_name,url_image,width,height
abc123,initial,decorated_initial,"[[100,200],[150,200],[150,250],[100,250],[100,200]]",France_Paris_BnF_latin_10533_f009v.jpg,https://gallica.bnf.fr/iiif/...,3000,4000
```

### YOLO Format Labels

For compatibility with YOLO models, annotations are also provided in standard YOLO format:
```
class_id x_center y_center width height
```

All coordinates are normalized (0-1) relative to image dimensions.

### Image Metadata (HORAE_LSv2_image_data.csv)

Contains one row per image with:
- Filename and source identification
- Original IIIF URL and manifest reference
- Image dimensions (original and downloaded)
- Source institution and shelfmark

## Annotation Methodology

### Original Creation (2019)

1. **Annotation tool**: Transkribus interface
2. **Annotation type**: Rectangles (except text_lines: polygons)
3. **Text lines**: Automatically detected with CITlab tool, then manually corrected
4. **Annotators**: 3 annotators with systematic verification by a 4th person
5. **Quality control**: Correction of erroneous polygons and labels

See Boillet et al. (2019) for detailed inter-annotator agreement metrics.

### Updates for Version 2 (2025)

**Annotation corrections**:
- Addition of missing annotations
- Deletion of erroneous zones and images (duplicate, partial)
- Label type corrections (decoration, decorated_initial, ornamentation)
- Removal of incorrect classifications

**Coordinate updates**:
- 10 images: coordinates adjusted for IIIF image size changes
- IRHT images: capped at 8000px maximum dimension, requiring coordinate rescaling

**Format migration**:
- From XML PAGE to CSV format via Arkindex intermediate database
- Preservation of obsolete IIIF URLs in metadata for documentation
- Addition of downloaded JPEG images for stability

## Comparison with HORAE_Minit

HORAE_LSv2 represents an earlier annotation approach with broader scope but less refined ontology for decorative elements:

| Aspect | HORAE_LSv2 | HORAE_Minit |
|--------|------------|-------------|
| **Focus** | Complete layout segmentation | Decorative elements only |
| **Scale** | 555 images | 14,225 images |
| **Text** | Lines + transcription | Not annotated |
| **Initials** | 3 types combined | 3 types distinct |
| **Marginal** | decoration (generic) | medallion + decoration (distinct) |
| **Borders** | Multiple types | Not annotated |
| **Line fillers** | Annotated | Not annotated |

### Ontology Mapping

| HORAE_LSv2 | HORAE_Minit | SegmOnto |
|------------|-------------|----------|
| miniature | miniature | GraphicZone > illumination |
| initial > simple_initial | simple_initial | DropCapitalZone > plain* |
| initial > decorated_initial | ornamented_initial | ~~DropCapitalZone~~ > flourished/voided/etc.* |
| initial > historiated_initial | historiated_initial | ~~DropCapitalZone~~ > historiated* |
| decoration > decorated_border | — | GraphicZone > ornamentation |
| decoration > illustrated_border | marginal_medallion + marginal_decoration | GraphicZone > ornamentation |
| decoration > line_filler | — | GraphicZone > fillings |
| decoration > music_notation | — | MusicZone |

*Note: SegmOnto's DropCapitalZone specifically refers to multi-line initials, which doesn't match our broader definition.

### Integration with HORAE_Minit

A subset of 530 images from HORAE_LSv2 was adapted to the HORAE_Minit ontology and is included as **HORAE_Minit_E**. This subset:
- Uses HORAE_Minit class definitions
- Excludes text, rubrication, and line-level annotations
- Maintains miniature and initial annotations with updated classifications
- Provides bridge between the two annotation approaches

## Usage

### Loading Annotations

```python
import pandas as pd
from PIL import Image
import ast

# Load annotations
elements = pd.read_csv('metadata/HORAE_LSv2_elements.csv')

# Load image metadata
images = pd.read_csv('metadata/HORAE_LSv2_image_data.csv')

# Parse polygon coordinates (stored as string)
elements['polygon'] = elements['polygon'].apply(ast.literal_eval)

# Load an image
img = Image.open('images/France_Paris_Bibliothèque_nationale_de_France_nouv_acq_lat_3197_43r.jpg')

# Get all annotations for this image
page_elements = elements[elements['page_name'] == 'France_Paris_Bibliothèque_nationale_de_France_nouv_acq_lat_3197_43r.jpg']
```

### Visualizing Annotations

```python
from PIL import ImageDraw

def draw_polygon(image, polygon, outline='red', width=2):
    draw = ImageDraw.Draw(image)
    # Flatten polygon coordinates
    coords = [(x, y) for x, y in polygon]
    draw.polygon(coords, outline=outline, width=width)
    return image

# Draw all miniatures on an image
img = Image.open('images/France_Paris_BnF_latin_10533_f009v.jpg')
miniatures = page_elements[page_elements['type_arkindex'] == 'miniature']

for _, element in miniatures.iterrows():
    img = draw_polygon(img, element['polygon'], outline='blue', width=3)

img.show()
```

### Converting to YOLO Format

YOLO format labels are provided in the `labels/` directory. To use with Ultralytics:

```python
from ultralytics import YOLO

# Note: HORAE_LSv2 is best suited for layout analysis
# For decorative element detection, consider HORAE_Minit

# Example: training a model on page zones
model = YOLO('yolov8n.pt')
results = model.train(
    data='horae_lsv2.yaml',  # You'll need to create this config
    epochs=100,
    imgsz=640
)
```

## Data Sources

Images originate from IIIF-compliant digital libraries. Top contributors:

| Institution | Images |
|------------|--------|
| Bibliothèque nationale de France (Gallica) | ~200 |
| Various French municipal libraries (via BVMM/Arca) | ~250 |
| International institutions (Walters, Cambridge, etc.) | ~100 |

All images include original IIIF URLs in metadata for reference and context.

## Known Issues and Limitations

### Technical Issues

1. **IIIF instability**: Original URLs from 2019 became obsolete, motivating this republication
2. **Image resizing**: Some institutions changed served image dimensions, requiring coordinate updates
3. **IRHT capping**: Images from IRHT now capped at 8000px max dimension
4. **Format migration**: Move from XML PAGE to CSV may have introduced minor inconsistencies

### Annotation Limitations

1. **Heterogeneous application**: Ontology evolved during annotation; not all elements uniformly annotated
2. **Text lines**: Automated detection with manual correction; may contain errors
3. **Polygon precision**: Variable tightness around elements
4. **Line fillers vs. ornaments**: Distinction not always clear
5. **Calendar classification**: Inconsistently applied across elements

### Use Case Suitability

**Well-suited for**:
- Layout analysis and page segmentation
- Text zone detection
- Basic initial detection

**Less suited for**:
- Fine-grained decorative element classification → Use HORAE_Minit instead
- Large-scale decorative analysis → Use HORAE_Minit instead
- Marginal decoration study → Use HORAE_Minit instead

## Citation

```bibtex
@dataset{stutzmann2025horae_lsv2,
  author       = {Stutzmann, Dominique and Bernard-Leterme, Lise and 
                  Boillet, Mélodie and Bonhomme, Marie-Laurence and 
                  Kermorvant, Christopher},
  title        = {{HORAE\_LSv2: Layout Segmentation Dataset for 
                   Medieval Books of Hours (Version 2)}},
  year         = 2025,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.16919911},
  url          = {https://doi.org/10.5281/zenodo.16919911}
}
```

Please also cite the original HORAE_LS publication:

```bibtex
@inproceedings{boillet2019horae,
  title        = {{HORAE: an annotated dataset of books of hours}},
  author       = {Boillet, Mélodie and Bonhomme, Marie-Laurence and 
                  Stutzmann, Dominique and Kermorvant, Christopher},
  booktitle    = {Proceedings of the 5th International Workshop on 
                  Historical Document Imaging and Processing},
  pages        = {7--12},
  year         = 2019,
  organization = {ACM},
  doi          = {10.1145/3352631.3352633}
}
```

## Related Resources

- **HORAE_Minit Dataset** (successor with refined ontology): https://doi.org/10.5281/zenodo.17279364
- **HORAE Detection Models**: https://doi.org/10.5281/zenodo.17279775
- **Original HORAE_LS** (2019, GitHub): https://github.com/oriflamms/HORAE/tree/master/Doc_Analysis/Layout_annotation/HORAE_LS
- **Arkindex Platform**: https://teklia.com/our-solutions/arkindex/
- **Transkribus**: https://readcoop.eu/transkribus/

## License

**Annotations**: Creative Commons Attribution 4.0 International (CC BY 4.0)

**Images**: Individual images retain their original institutional licenses. Most derive from public domain manuscripts, but users should verify specific image rights via provided IIIF URLs.

## Acknowledgments

### Original HORAE_LS Creation (2019)

- **Marie-Laurence Bonhomme**: Annotation coordination and quality control
- **Mélodie Boillet**: Annotation and technical implementation
- **Christopher Kermorvant**: Technical supervision
- **Teklia**: Arkindex platform development
- **3 annotators + 1 validator**: Manual annotation work

### HORAE_LSv2 Update (2025)

- **Lise Bernard-Leterme**: Version 2 preparation, corrections, documentation
- **Dominique Stutzmann**: Project direction and supervision, data correction, documentation

### Funding

- **Biblissima+** (ANR-21-ESRE-0005)
- **Institut de Recherche et d'Histoire des Textes** (CNRS)
- Original HORAE project funding (2019)

## Contact

For questions about HORAE_LSv2:

**Dominique Stutzmann**

Institut de Recherche et d'Histoire des Textes, CNRS

Email: firstname.lastname@irht.cnrs.fr

For questions about the original HORAE_LS (2019):

See original publication: Boillet et al. (2019)

## Technical Notes

### File Naming Convention

Images and labels follow the pattern:
```
{country}_{city}_{institution}_{shelfmark}_{folio}.jpg
```

Where `folio` refers to the actual numbering of the folio or the sequential position in the IIIF manifest.

Examples: `Belgique_Tournai_Bibliothèque_du_Séminaire_016_f_074v-075.jpg` or `États-Unis_Cambridge_Houghton_Library_Lat_251_seq_90.jpg`

### Polygon Format

Polygons are stored as strings representing lists of coordinate pairs:
```python
"[[x1, y1], [x2, y2], [x3, y3], ..., [xn, yn]]"
```

Polygons are closed: first and last coordinates are identical (x₁=xₙ, y₁=yₙ).

### Image Resolution

Images were downloaded at maximum IIIF resolution available in 2025. Original dimensions are preserved in metadata. Some images may differ from 2019 versions due to institutional policy changes.

## Changelog

### Version 2.0 (2025)
- Downloaded all images as JPEG files
- Migrated from XML PAGE to CSV format
- Corrected annotation errors (missing/wrong labels)
- Updated coordinates for resized images (10 images)
- Added comprehensive metadata with IIIF traceability
- Reorganized file structure for easier use
- Generated YOLO-compatible labels
- Created HTML visualizations

### Version 1.0 (2019)
- Original release on GitHub
- XML PAGE format with IIIF URL references
- 557 images, 22,964 annotations
- Transkribus annotation interface

## Future Work

This dataset is maintained primarily for:
1. **Reproducibility**: Enabling replication of 2019 experiments
2. **Comparison**: Baseline for evaluating HORAE_Minit improvements
3. **Layout analysis**: Text zone and page structure detection

For new projects focused on decorative elements, we recommend using **HORAE_Minit** instead, which offers:
- Larger scale (14,225 images vs. 557)
- Refined ontology for decorative elements
- Better class balance for minority elements
- More systematic annotation protocol
- State-of-the-art model performance

## Version Information

**Current version**: 2.0  
**Release date**: 2025  
**Original version**: 1.0 (June 2019)  
**Status**: Stable - maintained for reproducibility