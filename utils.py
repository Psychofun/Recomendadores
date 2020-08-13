import pandas as pd 
import numpy as np 
import json 
import seaborn as sns



def read_data():
    animes = pd.read_csv('./data/anime.csv')
    puntajes = pd.read_csv('./data/rating.csv')

    return animes, puntajes

def get_dataframe():
    animes,puntajes =  read_data()
    
    # Reemplaza puntaje -1 por 0 
    puntajes.rating.replace(to_replace = -1, value = 0, inplace= True)
    
    # Mezcla los dos DataFrames
    animes_puntaje = puntajes.merge(animes, left_on = 'anime_id',right_on = 'anime_id',suffixes=['_user',''])
   
    # Mezcla 
    animes_puntaje  = animes_puntaje.sample(frac=1)
   

    return animes_puntaje


def get_rating_matrix():
    animes_puntaje = get_dataframe()

    # Usa solo ciertas columnas
    animes_puntaje = animes_puntaje[['user_id', 'anime_id', 'rating_user', 'name']]

    #Considera animes con 1000 o más puntajes
    animes_puntaje = animes_puntaje.groupby('anime_id').filter(
        lambda d: d['rating_user'].count() >= 1000)


    # Usa solo 100,000 de ejemplos
    animes_puntaje = animes_puntaje.iloc[:100000]
    
    # Matrix de puntajes. Renglones: usuarios, columnas: items (animes)
    # R[i,j] puntaje de la pelicula j por el usuario i 
    R = animes_puntaje.pivot_table(values='rating_user', index = 'user_id',columns = 'anime_id', fill_value = 0) 
    
    return R

def plot_rating_distribution():
    sns.set()
    animes_puntaje = get_dataframe()
    with sns.axes_style('white'):
        g = sns.catplot("rating_user", data=animes_puntaje, aspect=2.0,kind='count')
        g.set_ylabels("Total number of ratings")
        g.savefig('puntajes.png')


def save_dicts(id_to_anime_name, anime_name_to_id):
    with open('id_to_anime_name','w') as f:
        json.dump(id_to_anime_name,f)
        
    with open('anime_name_to_id','w') as f :
        json.dump(anime_name_to_id,f)
        

def load_dict(name):
    try:
        with open(name, 'r') as f:
            dict_ = json.load(f)
    except IOError:
        # diccionario vacio
        dict_ = {}
    
    return dict_

def load_anime_dicts():
    id_to_anime_name = load_dict('id_to_anime_name')
    anime_name_to_id = load_dict('anime_name_to_id')
    
    return id_to_anime_name, anime_name_to_id

def create_dicts(data):
    id_to_anime_name = {
    }
    anime_name_to_id = {
    
    }

    for i in range(data.shape[0]):
        point = data.iloc[i]
    
        anime_id = str(point['anime_id'])
        nombre_anime = point['name']
    
        id_to_anime_name[anime_id] = nombre_anime
        anime_name_to_id[nombre_anime] = anime_id
    
        
    return id_to_anime_name,anime_name_to_id
    


if __name__ == '__main__':
    plot_rating_distribution()
