import pandas as pd
import os

import numpy as np

#Funcion que carga informacion desde un archivo CSV especificado
def load_data_csv(source_path):
    if not os.path.exists(source_path):
        print(f"Error: El archivo {source_path} no existe.")
        exit(1)
    return pd.read_csv(source_path)

# Se utilizara el metodo Zscore para detectar y eliminar outliers
def preprocess_data(dataframe, columns, multiplier=2):
    """
    Elimina outliers usando el método IQR.
    multiplier: 1.5 es estándar, 3.0 es más conservador
    """
    df_clean = dataframe.copy()
    
    for col in columns:
        # Ignorar valores NaN
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        
        # Definir límites
        lower_bound = Q1 - multiplier * IQR
        upper_bound = Q3 + multiplier * IQR
        
        # Filtrar outliers (mantener NaN)
        mask = ((df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)) | df_clean[col].isna()
        df_clean = df_clean[mask]
    
    return df_clean
    

def train_model(dataframe):
    # Function to train a machine learning model
    pass



if __name__ == "__main__":
    # Construir una ruta absoluta compatible con Linux y Windows
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_csv = os.path.join(base_dir, "csv", "Ensenada_2000_2025_weather.csv")
    dataframe = load_data_csv(archivo_csv)

    print("Datos leídos correctamente de", archivo_csv)

    # Seleccionar las columnas relevantes para el preprocesamiento
    columnas = ["Temperatura_Maxima_C","Temperatura_Minima_C","Humedad_Relativa_Promedio_%","Velocidad_Viento_Promedio_kmh","Precipitacion_mm"]
    columnas_a_discriminar = ["Temperatura_Maxima_C","Temperatura_Minima_C","Humedad_Relativa_Promedio_%","Velocidad_Viento_Promedio_kmh",]

    dataframe = preprocess_data(dataframe, columnas_a_discriminar)
    print(dataframe.info)


    #model = train_model(dataframe)

