#Import libraries
from hashlib import new
from sys import implementation
from turtle import distance

import numpy as py
import pandas as pd
import ast
import nltk

ast.literal_eval

from sklearn.feature_extraction.text import CountVectorizer

from nltk.stem.porter import PorterStemmer


movies =  pd.read_csv('tmdb_5000_movies.csv')
credits =  pd.read_csv('tmdb_5000_credits.csv')

#merging both datasets
movies = movies.merge(credits, on = 'title')

#useful cols = genres, id, keywords, title, overview, cast, crew
#extract only useful cols
movies = movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]

#make new dataframe (movie_id | title | tags(merge rest))
#pre-processing(removing null and duplicate values)

#for null value
movies.isnull().sum()
movies.dropna(inplace=True)

#for duplicate values
movies.duplicated().sum()

### For organising data ###

#print(movies.iloc[0].genres)
#['Action', ' Asventure' , ....]
#['Action', ' Asventure' , ....]

#to convert string of list to list, we use ast.literal_eval
#Fxn to organize genres column
def convert(obj):
    l=[]
    for i in ast.literal_eval(obj):
        l.append(i['name'])
    return l

movies['genres'] = movies['genres'].apply(convert)

#organizing keywords
movies['keywords'] = movies['keywords'].apply(convert)

#Fxn to organize cast
#only pick 1st three 
def convert3(obj):
    l=[]
    counter = 0
    for i in ast.literal_eval(obj):
        if counter != 3:
            l.append(i['name'])
            counter+=1
        else:
            break
    return l

movies['cast'] = movies['cast'].apply(convert3)

#Fxn to organize crew(director)
def fetch_director(obj):
    l=[]
    for i in ast.literal_eval(obj):
        if i['job'] == 'Director':
            l.append(i['name'])
    return l

movies['crew'] = movies['crew'].apply(fetch_director)

#organizing overview column and converting overview(string) into list
movies['overview'] = movies['overview'].apply(lambda x:x.split())

#list concatenate = string(big tag)
movies['genres'] = movies['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies['cast'] = movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew'] = movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])

#concatenate all useful columns
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_df = movies[['movie_id', 'title', 'tags']]

new_df['tags'] = new_df['tags'].apply(lambda x : " ".join(x))

#converting into lowercase
new_df['tags'] = new_df['tags'].apply(lambda x : x.lower())

cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()

#Stemming
ps = PorterStemmer()
def stem(text):
    y = []

    for i in text.split():
        y.append(ps.stem(i))

    return " ".join(y)

new_df['tags'] = new_df['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]

    for i in movies_list:
        print(new_df.iloc[i[0]].title)

import pickle

pickle.dump(new_df.to_dict(), open('movies.pkl', 'wb'))

pickle.dump(similarity, open('similarity.pkl', 'wb'))