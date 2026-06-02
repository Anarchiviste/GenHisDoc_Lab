import os
from pathlib import Path

directories_dict = {
"aikon_dir" : Path("Aikon"),
"horae_dir" : Path("HoraeV2"),
"illu_dir" : Path("illuhisdoc"),
"sved_dir" : Path("S-VED"),
}

index = 0

for key, value in directories_dict.items():
    if key != "aikon_dir":
        print(f"{key} : {value}")
        img_dir = Path(f"{value}/images")
        labels_dir = Path(f"{value}/labels")
        if os.path.exists(img_dir):
            print("ok")

        else:
            print("fuuuuck")

    else: 
        manifests = set(i for i in os.listdir(value))
        print(len(manifests))
        for manifest in manifests:
            directory ={ 
                f"{manifest}" : f"{os.listdir(os.path.join(value, manifest))}"
                        }

        print(directory)
                
        
                          
        

    

        