import pandas as pd

lidarPath = input("enter lidar xyz file: ")
bathyPath = input("enter bathy xyz file: ")
outPath = input("enter save file path: ")
outFileName = input("enter output file name: ")
lidar = pd.read_csv(lidarPath)
bathy = pd.read_csv(bathyPath)

lidar["Depth"] = 239.96 - lidar["Elevation"] #subtract lidar elevation to MPL(NAVD88)
lidarDF = lidar[["Easting", "Northing", "Depth"]].copy() #create copy of dataframe without elevation
lidarDF["Depth"] = lidarDF["Depth"] * 0.3048 #convert feet to meters

dfs = [lidarDF, bathy] #add both datasets to list
df = pd.concat(dfs, ignore_index=True) #concatenate list
df.to_csv(outPath + '\\' + outFileName + '.csv', index=False) #export dataset as single csv