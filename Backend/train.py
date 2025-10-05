import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_absolute_error
import os
import joblib

#Funcion que carga informacion desde un archivo CSV especificado
def load_data_csv(source_path):
    if not os.path.exists(source_path):
        print(f"Error: El archivo {source_path} no existe.")
        exit(1)
    return pd.read_csv(source_path)

# Se utilizara el metodo Zscore para detectar y eliminar outliers
def preprocess_data(dataframe, columns, multiplier=2):
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
    

def train_model(dataframe, target_columns):
    print("\nInicio de entrenamiento")
    
    # Caracteristicas
    df = dataframe.copy()
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    df['año'] = df['Fecha'].dt.year
    df['mes'] = df['Fecha'].dt.month
    df['dia_del_año'] = df['Fecha'].dt.dayofyear
    
    # Definir X (características) e Y (objetivos)
    X = df[['año', 'mes', 'dia_del_año']]
    Y = df[target_columns]
    
    # Dividir los datos 80% 20%
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, shuffle=False)
    
    print(f"Datos de entrenamiento: {len(X_train)} registros")
    print(f"Datos de prueba: {len(X_test)} registros")
    
    # 
    models = {} # diccionario para guardar cada modelo entrenado
    print("\nEntrenando modelos individuales")

    for col in Y_train.columns:
        print(f"Entrenando modelo para: {col}...")
        
        # Selecciona la columna objetivo actual
        y_train_single = Y_train[col]
        y_test_single = Y_test[col]
        
        model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=10000,
            learning_rate=0.05,
            early_stopping_rounds=10
        )
    
        model.fit(
            X_train, 
            y_train_single,
            eval_set=[(X_test, y_test_single)],
            verbose=False
        )
        
        # Guarda el modeloo
        models[col] = model
    
    # Evaluación de los modelos
    print("\nEvaluación del Modelo (Error Absoluto Medio)")
    for col, model in models.items():
        prediction = model.predict(X_test)
        mae = mean_absolute_error(Y_test[col], prediction)
        print(f"  - {col}: {mae:.2f}")

    return models

if __name__ == "__main__":
    # Construir una ruta absoluta compatible con Linux y Windows
    base_dir = os.path.dirname(os.path.abspath(__file__))
    archivo_csv = os.path.join(base_dir, "data", "Ensenada_2000_2025_weather.csv")
    dataframe = load_data_csv(archivo_csv)

    print("Datos leídos correctamente de", archivo_csv)

    # Seleccionar las columnas relevantes para el preprocesamiento
    columnas = ["Temperatura_Maxima_C","Temperatura_Minima_C","Humedad_Relativa_Promedio_%","Velocidad_Viento_Promedio_kmh","Precipitacion_mm"]
    columnas_a_discriminar = ["Temperatura_Maxima_C","Temperatura_Minima_C","Humedad_Relativa_Promedio_%","Velocidad_Viento_Promedio_kmh",]

    weather_dataframe = preprocess_data(dataframe, columnas_a_discriminar)

    models = train_model(weather_dataframe, columnas)
    model_filname = ("weather_model.joblib")
    joblib.dump(models, model_filname)
    print("\n Modelo entrenado")

