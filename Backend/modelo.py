import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor


from train.py import weather_dataframe

def llamar_dataframe():
    data = weather_dataframe
    label = weather_dataframe.columns.tolist()
    dtrain = xgb.DMatrix(data, label=label)

    pass

def ing_caracteristicas(data):
    data['Fecha'] = pd.to_datetime(data['Fecha'])
    data['año'] = data['ano'].data.year
    data['mes'] = data['mes'].data.month
    data['dia'] = data[]
                                 
                                 

def llamar_modelo():
    pass

def entrenar():
    pass




if __name__ == "__main__":
    llamar_dataframe()
    
    generar_modelo()

    entrenar()