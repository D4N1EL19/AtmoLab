import pandas as pd
import os


def load_data_csv(source_path):
    if not os.path.exists(archivo_csv):
        print(f"Error: El archivo {archivo_csv} no existe.")
        exit(1)
    return pd.read_csv(source_path)

def preprocess_data(dataframe):
    # Function to preprocess the data
    pass

def train_model(dataframe):
    # Function to train a machine learning model
    pass



if __name__ == "__main__":
    # Construir una ruta absoluta compatible con Linux y Windows
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_csv = os.path.join(base_dir, "csv", "Ensenada_2000_2025_weather.csv")

    dataframe = load_data_csv(archivo_csv)
    print("Datos leídos correctamente de", archivo_csv)

    dataframe = preprocess_data(dataframe)

    model = train_model(dataframe)

