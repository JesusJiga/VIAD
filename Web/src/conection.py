import pymongo
import streamlit as st

@st.cache_resource
def get_conection(key):
    client = pymongo.MongoClient(f"mongodb+srv://JiGa:{key}@viad.b6yfn8g.mongodb.net/?retryWrites=true&w=majority")

    database = "VIAD"
    collection = "CausesDeath"
    
    return client[database][collection]