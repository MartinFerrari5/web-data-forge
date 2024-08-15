# # #Modulo de funciones

# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
# from textblob import TextBlob
# import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
# from collections import Counter


# # general_categories = {
# #     "restaurants": [
# #         'Restaurants', 'Food', 'Cajun/Creole', 'Seafood', 'American (New)', 'Breakfast & Brunch', 'American (Traditional)', 'Sandwiches', 'Coffee & Tea', 'Burgers', 'Southern', 'Cafes', 'Mexican', 'Pizza', 'Salad', 'Specialty Food', 'Desserts', 'Italian', 'Steakhouses', 'French', 'Bakeries', 'Fast Food', 'Vegetarian', 'Chicken Wings', 'Barbeque', 'Comfort Food', 'Sushi Bars', 'Diners', 'Chinese', 'Soul Food', 'Asian Fusion', 'Ice Cream & Frozen Yogurt', 'Delis', 'Grocery', 'Gluten-Free', 'Mediterranean', 'Vegan', 'Vietnamese', 'Donuts', 'Juice Bars & Smoothies', 'Latin American', 'Tacos', 'Soup', 'Dive Bars', 'Thai', 'Tapas/Small Plates', 'Ethnic Food', 'Live/Raw Food', 'Tex-Mex', 'Food Delivery Services', 'Seafood Markets', 'Brasseries', 'Greek'
# #     ],
# #     "drinks_and_bars": ['Nightlife', 'Bars', 'Cocktail Bars', 'Beer', 'Wine & Spirits', 'Pubs', 'Wine Bars', 'Sports Bars', 'Breweries', 'Beer Bar', 'Gastropubs', 'Lounges', 'Jazz & Blues', 'Music Venues'
# #     ],
# #     "hotels_and_events": ['Event Planning & Services', 'Venues & Event Spaces', 'Hotels & Travel', 'Hotels', 'Tours', 'Historical Tours', 'Party & Event Planning'
# #     ],
# #     "shopping_and_beauty": ['Shopping', 'Beauty & Spas', 'Nail Salons', 'Fashion', 'Hair Salons', 'Hair Removal', 'Skin Care', 'Waxing', 'Flowers & Gifts'
# #     ],
# #     "travels": ['Hotels & Travel', 'Tours', 'Historical Tours', 'Transportation', 'Auto Repair'
# #     ],
# #     "services_and_entertainment": ['Arts & Entertainment', 'Active Life', 'Automotive', 'Local Services', 'Home Services', 'Health & Medical', 'Massage', 'Home & Garden', 'Pets', 'Public Services & Government', 'Flowers & Gifts'
# #     ]}

# # def process_categories(df, general_categories):
# #     # Invertir el diccionario para mapear cada categoría específica a su categoría general
# #     category_to_general = {cat: gen for gen, cats in general_categories.items() for cat in cats}

# #     def map_to_general(categories_list):
# #         return [category_to_general.get(cat, "others") for cat in categories_list]

# #     def get_least_frequent_general(categories_list):
# #         category_counts = Counter(categories_list)
# #         sorted_categories = sorted(category_counts.items(), key=lambda x: x[1])
# #         for category, count in sorted_categories:
# #             if all(category != other_category for other_category in categories_list if other_category != category):
# #                 return category
# #         return sorted_categories[0][0]  # En caso de que todas las categorías sean igual de frecuentes

# #     def get_two_least_frequent_generals(categories_list):
# #         category_counts = Counter(categories_list)
# #         sorted_categories = sorted(category_counts.items(), key=lambda x: x[1])
# #         unique_categories = [category for category, count in sorted_categories if categories_list.count(category) == 1]
# #         if len(unique_categories) >= 2:
# #             return unique_categories[:2]
# #         elif len(unique_categories) == 1:
# #             second_least_frequent = sorted_categories[1][0] if len(sorted_categories) > 1 else unique_categories[0]
# #             return [unique_categories[0], second_least_frequent]
# #         else:
# #             return [sorted_categories[0][0], sorted_categories[1][0]] if len(sorted_categories) > 1 else [sorted_categories[0][0]]

# #     # Aplicar las funciones al DataFrame
# #     df['general_mapped'] = df['categories_list'].apply(map_to_general)
# #     df['min_category'] = df['general_mapped'].apply(get_least_frequent_general)
# #     df['double_category'] = df['general_mapped'].apply(get_two_least_frequent_generals)
# #     df['double_category'] = df['double_category'].apply(lambda x: ', '.join(x))

# #     return df


# # def lemmatized_tokenize_text(df):
# #     # Inicializa el lematizador y las stopwords
# #     lemmatizer = WordNetLemmatizer()
# #     stopwords = nltk.corpus.stopwords.words('english')
# #     # Define la función de lematización
# #     def lemmatize_tokens(tokens):
# #         return [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stopwords]
# #     # Aplica la tokenización
# #     df['tokens'] = df['text'].apply(lambda x: word_tokenize(x.lower()))
# #     # Aplica la lematización
# #     df['lemmatized_tokens'] = df['tokens'].apply(lemmatize_tokens)
# #     # Reconstruye el texto
# #     df['reconstructed_text'] = df['lemmatized_tokens'].apply(lambda tokens: ' '.join(tokens))
# #     return df


# # def analyze_sentiment(df):
# #     df['polaridad'] = df['reconstructed_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
# #     df['sentimiento'] = df['polaridad'].apply(lambda x: 'positivo' if x > 0.25 else 'negativo' if x < 0 else 'negativo')
# #     df['target'] = (df['sentimiento'] == 'positivo').astype(int)
# #     return df

def similaridad(df, texto,vectorizador,matriz):
    new_text_vector = vectorizador.transform([texto])
    similarity_scores = cosine_similarity(new_text_vector, matriz)
    documentos_mas_similares = similarity_scores[0].argsort()[::-1] # indices de los valores mas similares
    # Filtrar índices fuera de rango
    documentos_mas_similares = [i for i in documentos_mas_similares if i < len(df)]
    # Solo seleccionamos los datos que tienen un índice válido
    datos_similares = df.iloc[documentos_mas_similares].copy()
    datos_similares.loc[:, 'similarity_score'] = similarity_scores[0][documentos_mas_similares]
    return datos_similares



def recomendar_ciudad(df_sin_filtrar):
    # 1.0: Filtrar ciudades con más de 100 negocios únicos
    unicos = df_sin_filtrar.groupby('city')['name'].nunique().reset_index()
    unicos.columns = ['ciudad', 'unicos']
    ciudades_filtradas = unicos[unicos['unicos'] > 100]['ciudad']
    df_filtrado = df_sin_filtrar[df_sin_filtrar['city'].isin(ciudades_filtradas)]
    # 1.1: Filtrar por la ciudad con el mayor puntaje de similitud promedio
    promedio_por_ciudad = df_filtrado.groupby('city')['similarity_score'].mean().reset_index()
    promedio_por_ciudad = promedio_por_ciudad.sort_values(by='similarity_score', ascending=False)
    ciudad_recomendada = promedio_por_ciudad.iloc[0].values[0]
    df_filtrado = df_filtrado[df_filtrado['city'] == ciudad_recomendada]
    # 1.2: Filtrar negocios con más de 3.5 estrellas promedio
    promedio_estrellas_negocio = df_filtrado.groupby('name')['stars_review'].mean().reset_index()
    promedio_estrellas_negocio = promedio_estrellas_negocio.query('stars_review > 3.5')
    df_final = df_filtrado.merge(promedio_estrellas_negocio, on='name', how='left', suffixes=('', '_promedio'))
    df_final.dropna(subset=['stars_review_promedio'], inplace=True)
    # 1.3: Filtrar por target = 1
    #df_final = df_final[df_final['target'] == 1]
    # 1.4: Filtrar por similarity_score > 0
    df_final = df_final[df_final['similarity_score'] > 0]
    # 1.5: Eliminar duplicados por nombre de negocio
    df_final.drop_duplicates(subset='name', inplace=True)
    return df_final

# # def recomendacion_map(df):
# #     df_sin_filtrar = df
# #     df_sin_filtrar.sort_values(by='similarity_score', ascending=False, inplace=True)
# #     df_filtrado = df_sin_filtrar[df_sin_filtrar['target'] == 1]
# #     df_filtrado.drop_duplicates(subset='name', inplace=True)
# #     df_filtrado = df_filtrado[:10]
# #     return df_filtrado
