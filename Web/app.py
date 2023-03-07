import streamlit as st
import pandas as pd
import joblib

# Unpickle classifier
both_genders_model = joblib.load("both_genders_model.pkl")

st.title("¡Bienvenido a VIAD!")

st.markdown("Aquí podrás obtener una predicción sobre las muertes en España. Estas pueden ser en terminos generales o por causas especificas.", unsafe_allow_html=False)

st.markdown("Tenga en cuenta de que se trata de una elaboración propia con datos extraídos del sitio web del [INE](https://www.ine.es/) a fecha 23/02/203. Los resultados obtenidos son una mera orientación de lo que podría ser.", unsafe_allow_html=False)

st.markdown("Cabe destacar que dichas predicciones no tienen en cuenta posibles futuras catastrofes naturales, guerras o cualquier causa fuera de conductas normales.", unsafe_allow_html=False)

year = st.slider('Seleccione un año', min_value=2015, max_value=2050, value=2023, step=1, format="%d")

community = st.selectbox("Seleccione una comunidad", ('Andalucía', 'Extremadura'))

province = st.selectbox("Seleccione una provincia", ('Málaga', 'Jaén'))

cause = st.selectbox("Seleccione una causa de muerte", ('Eres muy malo'))

age = st.selectbox("Seleccione una grupo de edad", ('0 -5', '6 -10'))

# Store inputs into dataframe
X = pd.DataFrame([
    [community, province, cause, age, year]],
    columns = ["Community", "Province", "Cause", "Age", "Year"])

if st.button('Comprobar'):

    # Get prediction
    prediction = both_genders_model.predict(X)[0]

    st.write(f"The fish's weight is around {prediction} gr")