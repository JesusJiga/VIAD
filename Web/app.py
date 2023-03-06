import streamlit as st
import pandas as pd
import joblib
import boto3
import AWS_config

# session = boto3.Session(AWS_config.aws_access_key_id, AWS_config.aws_secret_access_key, AWS_config.aws_session_token)
# s3 = session.client('s3', region_name='us-east-1')

s3 = boto3.client('s3', aws_access_key_id=AWS_config.aws_access_key_id, aws_secret_access_key=AWS_config.aws_secret_access_key, aws_session_token=AWS_config.aws_session_token, region_name='us-east-1')

bucket_name = 'viad'
folder_path = 'models/'
filename = 'both_genders_model.pkl'

full_path = folder_path + filename

object = s3.get_object(Bucket=bucket_name, Key=full_path)
file_content = object['Body'].read()

# Unpickle classifier
both_genders_model = joblib.load(file_content)

st.title("¡Bienvenido a VIAD!")

st.markdown("Aquí podrás obtener una predicción sobre las muertes en España. Estas pueden ser en terminos generales o por causas especificas.", unsafe_allow_html=False)

st.markdown("Tenga en cuenta de que se trata de una elaboración propia con datos extraídos del sitio web del [INE](https://www.ine.es/) a fecha 23/02/203. Los resultados obtenidos son una mera orientación de lo que podría ser.", unsafe_allow_html=False)

st.markdown("Cabe destacar que dichas predicciones no tienen en cuenta posibles futuras catastrofes naturales, guerras o cualquier causa fuera de conductas normales.", unsafe_allow_html=False)

year = st.slider('Seleccione un año', min_value=2015, max_value=2050, value=2023, step=1, format="%d")

# Store inputs into dataframe
X = pd.DataFrame([
    [17, 45, 1, 0, year]],
    columns = ["Community", "Province", "Cause", "Age", "Year"])

# Get prediction
prediction = both_genders_model.predict(X)[0]

st.write(f"The fish's weight is around {prediction} gr")