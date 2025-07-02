import pandas as pd
from pathlib import Path

# merges edited excel files in bulk

path = r'M:\MGS\Coastal\BaltimoreCityReservoirs2020\Loch_Raven\03_13_25'
files = Path(path).glob('*HFedit.xlsx')

dfs = list()
for f in files:
    data = pd.read_excel(f)
    xyz = data[[data.columns[15], data.columns[14], data.columns[18]]].copy()
    # xyz['file'] = f.stem #adds original filename of each row to output as columns
    dfs.append(xyz)

df = pd.concat(dfs, ignore_index=True)
df.to_csv(path + r'\\' + 'LR_031325_xyz.csv', index=False)