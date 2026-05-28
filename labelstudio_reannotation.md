# Importing Images annotated in yolo format in LabelStudio

Sources : 
[Tutorial: Importing Local YOLO Pre-Annotated Images to Label Studio](https://labelstud.io/blog/tutorial-importing-local-yolo-pre-annotated-images-to-label-studio/)

[HumanSignal/label-studio-converter on github](https://github.com/HumanSignal/label-studio-converter/tree/master#yolo-to-label-studio-converter)

# Step 1 : Installing LabelStudio with Python
Here is the file tree we will use to set-up Label Studio.
```
labelstudio
└── yolo
    └── datasets
        └── one
            ├── images
            └── labels
```

## 1.1 : The File Tree

In a empty directory, create a new python environnement and a datasets folder :
```bash
python -m venv labelstudioenv
source labelstudioenv/bin/activate
```
## 1.2 : Env Configuration

At the activation set the environnement variable with this commands :
```bash
export LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=/home/user/labelstudio/yolo/datasets
```

# Step 2 : Correctly formating your images and labels organisation

Here is the file tree with the files you need to import yolo style annotations. The directory need to be named  `images` and `labels`.

```
labelstudio
└── yolo
    └── datasets
        └── one
            ├── classes.txt
            ├── images
                └── 1.jpg
                └── 2.jpg
            └── labels
                └── 1.txt
                └── 2.txt

```

## 2.1 : The classes.txt file
A yolo annotation look like this so you need a classes.txt file that will tell Label Studio what label the annotation is. 
```
0 0.41 0.283681636282792 0.340666666666667 0.321920853712761
```

Here is what is inside my classes.txt file :
```
Illustration
Ornament
Initial
Stamp
Table
```

The order of the labels inside classes.txt is important, in the example above, Label Studio will interpret this annotation as an Illustration.
Images and Label need to have the exacte same name, images without a txt file will be considered unannotated in the labeling setup.

# Step 3 : Creating a Labeling Setup

Then launch Label Studio with this command : 
```bash
label-studio
```
## 3.1 : Creating a new project

In the webapp Label Studio, create a new project:
- enter a project name and a description
- skip the data import part
- choose your labeling setup (bouding boxes annotation) and enter your label names exactly as they are written in the classes.txt file
- Save and go in your new project

## 3.2 : Setting up local storage

In your new project, select `Connect Cloud Storage` > `Local Files`.
- Enter a Name for your local storage.
- Enter an absolute path to your root, in our case `/home/user/labelstudio/yolo/datasets/one` and verify the connection.
- Choose the `files` import method, review and press the `Save & Sync` button.

## 3.3 : Create a labeling interface for our datasets

In your new project select `Settings` > `Labeling Interface` > `Code` and copy paste the code below.

```xml
<View>
  <Image name="image" value="$image"/>
  <RectangleLabels name="label" toName="image">
    
    
  <Label value="Illustration" background="#FFA39E"/><Label value="Initial" background="#D4380D"/><Label value="Table" background="#FFC069"/><Label value="Stamp" background="#AD8B00"/><Label value="Ornament" background="#D3F261"/></RectangleLabels>
</View>
```

# Step 4 : Convertion between Yolo annotations and Label Studio JSON

Turn Off Label Studio but keep the virtual environnement activated, then enter :
```bash
label-studio-converter import yolo -i /home/user/labelstudio/yolo/datasets/one -o output.json --image-root-url "/data/local-files/?d=one/images"
```

Now a new file named output.json should have spawned in your file tree.
```
labelstudio
├── output.json
├── output.label_config.xml
└── yolo
    └── datasets
        └── one
            ├── classes.txt
            ├── images
                └── 1.jpg
                └── 2.jpg
            └── labels
                └── 1.txt
                └── 2.txt

```

You can open the json file in your browser to see if the annotations were correctly translated in the Label Studio format. To get your annotation to work you need to see if an "annotations" with x, y, width and height and a rectanglelabels are present.
```json
 {"data": {"image": "/data/local-files/?d=one/images/4283.jpg"}, "annotations": [{"result": [{"id": "306500c114", "type": "rectanglelabels", "value": {"x": 30.419921875, "y": 36.8326334733053, "width": 58.49609375, "height": 33.9532093581284, "rotation": 0, "rectanglelabels": ["Illustration"]}}]}]}
```

# Step 5 : Import of the images and their converted annotations

Relauch Label Studio, go to your project and select the `import` menue and the `Upload Files` button.

Select the output.json file. Normaly both files and annotations should be imported.

