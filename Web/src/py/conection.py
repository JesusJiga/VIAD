import pymongo
import pandas as pd

def start_conection(key):
    return pymongo.MongoClient(f"mongodb+srv://JiGa:{key}@viad.b6yfn8g.mongodb.net/?retryWrites=true&w=majority")

def get_client(conection):
    database = "VIAD"
    collection = "CausesDeath"

    return conection[database][collection]

def get_min_year(client):
    return int(pd.Timestamp(client.find({},{'Year':True}).sort('Year', pymongo.ASCENDING).limit(1)[0]['Year']).strftime('%Y'))

def get_max_year(client):
    return int(pd.Timestamp(client.find({},{'Year':True}).sort('Year', pymongo.DESCENDING).limit(1)[0]['Year']).strftime('%Y'))