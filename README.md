# FIFA 21 – player position prediction

This project cleans FIFA 21 player data and trains a model that predicts a player's position group from their skills: goalkeeper, defender, midfielder or attacker.

## Files

| File | What it is |
|---|---|
| `dati/data.csv` | The original dataset, not modified |
| `dati/AVOTS.txt` | Data source, download date and license |
| `01_tirisana.py` | Cleans the data and saves `tirs.csv` |
| `tirs.csv` | The cleaned data |
| `02_modelis.py` | Trains the model and prints the accuracy, the baseline and the most important columns |
| `rezultati.md` | Explanation of the results |

## Requirements

- Python 3.12 or newer (https://www.python.org/downloads/)
- The `pandas` and `scikit-learn` libraries

Setup step by step (in a terminal, in the project root folder):

```
python -m venv env
env\Scripts\activate
pip install pandas scikit-learn
```

After activation, the terminal line should start with `(env)`.

## How to run

```
python 01_tirisana.py
python 02_modelis.py
```

Run the scripts in this order, because `02_modelis.py` uses the `tirs.csv` file created by `01_tirisana.py`.
