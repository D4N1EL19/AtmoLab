import pandas as pd
import glob

ruta = ("data/dataset_chat/*.csv")

archivo_csv = glob.glob(ruta)

dataframe_list = [pd.read_csv(archivo) for archivo in archivo_csv]
final_df = pd.concat(dataframe_list, ignore_index=True)
final_df.to_csv("Ensenada_2000_2025_weather.csv", index=False)
print(final_df)

