import pandas as pd
import os
import glob

ruta = ("data/meteostat/*.csv")

archivos_csv = glob.glob(ruta)
# se crea un dataframe para cada archivo encontrado
dataframe_list = [pd.read_csv(archivo, usecols=["date", "tavg", "tmin", "tmax", "prcp", "wspd", "pres"]) for archivo in archivos_csv]

final_dataframe = pd.concat(dataframe_list, ignore_index=False).fillna(0)
final_dataframe.to_csv("datos_meteorologicos.csv", index=False)
print(final_dataframe)


    