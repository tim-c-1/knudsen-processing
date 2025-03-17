import pandas as pd
import glob
import os
from pathlib import Path

path = r'F:\Test\TestProject\KnudsenProcessing\RawKEA'
files = Path(path).glob('*.kea')

dfs = list()
for f in files:
    data = pd.read_csv(f)
    data['file'] = f.stem
    dfs.append(data)

df = pd.concat(dfs, ignore_index=True)
df.to_csv(path + r'\\' + 'all_kea_lines.csv', index=False)