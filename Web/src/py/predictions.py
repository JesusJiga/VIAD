import streamlit as st
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from pmdarima.arima import auto_arima

def load_csv(path):
    return pd.read_csv(path + 'data/causes_death_categorized.csv')

def __get_df_gender(dataframe, gender):
    if gender == 0:
        return (dataframe.drop(['Men', 'Women'], axis=1), "Both Genders")
    elif gender == 1:
        return (dataframe.drop(['Both Genders', 'Women'], axis=1), "Men") 
    elif gender == 2:
        return (dataframe.drop(['Both Genders', 'Men'], axis=1), "Women")
    else:
        print("sexo erroneo.")

def __get_df_age(dataframe, age):
    if age == 0:
        dataframe = dataframe.drop("Age", axis=1)  
        dataframe = dataframe.groupby(["Province", "Disease", "Year"]).sum().reset_index()
        return dataframe
    else:
        dataframe = dataframe.loc[dataframe['Age'] == age]
        dataframe = dataframe.drop("Age", axis=1) 
        return dataframe

def __get_df_province(dataframe, province):
    if province == 0:
        dataframe = dataframe.drop("Province", axis=1)  
        dataframe = dataframe.groupby(["Disease", "Year"]).sum().reset_index()
        return dataframe
    else:
        dataframe = dataframe.loc[dataframe['Province'] == province]
        dataframe = dataframe.drop("Province", axis=1) 
        return dataframe
    
def __get_df_disease(dataframe, disease):
    if disease == 0:
        dataframe = dataframe.drop("Disease", axis=1)  
        dataframe = dataframe.groupby(["Year"]).sum().reset_index()
        return dataframe
    else:
        dataframe = dataframe.loc[dataframe['Disease'] == disease]
        dataframe = dataframe.drop("Disease", axis=1) 
        return dataframe

def get_prediction(dataframe, gender, age, province, disease, year):
    dataframe, column = __get_df_gender(dataframe, gender)
    dataframe = __get_df_age(dataframe, age)
    dataframe = __get_df_province(dataframe, province)
    dataframe = __get_df_disease(dataframe, disease)

    dataframe = dataframe.set_index('Year')

    ts = pd.Series(dataframe[column], index=dataframe.index, dtype='int')

    # Ajustamos el modelo ARIMA utilizando la función auto_arima
    model = auto_arima(ts, start_p=1, start_q=1,
                    test='adf',       # Utilizamos el test de Dickey-Fuller aumentado
                    max_p=3, max_q=3, # Valores máximos de p y q
                    m=1,              # Frecuencia de la serie temporal (1 para anual)
                    d=None,           # d se estima automáticamente por la función
                    seasonal=False,   # No utilizamos componente estacional
                    trace=True)

    # Ajustar el modelo ARIMA
    model = ARIMA(ts, order=model.order)
    model_fit = model.fit()

    #Prediccion rango de fechas
    last_year = ts.index.max()
    period = year - int(pd.Timestamp(last_year).strftime('%Y'))

    index = pd.date_range(start=str(last_year), periods=period, freq='Y')

    prediction = model_fit.predict(start=index[0], end=index[-1])
    return int(prediction.round(0)[-1])