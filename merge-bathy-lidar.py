import pandas as pd

lidar = pd.read_csv(r'M:\MGS\Coastal\BaltimoreCityReservoirs2020\Loch_Raven\LRground_full.txt')
bathy = pd.read_csv(r'M:\MGS\Coastal\BaltimoreCityReservoirs2020\Loch_Raven\LR_combined_bathy_xyz.csv')

lidar["Depth"] = 239.96 - lidar["Elevation"] #subtract lidar elevation to MPL(NAVD88)
lidarDF = lidar["Easting", "Northing", "Depth"].copy() #create copy of dataframe without elevation
lidarDF["Depth"] = lidarDF["Depth"] * 0.3048 #convert feet to meters

dfs = [lidarDF, bathy] #add both datasets to list
df = pd.concat(dfs, ignore_index=True) #concatenate list
df.to_csv(r'M:\MGS\Coastal\BaltimoreCityReservoirs2020\Loch_Raven\LR_full_xyz_w-lidar.csv', index=False) #export dataset as single csv