import streamlit as st
import pandas as pd
import pymongo
import dictionaries
import conection
import ip_path
import predictions

# Elige el path para local o streamlit
path = ip_path.get_path()
# Establece la conexión con Atlas/MongoDB
mongodb_viad = conection.get_conection(st.secrets['DB_PASSWORD'])
#Carga el csv
causes_death_df = predictions.load_csv(path)

# Comprobamos valores máximos y mínimos de los registros de la base de datos
min_year = int(pd.Timestamp(mongodb_viad.find({},{'Year':True}).sort('Year', pymongo.ASCENDING).limit(1)[0]['Year']).strftime('%Y'))
max_year = int(pd.Timestamp(mongodb_viad.find({},{'Year':True}).sort('Year', pymongo.DESCENDING).limit(1)[0]['Year']).strftime('%Y'))

st.title("¡Bienvenido a VIAD!")

st.markdown("Aquí podrás obtener una predicción sobre las muertes en España. Estas pueden ser en terminos generales o por causas especificas.", unsafe_allow_html=False)

st.markdown("Tenga en cuenta de que se trata de una elaboración propia con datos extraídos del sitio web del [INE](https://www.ine.es/) a fecha 23/02/203. Los resultados obtenidos son una mera orientación de lo que podría ser.", unsafe_allow_html=False)

st.markdown("Cabe destacar que dichas predicciones no tienen en cuenta posibles futuras catastrofes naturales, guerras o cualquier causa fuera de conductas normales.", unsafe_allow_html=False)

year = st.slider('Seleccione un año', min_value=min_year, max_value=2050, value=2023, step=1, format="%d")

col1, col2  = st.columns(2)
with col1:
    community = st.selectbox("Seleccione una comunidad", (dictionaries.communities.values()))
    if community in dictionaries.communities.values():
        community_key = list(dictionaries.communities.keys())[list(dictionaries.communities.values()).index(community)]
with col2:
    if community_key == 0:
        st.text("Todas las provincias seleccionadas")
        province_key = 0
    else:        
        province = st.selectbox("Seleccione una provincia", (dictionaries.provinces.values()))
        if province in dictionaries.provinces.values():
            province_key = list(dictionaries.provinces.keys())[list(dictionaries.provinces.values()).index(province)]
disease = st.selectbox("Seleccione una causa de muerte", (dictionaries.diseases.values()))
if disease in dictionaries.diseases.values():
    disease_key = list(dictionaries.diseases.keys())[list(dictionaries.diseases.values()).index(disease)]
col1, col2  = st.columns(2)
with col1:
    age = st.selectbox("Seleccione una grupo de edad", (dictionaries.ages.values()))
    if age in dictionaries.ages.values():
        age_key = list(dictionaries.ages.keys())[list(dictionaries.ages.values()).index(age)]
with col2:
    gender = st.selectbox("Seleccione género", (dictionaries.genders.values()))
    if gender in dictionaries.genders.values():
        gender_key = list(dictionaries.genders.keys())[list(dictionaries.genders.values()).index(gender)]

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
                {
                'Year' : pd.to_datetime(year, format='%Y'),
                'Community' : str(community_key),
                'Province' : str(province_key),
                'Disease' : str(disease_key),
                'Age' : str(age_key)
                })

            # print results
            for i in result:
                st.text(i['Year']) 
                st.text(i['Both Genders'])
                st.text(i['Men'])
                st.text(i['Women'])
    #Predicción
    else:
        # st.text(community_key)
        st.text("Para la provincia " + dictionaries.provinces[province_key] + " con código " + str(province_key))
        st.text("y la enfermedad " + dictionaries.diseases[disease_key] + " con código " + str(disease_key))
        st.text("y rango de edad " + dictionaries.ages[age_key] + " con código " + str(age_key))
        st.text("en el año " + str(year))
        st.text("para el genero " + dictionaries.genders[gender_key] + " con código " + str(gender_key))
        data = causes_death_df
        prediction = predictions.get_prediction(data, gender_key, age_key, province_key, disease_key, year)

        st.write(f"Habrá {prediction} muertes. (Tenga en cuenta un margen de error)")