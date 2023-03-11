import streamlit as st
import pandas as pd
import dictionaries
import conection
import ip_path
import predictions
import base64

##########  Funciones para la optimización de velocidad ##########

# Elige el path para local o streamlit
@st.cache_data
def get_path():
    return ip_path.get_path()

# Establece la conexión con Atlas/MongoDB
@st.cache_resource
def start_conection():
    return conection.start_conection(st.secrets['DB_PASSWORD'])

@st.cache_resource
def get_client():
    return conection.get_client(mongodb_conection)

#Carga el csv
@st.cache_data
def load_causes_death_df():
    return predictions.load_csv(path)

# Cargamos valores máximos y mínimos de los registros de la base de datos
@st.cache_data
def get_min_year():
    return conection.get_min_year(mongodb_client)

@st.cache_data
def get_max_year():
    return conection.get_max_year(mongodb_client)

@st.cache_data
def set_background_image(image_file):
    extension = image_file.split(sep=".")[1]
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{extension};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

########## Configuración inicial ##########

st.set_page_config(page_title="VIAD", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

path = get_path()
mongodb_conection = start_conection()
mongodb_client = get_client()
causes_death_df = load_causes_death_df()
set_background_image('fondo.jpg')

########## WEB ##########

select_section = st.sidebar.selectbox(
    ":female-doctor: VIAD :male-doctor:",
    ("Home", "Linnear Regression", "ARIMA")
)

if select_section == "Home":

    st.markdown("<h1 style='text-align: center; color: #3ED5C4'>¡Bienvenido a VIAD!</h1>", unsafe_allow_html=True)

    st.markdown("Aquí podrás obtener una predicción sobre las muertes en España. Estas pueden ser en terminos generales o por causas especificas.", unsafe_allow_html=True)

    st.markdown("Tenga en cuenta de que se trata de una elaboración propia con datos extraídos del sitio web del [INE](https://www.ine.es/) a fecha 23/02/203. Los resultados obtenidos son una mera orientación de lo que podría ser.", unsafe_allow_html=False)

    st.markdown("Cabe destacar que dichas predicciones no tienen en cuenta posibles futuras catastrofes naturales, guerras o cualquier causa fuera de conductas normales.", unsafe_allow_html=False)

elif select_section == "Linnear Regresion":

    st.markdown("<h1 style='text-align: center; color: #3ED5C4'>Predicción con ARIMA</h1>", unsafe_allow_html=True)

    st.markdown("Aquí podrás obtener una predicción sobre las muertes en España. Estas pueden ser en terminos generales o por causas especificas.", unsafe_allow_html=True)

    st.markdown("Tenga en cuenta de que se trata de una elaboración propia con datos extraídos del sitio web del [INE](https://www.ine.es/) a fecha 23/02/203. Los resultados obtenidos son una mera orientación de lo que podría ser.", unsafe_allow_html=False)

    st.markdown("Cabe destacar que dichas predicciones no tienen en cuenta posibles futuras catastrofes naturales, guerras o cualquier causa fuera de conductas normales.", unsafe_allow_html=False)

    year = st.slider('Seleccione un año', min_value=get_min_year(), max_value=2050, value=2023, step=1, format="%d")

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
        if year <= get_max_year():

            # TODO: Rango de años
            st.text(community)
            st.text(province)
            st.text(disease)
            st.text(age)
            if community == "Todas" or province == "Todas" or disease == "Todas" or age == "Todas": 
                st.text("ha seleccionado todas")
            else:
                result = mongodb_client.find(
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
            data = causes_death_df
            prediction = predictions.get_prediction(data, gender_key, age_key, province_key, disease_key, year)

            st.write("Para la provincia de " + dictionaries.provinces[province_key] + " y la enfermedad " + dictionaries.diseases[disease_key] + " y rango de edad " + dictionaries.ages[age_key] + " en el año " + str(year) + " para el genero " + dictionaries.genders[gender_key])
            
            st.write(f"Habrá {prediction} muertes. (Tenga en cuenta un margen de error)")

else:
    st.markdown("<h1 style='text-align: center; color: #3ED5C4'>Predicción con Linear Regressor</h1>", unsafe_allow_html=True)

    st.markdown("Aquí podrás obtener una predicción sobre las muertes en España. Estas pueden ser en terminos generales o por causas especificas.", unsafe_allow_html=True)

    st.markdown("Tenga en cuenta de que se trata de una elaboración propia con datos extraídos del sitio web del [INE](https://www.ine.es/) a fecha 23/02/203. Los resultados obtenidos son una mera orientación de lo que podría ser.", unsafe_allow_html=False)

    st.markdown("Cabe destacar que dichas predicciones no tienen en cuenta posibles futuras catastrofes naturales, guerras o cualquier causa fuera de conductas normales.", unsafe_allow_html=False)

    year = st.slider('Seleccione un año', min_value=get_min_year(), max_value=2050, value=2023, step=1, format="%d")

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
        if year <= get_max_year():

            # TODO: Rango de años
            st.text(community)
            st.text(province)
            st.text(disease)
            st.text(age)
            if community == "Todas" or province == "Todas" or disease == "Todas" or age == "Todas": 
                st.text("ha seleccionado todas")
            else:
                result = mongodb_client.find(
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
            data = causes_death_df
            prediction = predictions.get_prediction(data, gender_key, age_key, province_key, disease_key, year)

            st.write("Para la provincia de " + dictionaries.provinces[province_key] + " y la enfermedad " + dictionaries.diseases[disease_key] + " y rango de edad " + dictionaries.ages[age_key] + " en el año " + str(year) + " para el genero " + dictionaries.genders[gender_key])
            
            st.write(f"Habrá {prediction} muertes. (Tenga en cuenta un margen de error)")