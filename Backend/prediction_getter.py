#En esta carpeta se obtiene los datos de las predicciones de una fecha determinada
#Libreria para obtener estos datos
import os
import joblib
from modelo import predict_weather
import json
from extrapolar_hora import generar_datos_horarios

# Función para obtener la predicción del clima, recibiendo la fecha como parámetro, retorna  un diccionario con las predicciones o un mensaje de error
# ejm. 'Temperatura_Maxima_C': np.float32(21.097271), 'Temperatura_Minima_C': np.float32(11.260718), 'Humedad_Relativa_Promedio_%': np.float32(49.84692), 'Velocidad_Viento_Promedio_kmh': np.float32(15.010931), 'Precipitacion_mm': np.float32(0.5091563)}

def get_prediction(fecha_a_predecir):
    MODEL_FILENAME = "weather_model.joblib"

    # Comprobar si el modelo existe
    if not os.path.exists(MODEL_FILENAME):
        return json.dumps({
            "error": f"El archivo del modelo '{MODEL_FILENAME}' no fue encontrado. Por favor, ejecuta 'train.py' primero para entrenar y guardar el modelo."
        })

    # Cargar el modelo
    models = joblib.load(MODEL_FILENAME)

    # Obtener la predicción
    pronostico = predict_weather(fecha_a_predecir, models)

    # Convertir los valores np.float32 a float nativo de Python
    if isinstance(pronostico, dict):
        pronostico = {k: float(v) for k, v in pronostico.items()}
        
        # Convertir a JSON
        datos =  json.dumps(pronostico, ensure_ascii=False)

        # generar horas
        datos_horarios = generar_datos_horarios(pronostico)
        return datos_horarios

    else:
        return json.dumps({"error": pronostico}, ensure_ascii=False)



if __name__ == "__main__":
    # Definir la fecha
    fecha_a_predecir = "11/02/2026"
    pronostico = get_prediction(fecha_a_predecir)
    print(pronostico)

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
