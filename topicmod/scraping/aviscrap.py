# imports
import os
import unicodedata
from datetime import *
import numpy as np
import pandas as pd
import googlemaps
from topicmod.utils.helper import timer
from topicmod.config import myconfig

#config
os.environ['http_proxy'] = myconfig.proxy['http']
os.environ['https_proxy'] = myconfig.proxy['https']
gmaps = googlemaps.Client(key=myconfig.google_apikey)



def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


def format_scrap_ids(places, bank_name):
    if len(places) > 0:
        agence = next((obj for obj in places if bank_name in remove_accents(obj['name'])),'not_found')
        if agence!='not_found' : 
            try:
                name = agence['name']
            except KeyError:
                name = ""
            try:
                lat = agence['geometry']['location']['lat']
            except KeyError:
                lat = ""
            try:
                lng = agence['geometry']['location']['lng']
            except KeyError:
                lng = ""
            try:
                place_id = agence['place_id']
            except KeyError:
                place_id = ""
            try:
                rating = agence['rating']
            except KeyError:
                rating = ""
            try:
                user_ratings_total = agence['user_ratings_total']
            except KeyError:
                user_ratings_total = ""
        else:
            place_id= name= lat= lng= rating= user_ratings_total=np.nan
    else:
        place_id= name= lat= lng= rating= user_ratings_total=np.nan
    return pd.Series([place_id, name, lat, lng, rating, user_ratings_total])


def format_scrap_reviews(place_id, details): 
    try:
        address = details['formatted_address']
    except KeyError:
        address = ""
    try:
        reviews = details['reviews']
    except KeyError:
        reviews = []
    rev_temp = []
    for review in reviews:
        author_name = review['author_name']
        user_rating = review['rating']
        text = review['text']
        time = str(date.fromtimestamp(review['time']))
        rev_temp.append((author_name, user_rating, text, time))
    rev_df = pd.DataFrame(rev_temp, columns = ['author_name', 'user_rating', 'text', 'review_date'])
    rev_df[['place_id','address']] = place_id, address
    return rev_df


def get_placeid_coords(gmaps, coords, agence_name, etab_name, bank_name):
    str_name = ''
    if bank_name in etab_name:
        str_name = bank_name
    else:
        str_name = etab_name
    str_name = str_name + " "+ agence_name
    places = gmaps.places_nearby((coords), name= str_name, \
                                     rank_by = "distance")['results']
    return format_scrap_ids(places, bank_name)


def get_placeid(gmaps, agence_name, etab_name, bank_name, street_name):
    str_address = ''
    if bank_name in etab_name:
        str_address = bank_name
    else:
        str_address = etab_name
    str_address = str_address + " "+ agence_name + " " + street_name
    places = gmaps.places(str_address)['results'] 
    return format_scrap_ids(places, bank_name)

def get_placeid_details(gmaps, place_id):
    fields =['name','formatted_address','rating','review']
    places_details = gmaps.place(place_id, language='fr', fields=fields)
    return format_scrap_reviews(place_id, places_details['result']) 

def format_geopoints(lat, lng):
    geopoints = "{:.7f}".format(lat)+','+"{:.7f}".format(lng)
    return geopoints

@timer
def scrap_ids(df_agencies):
    new_columns = ['place_id', 'place_name', 'lat', 'lng', 'rating', 'user_ratings_total']
    df_total = pd.DataFrame()

    #df_wi = pd.read_csv("data/input/ag_wi_ce.csv", sep = ";", encoding = "utf-8")
    mask = df_agencies.coords.isnull()
    df_wi = df_agencies[~mask] # agencies with coords
    df_wo = df_agencies[mask] # agencies withouts coords

    df_wi[new_columns] = df_wi.apply(lambda x: get_placeid_coords(gmaps, x.coords, x.nom_agence, x.nom_etab, x.nom_banque), axis=1)
    #df_wi['geopoints'] = df_wi['lat'].apply("{:.7f}".format)+','+df_wi['lng'].apply("{:.7f}".format)
    df_wi['geopoints'] = df_wi.apply(lambda x: format_geopoints(x.lat, x.lng), axis=1)
    df_wi.drop(columns=['coords', 'lat', 'lng'], inplace = True)

    df_wo[new_columns] = df_wo.apply(lambda x: get_placeid(gmaps, x.nom_agence, x.nom_banque, x.nom_banque, x.rue), axis=1)
    df_wi['geopoints'] = df_wo.apply(lambda x: format_geopoints(x.lat, x.lng), axis=1)
    df_wo.drop(columns=['coords', 'lat', 'lng'], inplace = True)
    df_total = df_wi.append(df_wo)
    return df_total

@timer
def scrap_reviews(df_ids):
    df_ids = df_ids.dropna(subset=['place_id'])
    place_id_list = df_ids.place_id.to_list()
    df_reviews = pd.DataFrame()
    for placeid in place_id_list :
        temp = get_placeid_details(gmaps, placeid)
        df_reviews = pd.concat([df_reviews, temp], ignore_index=True)
    df_final = pd.merge(left = df_ids, right = df_reviews, how = 'left', on = 'place_id')
    return df_final

def scrap_all(df_agencies):
    df_ids = scrap_ids(df_agencies)
    df_reviews = scrap_reviews(df_ids)
    return df_reviews

if __name__ == "__main__":
    df_ids = pd.read_csv(r"data/input/scraping/agences_ids.csv",sep = ";", encoding = "utf-8")
    df_total = scrap_reviews(df_ids)
    df_reviews.to_csv("data/output/scraping/agences_reviews_{}.csv".format(datetime.now().strftime("%Y%m%d")), sep = ';', index = False, encoding = 'utf-8')
    print(f"Written to {filepath}")

