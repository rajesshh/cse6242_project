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

actors = pd.read_csv(r'C:\Users\rajes\Documents\Masters\CSE6242\pythonProject\actors2_list_df.csv')

directors = pd.read_csv(r'C:\Users\rajes\Documents\Masters\CSE6242\pythonProject\directors.csv')

movies = pd.read_csv(r'C:\Users\rajes\Documents\Masters\CSE6242\pythonProject\df_cleaned_v2_nov25.csv',  lineterminator='\n')

@st.cache
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
    if poster_path is None:
        poster_path="/bBRcYbUt4IYzibiPxqylv49GcgU.jpg"
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

#################################################################################
def set_stage(stage):
    st.session_state.stage = 0
    clear()
    clear_side()
    st.session_state.sidebar_stage = None
    st.session_state.stage = stage

def set_sidebar_stage(sidebar_stage):
    st.session_state.sidebar_stage = 0
    clear_side()
    clear()
    st.session_state.stage  = None
    st.session_state.sidebar_stage = sidebar_stage

# New callback for the individual movie buttons
def selected(i):
    st.session_state.selected = 0
    st.session_state.selected = i
    # st.session_state.sidebar_stage = None
    # clear_side()


def side_selected(i):
    st.session_state.side_selected = 0
    st.session_state.side_selected = i
    st.session_state.stage = None
    clear()



def clear():
    st.session_state.selected = None

def clear_side():
    st.session_state.side_selected = None


###################################################################################
def movie_name(selected_movie_name, key):
    global recommended_movies
    recommended_movies= []
    global recommended_movie_posters
    recommended_movie_posters = []
    if (selected_movie_name != '<select>'):
        recommendations = recommend(selected_movie_name)

        for index, row in recommendations.iterrows():
            title = row['Recommended Movies']
            movie_id = row['movie_id']
            recommended_movies.append(title)
            recommended_movie_posters.append(fetch_poster(movie_id))
        st_columns=recommendations.shape[0]
        #columns=st.columns(st_columns,  gap="small")
        columns = st.columns(5)
        wcol=5
        for i in range(10):
            with columns[i%5]:
            # st.text(recommended_movies[i])
                st.image(recommended_movie_posters[i])
             # now the individual movie buttons affect the 'selected' key instead of the 'stage' key
                key1 = recommended_movies[i]+ key
                st.button(recommended_movies[i], on_click=selected, args=(i,), key=key1)
        return recommended_movies , recommended_movie_posters
    else:
        st.error('Please input valid Movie name.')
        return recommended_movies , recommended_movie_posters

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

# Logic for Filter  - Side bar
if st_genre == 'Any':
    if st_run_time == '0-60':
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & (
                        movies['runtime'] <= 60)]
    elif st_run_time == '61-120':
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & (
                        movies['runtime'] > 60) & (movies['runtime'] <= 120)]
    elif st_run_time == '121-180':
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & (
                        movies['runtime'] > 120) & (movies['runtime'] <= 180)]
    elif st_run_time == '180+':
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & (
                        movies['runtime'] >= 180)]
    else:
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor)]
else:
    if st_run_time == '0-60':
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & movies[
                'genres_tmdb'].str.contains(st_genre) & (movies['runtime'] <= 60)]
    elif st_run_time == '61-120':
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & movies[
                'genres_tmdb'].str.contains(st_genre) & (movies['runtime'] > 60) & (movies['runtime'] <= 120)]
    elif st_run_time == '121-180':
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & movies[
                'genres_tmdb'].str.contains(st_genre) & (movies['runtime'] > 120) & (movies['runtime'] <= 180)]
    elif st_run_time == '180+':
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & movies[
                'genres_tmdb'].str.contains(st_genre) & (movies['runtime'] >= 180)]
    else:
        movies_filter = movies.loc[
            movies['directors_1'].str.contains(st_director) & movies['actors_2'].str.contains(st_actor) & movies['actors_1'].str.contains(st_actor) & movies[
                'genres_tmdb'].str.contains(st_genre)]

movies_filter = movies_filter[['title_tmdb', 'tmdbId',  'vote_average']].sort_values('vote_average', ascending=False)
movies_filter = movies_filter[['title_tmdb', 'tmdbId']].head(10)
movies_filter.columns = ['Recommended Movies', 'movie_id']
movies_filter = movies_filter.reset_index(drop=True)


# SideBar Logic

if "sidebar_stage" not in st.session_state:
    st.session_state.sidebar_stage = 0

# Filter Attributes
st.sidebar.button('Show my Recommendations',on_click=set_sidebar_stage, args=(1,))
if st.session_state.sidebar_stage == 1:
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
                    st.image(recommended_movie_posters[i])
                    key='first'
                    key1 = recommended_movies[i]+ key
                    st.button(recommended_movies[i],on_click=side_selected, args=(i,),key=key1)
        else:
            st.sidebar.error('No movie matched, please try with different attributes.')

    else:
        st.sidebar.error('Please input all the attributes.')


# initialize a new key
if 'side_selected' not in st.session_state:
    st.session_state.side_selected = None

if st.session_state.side_selected  is not None:
    # st.session_state.stage = 0
    i = st.session_state.side_selected
    st.write ("Hello1")
    st.write("Movies similar to movie " + recommended_movies[i])
    movie_name(recommended_movies[i],'second')


 ############# side bar logic ends ########################

###############################################
# Main content Logic
###############################################
if "stage" not in st.session_state:
    st.session_state.stage = 0

st.button('Show Recommendations', on_click=set_stage, args=(1,))
if st.session_state.stage == 1:
    recommended_movies, recommended_movie_posters =movie_name(selected_movie_name,'first')

# initialize a new key
if 'selected' not in st.session_state:
    st.session_state.selected = None

if st.session_state.selected  is not None:
    # st.session_state.stage = 0
    i = st.session_state.selected
    st.write ("Hello")
    st.write("Movies similar to movie " + recommended_movies[i])


    movie_name(recommended_movies[i],'second')


#############  side bar logic ends ########################