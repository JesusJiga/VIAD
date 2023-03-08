import streamlit as st
import pandas as pd
import joblib
import pymongo
#from pymongo import MongoClient
from urllib.parse import quote_plus
import dictionaries

client = pymongo.MongoClient(f"mongodb+srv://JiGa:{st.secrets['DB_PASSWORD']}@viad.b6yfn8g.mongodb.net/?retryWrites=true&w=majority")

database = "VIAD"
collection = "CausesDeath"

mongodb_viad = client[database][collection]

result = mongodb_viad.find()
# print results
j=0
for i in result:
    st.write(i)
    j+=1
    if j >=6:
        break

# Unpickle classifier
both_genders_model = joblib.load("/Models/both_genders_model.pkl")
men_model = joblib.load("/Models/men_model.pkl")
women_model = joblib.load("/Models/women_model.pkl")

st.title("¡Bienvenido a VIAD!")

st.markdown("Aquí podrás obtener una predicción sobre las muertes en España. Estas pueden ser en terminos generales o por causas especificas.", unsafe_allow_html=False)

st.markdown("Tenga en cuenta de que se trata de una elaboración propia con datos extraídos del sitio web del [INE](https://www.ine.es/) a fecha 23/02/203. Los resultados obtenidos son una mera orientación de lo que podría ser.", unsafe_allow_html=False)

st.markdown("Cabe destacar que dichas predicciones no tienen en cuenta posibles futuras catastrofes naturales, guerras o cualquier causa fuera de conductas normales.", unsafe_allow_html=False)

year = st.slider('Seleccione un año', min_value=2015, max_value=2050, value=2023, step=1, format="%d")

community = st.selectbox("Seleccione una comunidad", (dictionaries.communities))
province = st.selectbox("Seleccione una provincia", (dictionaries.provinces))
disease = st.selectbox("Seleccione una causa de muerte", (dictionaries.diseases))
age = st.selectbox("Seleccione una grupo de edad", (dictionaries.ages))

# Store inputs into dataframe
X = pd.DataFrame([
    [community, province, disease, age, year]],
    columns = ["Community", "Province", "Disease", "Age", "Year"])

if st.button('Comprobar'):

    # Get prediction
    prediction = both_genders_model.predict(X)[0]

    st.write(f"The fish's weight is around {prediction} gr")