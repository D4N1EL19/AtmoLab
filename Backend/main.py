from fastapi import FastAPI, HTTPException
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from prediction_getter import get_prediction

# Aqui se encuentra todo respecto a la API del proyecto
# Para ejecutar: python3 -m uvicorn main:app --reload

app = FastAPI(
    title="API de Predicciones",
    description="API para obtener predicciones por fecha individual o rango de fechas",
    version="1.0.0"
)

# Modelos de respuesta
class PredictionResponse(BaseModel):
    fecha: date
    prediccion: Any
    
class RangePredictionResponse(BaseModel):
    fecha_inicio: date
    fecha_fin: date
    predicciones: List[PredictionResponse]
    total: int


@app.get("/")
def root():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "API de Predicciones",
        "endpoints": {
            "/prediccion/{fecha}": "Obtener predicción para una fecha específica (YYYY-MM-DD)",
            "/predicciones/rango": "Obtener predicciones para un rango de fechas"
        }
    }

# Endpoint para obtener predicción por fecha, ejm /prediccion/2025-10-15
# retorna 
@app.get("/prediccion/{fecha}", response_model=PredictionResponse)
def obtener_prediccion_fecha(fecha: date):
    """
    Obtiene la predicción para una fecha específica
    
    - **fecha**: Fecha en formato YYYY-MM-DD (ejemplo: 2025-10-15)
    """
    try:
        prediccion = get_prediction(fecha)
        return PredictionResponse(
            fecha=fecha,
            prediccion=prediccion
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener predicción: {str(e)}"
        )

# Endpoint para obtener predicciones en un rango de fechas, ejm /predicciones/rango?fecha_inicio=2025-10-01&fecha_fin=2025-10-07
# retorna
@app.get("/predicciones/rango", response_model=RangePredictionResponse)
def obtener_predicciones_rango(
    fecha_inicio: date,
    fecha_fin: date
):
    """
    Obtiene predicciones para un rango de fechas
    
    - **fecha_inicio**: Fecha inicial en formato YYYY-MM-DD
    - **fecha_fin**: Fecha final en formato YYYY-MM-DD
    """
    # Validar que fecha_inicio sea menor o igual a fecha_fin
    if fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio debe ser menor o igual a la fecha final"
        )
    
    # Validar que el rango no sea muy grande (opcional)
    dias_diferencia = (fecha_fin - fecha_inicio).days
    if dias_diferencia > 365:
        raise HTTPException(
            status_code=400,
            detail="El rango de fechas no puede ser mayor a 365 días"
        )
    
    try:
        predicciones = []
        fecha_actual = fecha_inicio
        
        # Iterar sobre cada día en el rango
        while fecha_actual <= fecha_fin:
            prediccion = get_prediction(fecha_actual)
            predicciones.append(
                PredictionResponse(
                    fecha=fecha_actual,
                    prediccion=prediccion
                )
            )
            fecha_actual += timedelta(days=1)
        
        return RangePredictionResponse(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            predicciones=predicciones,
            total=len(predicciones)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener predicciones: {str(e)}"
        )

