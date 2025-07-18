import streamlit as st
from PIL import Image
import pickle
import pandas as pd
import requests
import time


st.set_page_config(layout="wide")


movies_title = pd.DataFrame(pickle.load(open("movie_dict1.pkl", 'rb')))
similarity_title = pickle.load(open("similarity1.pkl", 'rb'))

movies_genre = pd.DataFrame(pickle.load(open("movie_dict2.pkl", 'rb')))
similarity_genre = pickle.load(open("similarity2.pkl", 'rb'))




def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')
    except:
        return "https://via.placeholder.com/500"


def recommend(movie, movies_df, similarity_matrix, feature_col='title'):
    try:
        movie_index = movies_df[movies_df[feature_col] == movie].index[0]
        distances = similarity_matrix[movie_index]
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:8]
        names = []
        posters = []
        for i in movie_list:
            movie_id = movies_df.iloc[i[0]].get('movie_id', None)
            names.append(movies_df.iloc[i[0]][feature_col])
            posters.append(fetch_poster(movie_id))
        return names, posters
    except:
        return [], []


st.markdown("""<style>body { background-color: black; color: white; }</style>""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
        <div style='text-align:center; background-position: center;'>
            <p style='font-size:20px;'>Ready to watch? Enter your email to create or restart your membership.</p>
        </div>
    """, unsafe_allow_html=True)


tabs = st.tabs(["Recommend by Title", "Recommend by Genre"])


with tabs[0]:
    st.header("🎬 Recommend Movies by Title")
    movie = st.selectbox("Choose a movie title", movies_title['title'].values)
    if st.button("Recommend", key="title_btn"):
        names, posters = recommend(movie, movies_title, similarity_title, 'title')
        if names:
            cols = st.columns(7)
            for i, col in enumerate(cols):
                with col:
                    st.text(names[i])
                    st.image(posters[i])
        else:
            st.warning("No recommendations found.")


with tabs[1]:
    st.header("🎭 Recommend Movies by Genre")
    genre = st.selectbox("Choose a genre", movies_genre['genres'].unique())
    if st.button("Recommend", key="genre_btn"):
        names, posters = recommend(genre, movies_genre, similarity_genre, 'genres')
        if names:
            cols = st.columns(7)
            for i, col in enumerate(cols):
                with col:
                    st.text(names[i])
                    st.image(posters[i])
        else:
            st.warning("No recommendations found.")

