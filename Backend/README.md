
# AtmoLab

Algoritmo de machine learning entrenado con datos de la NASA para
predecir el clima a mediano plazo

## Instación

Copiamos el repositorio

```git
  git clone https://github.com/D4N1EL19/AtmoLab.git
```

Una vez dentro ejecutamos

```Bash
cd Backend
pip install -r requirements.txt
```
Esto instalará todas las dependencias necearias



    
## Entrenamiento del codigo

dentro de 
```Bash
User/Atmolab/Backend
```
debemos entrenar el modelo antes de ejecutar el programa,
para ello ejecutaremos

```bash
python3 train.py
```
Se generará un archivo con el siguiente nombre

```
weather_model.joblib
```
Con esto ya estará listo el modelo





## API Reference

#### Predecir clima de una fecha especifica

```http
  GET /api/prediccion/{fecha}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `fecha` | `string` | **Requerido**. Fecha especifica a analizar |

#### Get item

```http
  GET /api/prediccion/predicciones/rango?fecha_inicio={fecha}&fecha_fin={fecha}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `dias consecutivos` | `string` | **Requerido**. dia inicial y final del rango |



