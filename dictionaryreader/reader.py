import csv
import numpy as np
from pathlib import Path

dict = {}
with open('.\dictionary.csv',encoding='utf-8-sig') as f:
    for row in csv.reader(f,skipinitialspace = True):
        dict[row[0]] = row[1]

store_path = str(Path.cwd()/"dict.npy")
print(store_path)
np.save(store_path, dict)

