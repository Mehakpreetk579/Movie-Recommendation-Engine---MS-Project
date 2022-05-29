from cgitb import text
from email.mime import image
from unicodedata import name
import streamlit as st  #pip install streamlit
from PIL import Image

import pickle
from pathlib import Path

import pandas as pd
import requests

import streamlit_authenticator as stauth  #pip install streamlit-authenticator

#---To simply run the app--
#COMMAND: streamlit run application.py

#----Change Default App Name and Icon----
img = Image.open('movies_icon.jpg')
st.set_page_config(page_title="Movie Recommendation Engine", page_icon=img, layout="wide")

#----Hide by-default main menu and footer in app----
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

#----GIVING TITLE----
st.title('Movie Recommendation Engine')

#----USER AUTHENTICATION----
names = ["User1", "User2"]
usernames = ["u1", "u2"]

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "Movie Recommendation Engine", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.error("Please enter your username and password")

if authentication_status:
    #----MAIN CODE---
    movies_dict = pickle.load(open('movies.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    similarity = pickle.load(open('similarity.pkl', 'rb'))

    selected_mov_name = st.selectbox(
        'Choose your favourite movie',
        movies['title'].values)

    #---Fxn to fetch trailer of movie---
    def fetch_trailer_of_movie(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}/videos?api_key=b854a1a1d67e004f486398fcbe0e8473&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        for row in data['results']:
            return "https://www.youtube.com/watch?v=" + row['key']

    #---Fxn to store movies and their trailers to be recommended---
    def recommend(movie):
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]

        recommended_mov =[]
        recommended_mov_pos =[]
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
         
            recommended_mov.append(movies.iloc[i[0]].title)       
            recommended_mov_pos.append(fetch_trailer_of_movie(movie_id))
     
        return recommended_mov, recommended_mov_pos

    #---Show the recommendations along with trailers---
    if st.button('Show Recommendation'):
        recommended_movie_names,recommended_movie_posters = recommend(selected_mov_name)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_movie_names[0])
            st.video(recommended_movie_posters[0], format="video/mp4", start_time=0)

        with col2:
            st.text(recommended_movie_names[1])
            st.video(recommended_movie_posters[1], format="video/mp4", start_time=0)

        with col3:
            st.text(recommended_movie_names[2])
            st.video(recommended_movie_posters[2], format="video/mp4", start_time=0)
        with col4:
            st.text(recommended_movie_names[3])
            st.video(recommended_movie_posters[3], format="video/mp4", start_time=0)
        with col5:
            st.text(recommended_movie_names[4])
            st.video(recommended_movie_posters[4], format="video/mp4", start_time=0)

    #---SIDEBAR---
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")