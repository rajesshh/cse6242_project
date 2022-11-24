import pandas as pd
import streamlit as st  # pip install streamlit
import subprocess
from streamlit import session_state as ss
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import matplotlib.pyplot as plt
import time
import requests

movies_list = pd.read_csv(r'C:\Users\rajes\Documents\Masters\CSE6242\pythonProject\content_similar_movies.csv')

genres = pd.read_csv(r'C:\Users\rajes\Documents\Masters\CSE6242\pythonProject\genres.csv')

actors = pd.read_csv(r'C:\Users\rajes\Documents\Masters\CSE6242\pythonProject\actors.csv')

directors = pd.read_csv(r'C:\Users\rajes\Documents\Masters\CSE6242\pythonProject\directors.csv')

movies = pd.read_csv(r'C:\Users\rajes\Documents\Masters\CSE6242\pythonProject\df_cleaned_nov_19.csv',
                     lineterminator='\n')


def recommend(movie):
    similar_movies = pd.DataFrame()
    if movie in movies_list.values:
        similar_movies = movies_list[movies_list['title'] == movie]

        similar_movies_title = similar_movies[
            ['title1', 'title2', 'title3', 'title4', 'title5', 'title6', 'title7', 'title8', 'title9',
             'title10']].transpose().reset_index(drop=True)
        similar_movies_movie_id = similar_movies[
            ['movie_id1', 'movie_id2', 'movie_id3', 'movie_id4', 'movie_id5', 'movie_id6', 'movie_id7', 'movie_id8',
             'movie_id9', 'movie_id10']].transpose().reset_index(drop=True)
        similar_movies = pd.concat([similar_movies_title, similar_movies_movie_id], axis=1)

        similar_movies.columns = ['Recommended Movies', 'movie_id']
        similar_movies = similar_movies.reset_index(drop=True)
        return similar_movies


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=7fdd0dc4b29fd64f6fa280c798f90eda&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

#################################################################################
def set_stage(stage):
    st.session_state.stage = stage

###################################################################################
def movie_name(selected_movie_name):
    if (selected_movie_name != '<select>'):
        recommendations = recommend(selected_movie_name)
        global recommended_movies
        recommended_movies= []
        global recommended_movie_posters
        recommended_movie_posters = []
        for index, row in recommendations.iterrows():
            title = row['Recommended Movies']
            movie_id = row['movie_id']
            recommended_movies.append(title)
            recommended_movie_posters.append(fetch_poster(movie_id))

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            # st.text(recommended_movies[0])
            st.image(recommended_movie_posters[0])
            st.button(recommended_movies[0], on_click=set_stage, args=(2,), key=recommended_movies[0])

        with col2:
            # st.text(recommended_movies[1])
            st.image(recommended_movie_posters[1])
            st.button(recommended_movies[1], on_click=set_stage, args=(3,),key=recommended_movies[1])

        with col3:
            # st.text(recommended_movies[2])
            st.image(recommended_movie_posters[2])
            st.button(recommended_movies[2], on_click=set_stage, args=(4,),key=recommended_movies[2])

        with col4:
            # st.text(recommended_movies[3])
            st.image(recommended_movie_posters[3])
            st.button(recommended_movies[3], on_click=set_stage, args=(5,),key=recommended_movies[3])

        with col5:
            # st.text(recommended_movies[4])
            st.image(recommended_movie_posters[4])
            st.button(recommended_movies[4], on_click=set_stage, args=(6,),key=recommended_movies[4])


        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            # st.text(recommended_movies[5])
            st.image(recommended_movie_posters[5])
            st.button(recommended_movies[5], on_click=set_stage, args=(7,),key=recommended_movies[5])

        with col2:
            # st.text(recommended_movies[6])
            st.image(recommended_movie_posters[6])
            st.button(recommended_movies[6], on_click=set_stage, args=(8,),key=recommended_movies[6])

        with col3:
            # st.text(recommended_movies[7])
            st.image(recommended_movie_posters[7])
            st.button(recommended_movies[7], on_click=set_stage, args=(9,),key=recommended_movies[7])

        with col4:
            # st.text(recommended_movies[8])
            st.image(recommended_movie_posters[8])
            st.button(recommended_movies[8], on_click=set_stage, args=(10,),key=recommended_movies[8])

        with col5:
            # st.text(recommended_movies[9])
            st.image(recommended_movie_posters[9])
            st.button(recommended_movies[9], on_click=set_stage, args=(11,),key=recommended_movies[9])

    else:
        st.error('Please input valid Movie name.')
    return recommended_movies

##################################################################################
###  Functions Definition Ends #####################################################
##################################################################################

st.title('Movie Recommender System')
# @st.cache
select_list = ['<select>']
any_list = ['Any']
movie_list = movies_list['title'].values.tolist()
movie_list = select_list + movie_list

directors['director']= directors['director'].unique()
director_list = directors['director'].values.tolist()
director_list = select_list + director_list
genre_list = genres['genre'].values.tolist()
genre_list = select_list + any_list + genre_list

actors['actor'] = actors['actor'].unique()
actor_list = actors['actor'].values.tolist()
actor_list = select_list + actor_list

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list)

# Capture Inputs from left hand side bar.
st.sidebar.header("Please select your criteria here:")
st_actor = st.sidebar.selectbox("Actor", actor_list)
st_director = st.sidebar.selectbox("Director", director_list)
st_genre = st.sidebar.selectbox("Genre", genre_list)
st_run_time = st.sidebar.selectbox('Run Time of Movie', ['<select>', 'Any', '0-60', '61-120', '121-180', '181+'])
st_click = st.sidebar.button('Show my recommendations')

st_actor = 'Samuel L. Jackson'
# Logic for Filter  - Side bar
if st_genre == 'Any':
    if st_run_time == '0-60':
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & (
                        movies['runtime'] <= 60)]
    elif st_run_time == '61-120':
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & (
                        movies['runtime'] > 60) & (movies['runtime'] <= 120)]
    elif st_run_time == '121-180':
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & (
                        movies['runtime'] > 120) & (movies['runtime'] <= 180)]
    elif st_run_time == '180+':
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & (
                        movies['runtime'] >= 180)]
    else:
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor)]
else:
    if st_run_time == '0-60':
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & movies[
                'genres'].str.contains(st_genre) & (movies['runtime'] <= 60)]
    elif st_run_time == '61-120':
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & movies[
                'genres'].str.contains(st_genre) & (movies['runtime'] > 60) & (movies['runtime'] <= 120)]
    elif st_run_time == '121-180':
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & movies[
                'genres'].str.contains(st_genre) & (movies['runtime'] > 120) & (movies['runtime'] <= 180)]
    elif st_run_time == '180+':
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & movies[
                'genres'].str.contains(st_genre) & (movies['runtime'] >= 180)]
    else:
        movies_filter = movies.loc[
            movies['directors'].str.contains(st_director) & movies['actors'].str.contains(st_actor) & movies[
                'genres'].str.contains(st_genre)]

movies_filter = movies_filter[['title_tmdb', 'tmdbId', 'vote_count', 'vote_average', 'popularity']].sort_values(
    'popularity', ascending=False)
movies_filter = movies_filter[['title_tmdb', 'tmdbId']].head(10)
movies_filter.columns = ['Recommended Movies', 'movie_id']
movies_filter = movies_filter.reset_index(drop=True)

# Filter Attributes
if st_click:
    if (st_actor != '<select>') and (st_director != '<select>') and (st_genre != '<select>') and (
            st_run_time != '<select>'):
        st_columns = movies_filter.shape[0]
        if st_columns >= 1:
            recommended_movies = []
            recommended_movie_posters = []
            for index, row in movies_filter.iterrows():
                title = row['Recommended Movies']
                movie_id = row['movie_id']
                recommended_movies.append(title)
                recommended_movie_posters.append(fetch_poster(movie_id))
            cols = st.columns(st_columns, gap="small")
            wcol = 5
            for i in range(st_columns):
                col = cols[i % wcol]
                with col:
                    # st.text(recommended_movies[i])
                    st.image(recommended_movie_posters[i], caption=recommended_movies[i])
        else:
            st.sidebar.error('No movie matched, please try with different attributes.')

    else:
        st.sidebar.error('Please input all the attributes.')



# Main Content
if "stage" not in st.session_state:
    st.session_state.stage = 0

st.button('Show Recommendations', on_click=set_stage, args=(1,))
if st.session_state.stage > 0:
    recommended_movies=movie_name(selected_movie_name)
    # movie1=recommended_movies[0]
    # st.write(movie1)


if st.session_state["stage"] == 2:
    st.write("Hello")
    st.write(recommended_movies[0])
    movie_name(recommended_movies[0])

if st.session_state["stage"] == 3:
    st.write("Hello")
    st.write(recommended_movies[1])
    movie_name(recommended_movies[1])

if st.session_state["stage"] == 4:
    st.write("Hello")
    st.write(recommended_movies[2])
    movie_name(recommended_movies[2])

if st.session_state["stage"] == 5:
    st.write("Hello")
    st.write(recommended_movies[3])
    movie_name(recommended_movies[3])

if st.session_state["stage"] == 6:
    st.write("Hello")
    st.write(recommended_movies[4])
    movie_name(recommended_movies[4])

if st.session_state["stage"] == 7:
    st.write("Hello")
    st.write(recommended_movies[5])
    movie_name(recommended_movies[5])

if st.session_state["stage"] == 8:
    st.write("Hello")
    st.write(recommended_movies[6])
    movie_name(recommended_movies[6])

if st.session_state["stage"] == 9:
    st.write("Hello")
    st.write(recommended_movies[7])
    movie_name(recommended_movies[7])

if st.session_state["stage"] == 10:
    st.write("Hello")
    st.write(recommended_movies[8])
    movie_name(recommended_movies[8])

if st.session_state["stage"] == 11:
    st.write("Hello")
    st.write(recommended_movies[9])
    movie_name(recommended_movies[9])