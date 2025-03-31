import pandas as pd
from osgeo import osr

lat_col_name = "Lat/Y"
lon_col_name = "Long/X"
source_epsg = "4326"
target_epsg = "26918"


#for prod
input_file = input("file to convert: ")
# output_file = input("path to output file: ")
output_file = input_file[:-4] + "_reduced.csv"

# lat_col_name = input("lat column: ")
# lon_col_name = input("lon column name: ")
# source_epsg = "EPSG:" + input("source epsg: ")
# target_epsg = "EPSG:" + input("target epsg: ")


df = pd.read_csv(input_file)
print(df)

def ddm_to_dd(ddm):
    try:
        parts = ddm.strip().split()
        degrees = float(parts[0])
        minutes = float(parts[1][:-1])  # Remove the last character (N/S/E/W)
        direction = parts[1][-1]  # Get the N/S/E/W

        dd = degrees + (minutes / 60)
        if direction in ['S', 'W']:  # Negative for South/West
            dd *= -1
        return dd
    except Exception as e:
        print(f"Error converting '{ddm}': {e}")
        return None


def transform_coords(lon, lat, source_epsg="4326", target_epsg="26918"):
    source_srs = osr.SpatialReference()
    source_srs.ImportFromEPSG(int(source_epsg))

    target_srs = osr.SpatialReference()
    target_srs.ImportFromEPSG(int(target_epsg))

    transform = osr.CoordinateTransformation(source_srs, target_srs)

    utm_x, utm_y, _ = transform.TransformPoint(lon,lat)

    return utm_x, utm_y

# convert to decimal degrees
df["Lat_DD"] = df[lat_col_name].apply(ddm_to_dd)
df["Long_DD"] = df[lon_col_name].apply(ddm_to_dd)

df["easting_UTM"], df["northing_UTM"] = zip(*df.apply(lambda row: transform_coords(row["Long_DD"], row["Lat_DD"]), axis=1))

df["Header"] = df[df.columns[0]]
df["Time Fix ID"] = df[df.columns[2]]
df["Date mm/dd/yyy"] = df[df.columns[3]]
df["Time hhmmss.sss"] = df[df.columns[4]]
df["200kHz Depth"] = df[df.columns[6]]
df["200kHz Valid"] = df[df.columns[8]]
df["28khz Depth"] = df[df.columns[19]]
df["28kHz Valid"] = df[df.columns[21]]
df["Speed of Sound"] = df[df.columns[31]]
df["Lattitude NAD83"] = df[df.columns[33]]
df["Longitude NAD83"] = df[df.columns[34]]
df["GPS Latency"] = df[df.columns[35]]

df[["Header", "Time Fix ID", "Date mm/dd/yyy", "Time hhmmss.sss", "200kHz Depth", "200kHz Valid", "28khz Depth", "28kHz Valid", "Speed of Sound", "Lattitude NAD83", "Longitude NAD83", "GPS Latency","northing_UTM", "easting_UTM"]].to_csv(output_file, index=False)

print(f"Output saved to {output_file}")