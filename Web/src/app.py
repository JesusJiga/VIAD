import streamlit as st
import pandas as pd
import joblib
import pymongo
import dictionaries
import conection
import ip_path

# Elige el path para local o streamlit
path = ip_path.get_path()
# Establece la conexión con Atlas/MongoDB
mongodb_viad = conection.get_conection(st.secrets['DB_PASSWORD'])

# Comprobamos valores máximos y mínimos de los registros de la base de datos
min_year = int(mongodb_viad.find({},{'Year':True}).sort('Year', pymongo.ASCENDING).limit(1)[0]['Year'])
max_year = int(mongodb_viad.find({},{'Year':True}).sort('Year', pymongo.DESCENDING).limit(1)[0]['Year'])

st.title("¡Bienvenido a VIAD!")

st.markdown("Aquí podrás obtener una predicción sobre las muertes en España. Estas pueden ser en terminos generales o por causas especificas.", unsafe_allow_html=False)

st.markdown("Tenga en cuenta de que se trata de una elaboración propia con datos extraídos del sitio web del [INE](https://www.ine.es/) a fecha 23/02/203. Los resultados obtenidos son una mera orientación de lo que podría ser.", unsafe_allow_html=False)

st.markdown("Cabe destacar que dichas predicciones no tienen en cuenta posibles futuras catastrofes naturales, guerras o cualquier causa fuera de conductas normales.", unsafe_allow_html=False)

year = st.slider('Seleccione un año', min_value=min_year, max_value=2050, value=2023, step=1, format="%d")

col1, col2  = st.columns(2)
with col1:
    community = st.selectbox("Seleccione una comunidad", (dictionaries.communities))
with col2:
    if dictionaries.communities[community] == 0:
        st.text("Todas las provincias seleccionadas")
        province = "Todas"
    else:        
        province = st.selectbox("Seleccione una provincia", (dictionaries.provinces))
disease = st.selectbox("Seleccione una causa de muerte", (dictionaries.diseases))
col1, col2  = st.columns(2)
with col1:
    age = st.selectbox("Seleccione una grupo de edad", (dictionaries.ages))
with col2:
    gender = st.selectbox("Seleccione género", (dictionaries.genders))

if st.button('Comprobar'):

    #Búsqueda datos reales
    if year <= max_year:

        # TODO: Rango de años
        st.text(community)
        st.text(province)
        st.text(disease)
        st.text(age)
        if community == "Todas" or province == "Todas" or disease == "Todas" or age == "Todas": 
            st.text("ha seleccionado todas")
        else:
            result = mongodb_viad.find(
                {'Year' : str(year),
                'Community' : str(dictionaries.communities[community]),
                'Province' : str(dictionaries.provinces[province]),
                'Disease' : str(dictionaries.diseases[disease]),
                'Age' : str(dictionaries.ages[age])
                })

            # print results
            for i in result:
                st.text(i['Year']) 
                st.text(i['Both Genders'])
                st.text(i['Men'])
                st.text(i['Women'])
    #Predicción
    else:
        # Cargamos los modelos
        both_genders_model = joblib.load(path + "both_genders_model.pkl")
        men_model = joblib.load(path + "men_model.pkl")
        women_model = joblib.load(path + "women_model.pkl")

        X = pd.DataFrame([
            [
                dictionaries.communities[community],
                dictionaries.provinces[province],
                dictionaries.diseases[disease],
                dictionaries.ages[age], 
                year
            ]
        ],
        columns = ["Community", "Province", "Disease", "Age", "Year"])

        prediction = ""
        if dictionaries.genders[gender] == 0:
            prediction = both_genders_model.predict(X)[0]
        elif dictionaries.genders[gender] == 1:
            prediction = men_model.predict(X)[0]
        elif dictionaries.genders[gender] == 2:
            prediction = women_model.predict(X)[0]
        else:
            st.text("Ha habido un error con el género")

        st.write(f"Habrá {prediction} muertes. (Tenga en cuenta un margen de error)")