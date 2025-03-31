import pandas as pd

reduced_kea_file = r'F:\Test\TestProject\KnudsenProcessing\RawKEA\LochRaven_031125_line_002_reduced.csv'
file_out = reduced_kea_file[:-11]

df = pd.read_csv(reduced_kea_file)

# df["Out Of Range HF"] = (df["200kHz Depth"].shift() > 0.3) & (df["200kHz Depth"].shift(-1) > 0.3)
df["Out Of Range HF"] = (abs(df["200kHz Depth"] - df["200kHz Depth"].shift()) > 0.3) & (abs(df["200kHz Depth"] - df["200kHz Depth"].shift(-1)) > 0.3)

df["duplicate UTM"] = (df.duplicated(subset=["X_UTM"]) & df.duplicated(subset=["Y_UTM"]))

df.to_csv(file_out + "reformatted.csv",index=False)