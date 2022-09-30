import pandas as pd
import numpy as np
from datetime import *
from topicmod.config import myconfig

def load_df_ids(filepath=myconfig.df_ids):
    df_ids = pd.read_csv(filepath, sep=";", encoding="utf-8-sig")
    df_ids = df_ids[df_ids["rating"]!=0.0]
    df_ids = df_ids.dropna(subset=['rating'])
    return df_ids

def nbr_agence(df):
    grouped_df = (df[df['rating']>3.0].groupby(['nom_banque','nom_etab']).size()).reset_index()
    grouped_df.rename(columns={0:'rating > 3'}, inplace = True)
    grouped_df['nbr_agence'] = df.groupby(['nom_banque','nom_etab']).size().reset_index()[0]
    grouped_df['rating <= 3'] = grouped_df['nbr_agence'] - grouped_df['rating > 3']
    return grouped_df

def note_agence(grouped_df, nom_banque): 
    grouped_bq = grouped_df[grouped_df["nom_banque"].str.contains(nom_banque)]\
        .sort_values('nbr_agence', ascending=False)
    grouped_bq = grouped_bq[['nom_etab','rating <= 3','rating > 3']]
    return grouped_bq

def df_bank_points(df, nom_banque):    
    df_bq = df[df["nom_banque"].str.contains(nom_banque)].copy()
    df_bq['Latitude'] = df_bq.apply(lambda x : float(x.lat_lng.split(',')[0]), axis=1)
    df_bq['Longitude'] = df_bq.apply(lambda x : float(x.lat_lng.split(',')[1]), axis=1)
    return df_bq

def df_bank_circles(df, nom_banque):    
    df_ce = df_bank_points(df, nom_banque)

    grouped = df_ce.groupby('nom_etab').mean().reset_index()

    lat_dict = grouped.set_index('nom_etab').to_dict()['Latitude']
    lng_dict = grouped.set_index('nom_etab').to_dict()['Longitude']


    df_ce['lat_cen'] = df_ce['nom_etab'].map(lat_dict)
    df_ce['lng_cen'] = df_ce['nom_etab'].map(lng_dict)

    df_etab = grouped.copy()

    df_etab.drop(['code_etab'],inplace=True,axis=1)
    df_etab.rename(columns={"rating": "avg_rating", "user_ratings_total": "avg_nbr_ratings"}, inplace=True)


    temp_dict = df_ce.groupby(['nom_etab'])["user_ratings_total"].sum().to_dict()
    df_etab['user_ratings_total'] =df_etab['nom_etab'].map(temp_dict)

    temp_dict = df_ce[df_ce['rating']>3.0].groupby(['nom_etab']).size().to_dict()
    df_etab['rating > 3'] = df_etab['nom_etab'].map(temp_dict)

    temp_dict = df_ce.groupby(['nom_etab']).size().to_dict()
    df_etab['nbr_agence'] = df_etab['nom_etab'].map(temp_dict)
    
    return df_etab
