# import pandas as pd

# import funciones as func

# df = pd.read_parquet('google_yelp.parquet',engine='pyarrow')

# # Cargar múltiples objetos desde un archivo .pkl
# # with open('artefact.pkl', 'rb') as archivo:
# #     artefactos = joblib.load(archivo)


# def rec_system(text="i would like to have some burguers"):
#     df_similarity = func.similaridad(df,text)
#     df_rec = func.recomendar_ciudad(df_similarity)
#     city = df_rec[df_rec["similarity_score"]==df_rec["similarity_score"].max()]["city"][0]
#     city.replace(" ","-")
#     return city
