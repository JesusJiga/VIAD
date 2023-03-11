import streamlit as st
import pandas as pd
from py import dictionaries
from py import conection
from py import ip_path
from py import predictions
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

# Carga de la imagen de fondo
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

@st.cache_data
def transform_images(image_file):
    with open(image_file, "rb") as image_file:
        return base64.b64encode(image_file.read())

# Carga del css
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

########## Configuración inicial ##########

st.set_page_config(page_title="VIAD", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

path = get_path()
mongodb_conection = start_conection()
mongodb_client = get_client()
causes_death_df = load_causes_death_df()

load_css(path + 'css/viad.css')
set_background_image(path + 'images/background.jpg')

########## WEB ##########

select_section = st.sidebar.selectbox(":female-doctor: VIAD :male-doctor:",("Inicio", "Estadísticas", "Datos"))

if select_section == "Inicio":

    st.markdown("<h1 class='myh1'>¡Bienvenido a VIAD!</h1>", unsafe_allow_html=True)

    st.markdown("<h2 class='myh2'>Trabajo de fin de master de IA y Big Data</h2>", unsafe_allow_html=True)

    st.markdown("<h3 class='myh3'>Jesús Jiménez García. <a href='https://www.linkedin.com/in/jesusjiga/'>Linkedin</a></h3>", unsafe_allow_html=True)

    st.markdown("<h3 class='myh3'>Jose Pérez Soler <a href='https://www.linkedin.com/in/demiurgodigital/'>Linkedin</a><h3>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
            <div class="images">
                <img src="data:image/png;base64,{transform_images(path + 'images/LoTechBlanco.png').decode()}" alt="logo malaga tech" width="250">
                <img src="data:image/png;base64,{transform_images(path + 'images/LogoIABD.png').decode()}" alt="logo master ia big data" width="100">
                <img src="data:image/png;base64,{transform_images(path + 'images/LogoAccenture.png').decode()}" alt="logo accenture" width="100">
            </div>
        """, unsafe_allow_html=True)

elif select_section == "Estadísticas":
    st.markdown("<h1 class='myh1'>Estadísticas</h1>", unsafe_allow_html=True)

elif select_section == "Datos":

    st.markdown("<h1 class='myh1'>Consulta de datos</h1>", unsafe_allow_html=True)

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
            provinces_in_community = dictionaries.community_provinces[community_key]
            provinces_dict = { 0 : 'Todas'}
            for province_id in provinces_in_community:
                provinces_dict[province_id] = dictionaries.provinces[province_id]
            province = st.selectbox("Seleccione una provincia", provinces_dict.values())
            if province == "Todas":
                province_key = 0
            elif province in dictionaries.provinces.values():
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

            year = str(pd.to_datetime(year, format='%Y')).split(sep=' ')[0]
            # TODO: Rango de años

            st.write("Los datos siguientes son los resultados de su consulta.")
            st.write("En este caso los datos obtenidos son reales según los datos públicos de la página oficial del Instituto Nacional de Estadística.")

            cursor, query = conection.get_historical_data(mongodb_client, year, community_key, province_key, disease_key, age_key)

            gender_column_name = ""
            # Se define la cabecera personalizada 
            if gender_key == 0:
                gender_column_name = 'Both Genders'
                headers = ['Año', 'Provincia', 'Enfermedad', 'Edad', 'Ambos sexos']
            elif gender_key == 1:
                gender_column_name = 'Men'
                headers = ['Año', 'Provincia', 'Enfermedad', 'Edad', 'Ambos sexos']
            elif gender_key == 2:
                gender_column_name = 'Women'
                headers = ['Año', 'Provincia', 'Enfermedad', 'Edad', 'Ambos sexos']

            data = []

            # iteramos sobre el cursor y se agregan los valores a la lista
            for document in cursor:
                row = [
                    str(document['Year']).split(sep='-')[0],
                    dictionaries.provinces[int(document['Province'])],
                    dictionaries.diseases[int(document['Disease'])],
                    dictionaries.ages[int(document['Age'])],
                    document[gender_column_name]
                ]
                data.append(row)

            # Se crea el dataframe con los datos y las cabeceras personalizadas
            df = pd.DataFrame(data, columns=headers)

            # mostramos por pantalla
            st.table(df)

        #Predicción
        else:
            data = causes_death_df.copy()
            prediction = predictions.get_prediction(data, gender_key, age_key, community_key, province_key, disease_key, year)
          
            st.write(f"Para su consulta hay una predicción de que habrá <span class='neg_mark'>{abs(prediction)}</span> muertes.", unsafe_allow_html=True)
            st.write("Siempre tenga en cuenta un margen de error y que son predicciones a partir de los datos registrados en bases de datos públicas oficiales.")
            st.write("El resultado no tienen ninguna validez legal y es meramente orientativa.")
