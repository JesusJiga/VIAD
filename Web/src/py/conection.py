import pymongo
import pandas as pd
from py import dictionaries

def start_conection(key):
    return pymongo.MongoClient(f"mongodb+srv://JiGa:{key}@viad.b6yfn8g.mongodb.net/?retryWrites=true&w=majority")

def get_min_year(client):
    return int(pd.Timestamp(client.find({},{'Year':True}).sort('Year', pymongo.ASCENDING).limit(1)[0]['Year']).strftime('%Y'))

def get_max_year(client):
    return int(pd.Timestamp(client.find({},{'Year':True}).sort('Year', pymongo.DESCENDING).limit(1)[0]['Year']).strftime('%Y'))

def get_historical_data(client, year, community, province, disease, age):
    
    query = {}

    query['Year'] = year

    # si la provincia y la comunidad vale 0 no se añade nada para que obtenga todas
    if province == 0:
        if community != 0:
            # seleccionar las provincias de la comunidad elegida 
            query['$or'] = [{'Province': str(p)} for p in dictionaries.community_provinces[community]]

    else:
        # seleccionar solo la provincia elegida
        query['Province'] = str(province)

    # si la enfermedad vale 0 no se añade nada para que obtenga todas
    if disease != 0:
        # selecciona solo la enfermedad elegida
        query['Disease'] = str(disease)

    # si la edad vale 0 no se añade nada para que se obtengan todas
    if age != 0:
        # selecciona solo el rango de edad elegido
        query['Age'] = str(age)

    return (client.find(query) , query)

def get_total_both(client):
    resultado = client.aggregate([
                    {
                        "$project": {
                            "Both Genders Numeric": {"$toInt": "$Both Genders"}
                        }
                    },
                    {
                        "$group": {
                            "_id": None,
                            "total": {"$sum": "$Both Genders Numeric"}
                        }
                    }])
    return resultado

def get_total_men(client):
    resultado = client.aggregate([
                    {
                        "$project": {
                            "Men Numeric": {"$toInt": "$Men"}
                        }
                    },
                    {
                        "$group": {
                            "_id": None,
                            "total": {"$sum": "$Men Numeric"}
                        }
                    }])
    return resultado

def get_total_women(client):
    resultado = client.aggregate([
                    {
                        "$project": {
                            "Wome Numeric": {"$toInt": "$Women"}
                        }
                    },
                    {
                        "$group": {
                            "_id": None,
                            "total": {"$sum": "$Women Numeric"}
                        }
                    }])
    return resultado

def get_total_both_by_year(client):
    resultado = client.aggregate([
        {
            "$project": {
                "Both Genders Numeric": {"$toInt": "$Both Genders"},
                "Year": "$Year"
            }
        },
        {
            "$group": {
                "_id": "$Year",
                "total": {"$sum": "$Both Genders Numeric"}
            }
        }
    ])
    return list(resultado)

def get_total_women_by_year(client):
    resultado = client.aggregate([
        {
            "$project": {
                "Women Numeric": {"$toInt": "$Women"},
                "Year": "$Year"
            }
        },
        {
            "$group": {
                "_id": "$Year",
                "total": {"$sum": "$Women Numeric"}
            }
        }
    ])
    return list(resultado)

def get_total_men_by_year(client):
    resultado = client.aggregate([
        {
            "$project": {
                "Men Numeric": {"$toInt": "$Men"},
                "Year": "$Year"
            }
        },
        {
            "$group": {
                "_id": "$Year",
                "total": {"$sum": "$Men Numeric"}
            }
        }
    ])
    return list(resultado)

    
