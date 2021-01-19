# Umudugudu map of Kigali

This code is used to build an interactive map of Villages/Umudugudus of Kigali. The map uses the shapefiles published by the [world bank data catalog](https://datacatalog.worldbank.org/dataset/rwanda-admin-boundaries-and-villages/resource/541db017-5a04-4f3d-a387-20a169553a50) 



## Reproducing the map

The code is written in Python. Install the dependencies from the requirements file with your favorite Python environment:

```bash
pip install -r requirements.txt
```

Download the shapefiles from [here](https://datacatalog.worldbank.org/dataset/rwanda-admin-boundaries-and-villages/resource/541db017-5a04-4f3d-a387-20a169553a50) and unzip it in the current folder. The resulting files should be located at a folder named `rwa_villages`.

Modify the file `create_map.py` as you wish and run it with Python:

```bash
python create_map.py
```

This will create an `index.html` file in the `Kigali_villages` folder.