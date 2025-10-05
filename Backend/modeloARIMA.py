"""
Script para aplicar ARIMA a datos climáticos históricos.
Analiza múltiples variables: temperatura, humedad, viento, precipitación.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
warnings.filterwarnings('ignore')


def cargar_datos_clima(archivo_csv):
    """
    Carga y prepara los datos climáticos.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV
        
    Returns:
        pd.DataFrame: DataFrame procesado con fecha como índice
    """
    # Leer CSV
    df = pd.read_csv(archivo_csv)
    
    # Convertir fecha a datetime (ajustar formato según tus datos)
    df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%Y')
    
    # Establecer fecha como índice
    df = df.set_index('Fecha')
    
    # Ordenar por fecha
    df = df.sort_index()
    
    # Asegurar frecuencia diaria
    df = df.asfreq('D')
    
    # Interpolar valores faltantes si existen
    df = df.interpolate(method='linear')
    
    print(f"Datos cargados: {len(df)} registros")
    print(f"Período: {df.index[0].date()} a {df.index[-1].date()}")
    print(f"\nColumnas disponibles:")
    for col in df.columns:
        print(f"  - {col}")
    
    return df


def analizar_estacionariedad(serie, nombre_variable):
    """
    Analiza si una serie temporal es estacionaria.
    
    Args:
        serie (pd.Series): Serie temporal a analizar
        nombre_variable (str): Nombre de la variable
        
    Returns:
        bool: True si es estacionaria
    """
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE ESTACIONARIEDAD: {nombre_variable}")
    print(f"{'='*60}")
    
    result = adfuller(serie.dropna())
    
    print(f'Estadístico ADF: {result[0]:.6f}')
    print(f'p-value: {result[1]:.6f}')
    print(f'Valores críticos:')
    for key, value in result[4].items():
        print(f'  {key}: {value:.3f}')
    
    es_estacionaria = result[1] <= 0.05
    
    if es_estacionaria:
        print(f"\n✓ {nombre_variable} es ESTACIONARIA")
        print("  → Puedes usar d=0 en ARIMA")
    else:
        print(f"\n✗ {nombre_variable} NO es estacionaria")
        print("  → Usa d=1 o d=2 en ARIMA para diferenciar")
    
    return es_estacionaria


def graficar_serie_temporal(df, columnas=None, figsize=(15, 10)):
    """
    Grafica las series temporales de múltiples variables.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columnas (list): Lista de columnas a graficar (None = todas)
        figsize (tuple): Tamaño de la figura
    """
    if columnas is None:
        columnas = df.columns.tolist()
    
    n_cols = len(columnas)
    fig, axes = plt.subplots(n_cols, 1, figsize=figsize)
    
    if n_cols == 1:
        axes = [axes]
    
    for i, col in enumerate(columnas):
        axes[i].plot(df.index, df[col], linewidth=1)
        axes[i].set_title(f'{col} - Serie Temporal', fontsize=12, fontweight='bold')
        axes[i].set_ylabel(col)
        axes[i].grid(True, alpha=0.3)
        axes[i].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()


def entrenar_modelo_arima(df, columna, order=(1, 1, 1), 
                         seasonal_order=(1, 0, 1, 365),
                         entrenar_hasta=None):
    """
    Entrena un modelo ARIMA/SARIMA para una variable específica.
    
    Args:
        df (pd.DataFrame): DataFrame con los datos
        columna (str): Nombre de la columna a modelar
        order (tuple): Orden ARIMA (p, d, q)
        seasonal_order (tuple): Orden estacional (P, D, Q, s)
        entrenar_hasta (str): Fecha hasta donde entrenar (formato 'YYYY-MM-DD')
                             Si es None, usa todos los datos
        
    Returns:
        tuple: (modelo_entrenado, datos_entrenamiento, datos_prueba)
    """
    print(f"\n{'='*60}")
    print(f"ENTRENANDO MODELO ARIMA PARA: {columna}")
    print(f"{'='*60}")
    print(f"Orden ARIMA: {order}")
    print(f"Orden Estacional: {seasonal_order}")
    
    # Dividir datos si se especifica
    if entrenar_hasta:
        train = df[columna][:entrenar_hasta]
        test = df[columna][entrenar_hasta:]
        print(f"Entrenamiento: {len(train)} registros")
        print(f"Prueba: {len(test)} registros")
    else:
        train = df[columna]
        test = None
        print(f"Usando todos los datos: {len(train)} registros")
    
    # Entrenar modelo
    print("\nEntrenando modelo... (puede tardar unos minutos)")
    
    try:
        modelo = SARIMAX(
            train,
            order=order,
            seasonal_order=seasonal_order,
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        
        resultado = modelo.fit(disp=False, maxiter=200)
        
        print("\n✓ Modelo entrenado exitosamente")
        print(f"AIC: {resultado.aic:.2f}")
        print(f"BIC: {resultado.bic:.2f}")
        
        return resultado, train, test
        
    except Exception as e:
        print(f"\n✗ Error al entrenar el modelo: {e}")
        print("\nSugerencias:")
        print("  - Intenta con un orden más simple, ej: order=(1,1,1)")
        print("  - Reduce el período estacional o usa (0,0,0,0)")
        print("  - Verifica que no haya valores NaN en los datos")
        return None, train, test


def predecir_futuro(resultado, pasos=365, columna="Variable"):
    """
    Realiza predicciones futuras con el modelo entrenado.
    
    Args:
        resultado: Resultado del modelo SARIMAX
        pasos (int): Número de días a predecir
        columna (str): Nombre de la variable (para display)
        
    Returns:
        pd.DataFrame: DataFrame con predicciones e intervalos de confianza
    """
    print(f"\nRealizando predicciones para los próximos {pasos} días...")
    
    # Hacer predicción
    forecast = resultado.get_forecast(steps=pasos)
    pred_mean = forecast.predicted_mean
    pred_ci = forecast.conf_int(alpha=0.05)
    
    # Crear DataFrame con resultados
    predicciones = pd.DataFrame({
        'Prediccion': pred_mean,
        'Limite_Inferior': pred_ci.iloc[:, 0],
        'Limite_Superior': pred_ci.iloc[:, 1]
    })
    
    print(f"✓ Predicciones completadas")
    print(f"\nPrimeras 10 predicciones para {columna}:")
    print(predicciones.head(10).to_string())
    
    return predicciones


def graficar_predicciones(train, predicciones, columna, 
                         puntos_historicos=365, figsize=(15, 6)):
    """
    Grafica datos históricos y predicciones.
    
    Args:
        train (pd.Series): Datos de entrenamiento
        predicciones (pd.DataFrame): DataFrame con predicciones
        columna (str): Nombre de la variable
        puntos_historicos (int): Cantidad de puntos históricos a mostrar
        figsize (tuple): Tamaño de la figura
    """
    plt.figure(figsize=figsize)
    
    # Datos históricos (últimos N puntos)
    historical = train.iloc[-puntos_historicos:]
    plt.plot(historical.index, historical.values, 
            label='Datos Históricos', color='blue', linewidth=1.5)
    
    # Predicciones
    plt.plot(predicciones.index, predicciones['Prediccion'],
            label='Predicción', color='red', linewidth=2, linestyle='--')
    
    # Intervalos de confianza
    plt.fill_between(
        predicciones.index,
        predicciones['Limite_Inferior'],
        predicciones['Limite_Superior'],
        color='red', alpha=0.2, label='Intervalo de Confianza 95%'
    )
    
    plt.title(f'Predicción ARIMA - {columna}', fontsize=14, fontweight='bold')
    plt.xlabel('Fecha')
    plt.ylabel(columna)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def evaluar_modelo(resultado, test, columna):
    """
    Evalúa el modelo con datos de prueba.
    
    Args:
        resultado: Modelo entrenado
        test (pd.Series): Datos de prueba
        columna (str): Nombre de la variable
        
    Returns:
        dict: Métricas de evaluación
    """
    if test is None or len(test) == 0:
        print("No hay datos de prueba disponibles para evaluar")
        return None
    
    print(f"\n{'='*60}")
    print(f"EVALUACIÓN DEL MODELO: {columna}")
    print(f"{'='*60}")
    
    # Predecir sobre el período de prueba
    predictions = resultado.forecast(steps=len(test))
    
    # Calcular métricas
    mae = np.mean(np.abs(test - predictions))
    rmse = np.sqrt(np.mean((test - predictions)**2))
    mape = np.mean(np.abs((test - predictions) / test)) * 100
    
    print(f"MAE (Error Absoluto Medio): {mae:.4f}")
    print(f"RMSE (Raíz del Error Cuadrático Medio): {rmse:.4f}")
    print(f"MAPE (Error Porcentual Absoluto Medio): {mape:.2f}%")
    
    return {'mae': mae, 'rmse': rmse, 'mape': mape}


def analisis_completo_clima(archivo_csv, variable='Temperatura_Maxima_C', 
                           dias_prediccion=365, order=(1, 1, 1),
                           usar_estacionalidad=True):
    """
    Realiza un análisis completo ARIMA para datos climáticos.
    
    Args:
        archivo_csv (str): Ruta al archivo CSV
        variable (str): Variable a analizar
        dias_prediccion (int): Días a predecir hacia el futuro
        order (tuple): Orden ARIMA (p, d, q)
        usar_estacionalidad (bool): Si incluir componente estacional
        
    Returns:
        dict: Resultados del análisis
    """
    print("="*60)
    print("ANÁLISIS ARIMA PARA DATOS CLIMÁTICOS")
    print("="*60)
    
    # 1. Cargar datos
    df = cargar_datos_clima(archivo_csv)
    
    # 2. Verificar que la variable existe
    if variable not in df.columns:
        print(f"\n✗ Error: '{variable}' no encontrada en el dataset")
        print(f"Variables disponibles: {list(df.columns)}")
        return None
    
    # 3. Analizar estacionariedad
    analizar_estacionariedad(df[variable], variable)
    
    # 4. Graficar serie temporal
    print("\nGraficando serie temporal...")
    graficar_serie_temporal(df, [variable])
    
    # 5. Configurar componente estacional
    if usar_estacionalidad:
        # Para datos diarios con patrón anual
        seasonal_order = (1, 0, 1, 365)
        print("\nUsando componente estacional: período = 365 días")
    else:
        seasonal_order = (0, 0, 0, 0)
        print("\nSin componente estacional")
    
    # 6. Entrenar modelo
    resultado, train, test = entrenar_modelo_arima(
        df, variable, 
        order=order,
        seasonal_order=seasonal_order
    )
    
    if resultado is None:
        return None
    
    # 7. Hacer predicciones
    predicciones = predecir_futuro(resultado, dias_prediccion, variable)
    
    # 8. Graficar predicciones
    print("\nGraficando predicciones...")
    graficar_predicciones(train, predicciones, variable, puntos_historicos=730)
    
    # 9. Guardar predicciones
    archivo_salida = f'predicciones_{variable}.csv'
    predicciones.to_csv(archivo_salida)
    print(f"\n✓ Predicciones guardadas en: {archivo_salida}")
    
    return {
        'modelo': resultado,
        'predicciones': predicciones,
        'datos': df
    }


# EJEMPLO DE USO PRINCIPAL
if __name__ == "__main__":
    
    # Ruta a tu archivo CSV
    ARCHIVO_CSV = 'csv/Ensenada_2000_2025_weather.csv'  # ← CAMBIA ESTO por tu archivo
    
    # Opción 1: Análisis completo de temperatura máxima
    print("\n" + "="*60)
    print("ANÁLISIS 1: TEMPERATURA MÁXIMA")
    print("="*60)
    resultados_temp_max = analisis_completo_clima(
        ARCHIVO_CSV,
        variable='Temperatura_Maxima_C',
        dias_prediccion=365,
        order=(2, 1, 2),  # Ajusta según tus datos
        usar_estacionalidad=True
    )
    
    # Opción 2: Análisis de temperatura mínima
    print("\n" + "="*60)
    print("ANÁLISIS 2: TEMPERATURA MÍNIMA")
    print("="*60)
    resultados_temp_min = analisis_completo_clima(
        ARCHIVO_CSV,
        variable='Temperatura_Minima_C',
        dias_prediccion=365,
        order=(2, 1, 2),
        usar_estacionalidad=True
    )
    
    # Opción 3: Análisis de humedad (sin estacionalidad fuerte)
    print("\n" + "="*60)
    print("ANÁLISIS 3: HUMEDAD RELATIVA")
    print("="*60)
    resultados_humedad = analisis_completo_clima(
        ARCHIVO_CSV,
        variable='Humedad_Relativa_Promedio_%',
        dias_prediccion=365,
        order=(1, 1, 1),
        usar_estacionalidad=False  # Puede no tener patrón estacional claro
    )
    
    print("\n" + "="*60)
    print("ANÁLISIS COMPLETADO")
    print("="*60)
    print("\nArchivos generados:")
    print("  - predicciones_Temperatura_Maxima_C.csv")
    print("  - predicciones_Temperatura_Minima_C.csv")
    print("  - predicciones_Humedad_Relativa_Promedio_%.csv")