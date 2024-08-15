import pandas as pd
import joblib
import funciones 

df = pd.read_parquet('google_yelp_mini.parquet',engine='pyarrow')

# Cargar múltiples objetos desde un archivo .pkl
with open('artefactos_mini.pkl', 'rb') as archivo:
    artefactos = joblib.load(archivo)

matriz = artefactos['matriz']
vectorizador = artefactos['vectorizer']

def rec_system(text):
    try:
        df_similarity = funciones.similaridad(df,text,vectorizador,matriz)
        df_rec = funciones.recomendar_ciudad(df_similarity)
        city = df_rec[df_rec["similarity_score"]==df_rec["similarity_score"].max()]["city"].iloc[0]
        city.replace(" ","-")
        return city
    except Exception:
        return  "error"
    return city
