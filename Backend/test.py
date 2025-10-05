# test.py
import os
import joblib
from modelo import predict_weather

MODEL_FILENAME = "weather_model.joblib"

# Comprobar si el modelo existe
if not os.path.exists(MODEL_FILENAME):
    print(f"Error: El archivo del modelo '{MODEL_FILENAME}' no fue encontrado.")
    print("Por favor, ejecuta 'train.py' primero para entrenar y guardar el modelo.")
    exit()

print(f"Cargando modelo desde '{MODEL_FILENAME}'...")
models = joblib.load(MODEL_FILENAME)
print("Modelo cargado exitosamente.")

# Definir la fecha
fecha_a_predecir = "11/02/2026"
pronostico = predict_weather(fecha_a_predecir, models)

# Mostrar resultado
if isinstance(pronostico, dict):
    print(f"\nPronóstico del Clima para el {fecha_a_predecir}")
    for variable, valor in pronostico.items():
        unidad = ""
        if "Temperatura" in variable: unidad = "°C"
        elif "Humedad" in variable: unidad = "%"
        elif "Velocidad" in variable: unidad = "km/h"
        elif "Precipitacion" in variable: unidad = "mm"
        
        print(f"  - {variable.replace('_', ' '):<35}: {valor:.2f} {unidad}")
else:
    print(pronostico)