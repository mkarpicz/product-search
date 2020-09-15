# Fuzzy search of products

## Requirements

- Python 3.8
- CSV files with data

CSV files and their format where removed from the repository on purpose.

## SETTING UP THE PROJECT

1. Create virutalenv with Python 3.8
- `mkdir .venv`
- `cd .venv`
- `virtualenv -p python3.8 .`
- `cd ..`

2. Install packages
- `pip3 install -r requirements.txt`

## MODULES

The main module is `main.py`. The example usage is:

```
python3.8 main.py --search-phrase "Micro Greens Arrugala"
```

For more options check `python3.8 main.py --help`.


- `conig.py` contains the basic configuration for the products catalog.
- `data_preprocessor.py` is a simple data cleaning module that removes some artifacts from products names.
- `search_engine.py` should contain logic for searching for products in the products catalog.
- `adapters.py` contains a connector to the products catalog database and interface for querying it.