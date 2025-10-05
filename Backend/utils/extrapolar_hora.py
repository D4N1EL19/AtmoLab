from datetime import datetime, date, timedelta, time
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import json
import math
import random

class HourlyData(BaseModel):
    hora: str
    temperatura_c: float
    humedad_relativa_pct: float
    velocidad_viento_kmh: float
    precipitacion_mm: float


def generar_datos_horarios(prediccion_diaria: dict) :
    """
    Genera datos horarios basados en la predicción diaria.
    La temperatura sigue un patrón sinusoidal con mínimo cerca de las 6am y máximo cerca de las 2pm.
    """
    datos_horarios = []
    
    # Parsear los datos si vienen como string JSON
    if isinstance(prediccion_diaria, str):
        prediccion_diaria = json.loads(prediccion_diaria)
    
    temp_max = prediccion_diaria.get("Temperatura_Maxima_C", 25)
    temp_min = prediccion_diaria.get("Temperatura_Minima_C", 15)
    humedad_prom = prediccion_diaria.get("Humedad_Relativa_Promedio_%", 50)
    viento_prom = prediccion_diaria.get("Velocidad_Viento_Promedio_kmh", 15)
    precipitacion_total = prediccion_diaria.get("Precipitacion_mm", 0)
    
    # Rango de temperaturas
    temp_rango = temp_max - temp_min
    temp_media = (temp_max + temp_min) 
    
    for hora in range(24):
        # Patrón sinusoidal para temperatura
        # Mínimo a las 6:00 (hora 6), Máximo a las 14:00 (hora 14)
        # Desplazamos la onda sinusoidal para que coincida con estos valores
        angulo = ((hora - 6) / 24) * 2 * math.pi
        factor_temp = math.sin(angulo)
        
        # Temperatura con variación aleatoria pequeña
        temperatura = temp_media + (temp_rango / 2) * factor_temp
        temperatura += random.uniform(-0.5, 0.5)  # Ruido aleatorio
        
        # Humedad (inversa a temperatura con variación)
        # Mayor humedad cuando temperatura es menor
        factor_humedad = -factor_temp * 0.3  # 30% de variación
        humedad = humedad_prom + (humedad_prom * factor_humedad)
        humedad += random.uniform(-3, 3)
        humedad = max(20, min(100, humedad))  # Limitar entre 20-100%
        
        # Velocidad del viento (tiende a ser mayor durante el día)
        factor_viento = (math.sin(((hora - 12) / 24) * 2 * math.pi) + 1) / 2
        viento = viento_prom * (0.7 + 0.6 * factor_viento)
        viento += random.uniform(-1, 1)
        viento = max(0, viento)
        
        # Precipitación (distribuida aleatoriamente, más probable en ciertas horas)
        # Mayor probabilidad en horas de tarde/noche
        if precipitacion_total > 0:
            # Distribuir la precipitación en algunas horas aleatorias
            if random.random() < 0.15:  # 15% probabilidad por hora
                precipitacion = precipitacion_total * random.uniform(0.1, 0.4)
            else:
                precipitacion = 0
        else:
            precipitacion = 0
        
        datos_horarios.append(HourlyData(
            hora=f"{hora:02d}:00",
            temperatura_c=round(temperatura, 2),
            humedad_relativa_pct=round(humedad, 2),
            velocidad_viento_kmh=round(viento, 2),
            precipitacion_mm=round(precipitacion, 2)
        ))
    
    return datos_horarios