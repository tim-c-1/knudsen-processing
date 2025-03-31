# -*- coding: utf-8 -*-

import arcpy


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [keaReformat]


class keaReformat:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "keaReformat"
        self.description = "Reformats knudsen ascii files to prep for editing. Adds a column with new coordinates (defulats to NAD83 UTM Zone 18N)"

    def getParameterInfo(self):
        """Define the tool parameters."""
        param0 = arcpy.Parameter(
            displayName="input file", 
            name="input_file", 
            datatype="DEFile", 
            parameterType="Required", 
            direction="Input",
            )

        param1 = arcpy.Parameter(
            displayName="output file",
            name="out_file",
            datatype="String",
            parameterType="Required",
            direction="Input")
        
        param2 = arcpy.Parameter(
            displayName="input epsg",
            name="in_epsg",
            datatype="GPLong",
            parameterType="Required",
            direction="Input"
        )

        param3 = arcpy.Parameter(
            displayName="output epsg",
            name="out_epsg",
            datatype="GPLong",
            parameterType="Required",
            direction="Input"
        )
        
        param0.filter.list = ["kea"]
        # param1.filter.list = ["txt", "csv"]
        param2.values = 4326
        param3.values = 26918

        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        # when param0 is input, make param1 the same path- add _reduced.csv to end
        in_file = parameters[0].value
        out_file = parameters[1]

        in_file_path = parameters[0].valueAsText

        if in_file:
            out_file.value = in_file_path[:-4] + "_reduced.csv"

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        import pandas as pd
        from osgeo import osr

        input_file = parameters[0].valueAsText
        output_file = parameters[1].valueAsText
        source_epsg = parameters[2].valueAsText
        target_epsg = parameters[3].valueAsText

        lat_col_name = "Lat/Y"
        lon_col_name = "Long/X"
        # source_epsg = "4326"
        # target_epsg = "26918"


        #for prod
        # input_file = input("file to convert: ")
        # output_file = input_file[:-4] + "_reduced.csv"


        df = pd.read_csv(input_file)
        
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

        #clear missing content?
        # df = df.dropna(subset=["Lat_DD", "Long_DD"])

        df["X_UTM"], df["Y_UTM"] = zip(*df.apply(lambda row: transform_coords(row["Long_DD"], row["Lat_DD"],source_epsg, target_epsg), axis=1))

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


        df[["Header", "Time Fix ID", "Date mm/dd/yyy", "Time hhmmss.sss", "200kHz Depth", "200kHz Valid", "28khz Depth", "28kHz Valid", "Speed of Sound", "Lattitude NAD83", "Longitude NAD83", "GPS Latency","X_UTM", "Y_UTM"]].to_csv(output_file, index=False)

        print(f"Output saved to {output_file}")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return