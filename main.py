import streamlit as st
import numpy as np
import pandas as pd
import pickle
import requests
import os

API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data["poster_path"]


def recommend(movie):
  movie_index=movies[movies['title']==movie].index[0]
  distances=similarity[movie_index]
  movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  recommended_movies=[]
  recommended_movie_poster=[]

  for i in movie_list:
    movie_id=movies.iloc[i[0]].movie_id    #iloc use to fetch data of that row
    recommended_movies.append(movies.iloc[i[0]].title)    #i[0]->movie index
    recommended_movie_poster.append(fetch_poster(movie_id))
  return recommended_movies,recommended_movie_poster


movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommnedation System")
selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names,posters=recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.markdown(
                f"""
                <p style="
                    font-size:13px;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    text-align: center;
                " title="{names[i]}">
                    {names[i]}
                </p>
                """,
                unsafe_allow_html=True
            )
