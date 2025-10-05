import pandas as pd

def predict_weather(date_str, models_dict):

    try:
        # Convertir la fecha de entrada y extraer características
        future_date = pd.to_datetime(date_str, format='%d/%m/%Y')
        input_features = {
            'año': [future_date.year],
            'mes': [future_date.month],
            'dia_del_año': [future_date.dayofyear]
        }
        
        # Crear un DataFrame con el mismo formato que los datos de entrenamiento
        input_df = pd.DataFrame(input_features)
        
        # Iterar sobre cada modelo
        predictions = {}
        for variable, model in models_dict.items():
            prediction_value = model.predict(input_df)[0]
            print(prediction_value)
            predictions[variable] = prediction_value
            
        return predictions

    except ValueError:
        return f"Error: La fecha '{date_str}' no es válida o no tiene el formato 'dd/mm/YYYY'."