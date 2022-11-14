import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity ,euclidean_distances
import time

movies = pd.read_csv(r'C:\Users\rajes\Google Drive\Masters\CSE6242 - Data and Visual Analytics\Projects\movie_rec_filtered.csv',lineterminator='\n')
# movies = movies1.iloc[:4000,:]

# #######################################
####### Functions Definition  ###########
##########################################

# Returns the list top 3 elements or entire list
def get_list(x):
    x = str(x).split("|")
    if isinstance (x, list):
        # names = [i for i in x]

        if len(x) > 5:
            x =  x[:5]
        return x
    #Return empty list in case there is no data
    return []
############################################################
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace( " ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

#############################################################
def movie_recommender(title_tmdb, cosine_sim):
    if title_tmdb in movies_list.values :
        idx = indices[title_tmdb]

        sim_scores= list(enumerate(cosine_sim[idx]))

        sim_scores =sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores_as_df = pd.DataFrame(sim_scores, columns=['index','sim_score'])
        movies_final = movies_list.merge(sim_scores_as_df, how='left', left_on='index_col', right_on='index')
        movies_final = movies_final.sort_values('sim_score', ascending=False)
        similar_movies = movies_final[['title_tmdb', 'sim_score','score']].head(11).tail(10)
        print( "Here is the list of Top 10 movies, similar to Title \"" + title_tmdb + "\"")

        print(tabulate(similar_movies, headers = 'keys', tablefmt = 'fancy_grid', showindex=False))
        # title_tmdb = similar_movies.style.hide_index()
        return similar_movies

    else:
        print ("Movie \"" + title_tmdb + "\" in not present in our database, please search for another movie")

############################################################

def create_combine_overview(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['actors']) +  ' ' + ' '  .join(x['directors']) + ' ' + str(x['overview']) +  ' ' + ' '.join(x['genres'] )

#############################################################
# quartile 90 for getting which  got votes more than 90%
# value of m can be change depending on requirement
# m=movies['vote_count'].quantile(0.9)
m =1
C=movies['vote_average'].mean()


def weighted_rating(x, m=m, C=C):
    v=x['vote_count']
    R=x['vote_average']
    # calculation done using  IMDB formula
    return (v/(v+m) * R) + (m/(m+v) *C)

# Calcualting cosine_similarity in batches
def cosine_similarity_n_space(m1, m2, batch_size=50):
    assert m1.shape[1] == m2.shape[1]
    ret = np.ndarray((m1.shape[0], m2.shape[0]))
    for row_i in range(0, int(m1.shape[0] / batch_size) + 1):
        start = row_i * batch_size
        end = min([(row_i + 1) * batch_size, m1.shape[0]])
        if end <= start:
            break # cause I'm too lazy to elegantly handle edge cases
        rows = m1[start: end]
        sim = cosine_similarity(rows, m2) # rows is O(1) size
        ret[start: end] = sim
    return ret


###############################################################
 ######### Functions Ends
##############################################################
# Get the Top 3 elements from cast, genres and Keywords attribute
features = ['actors', 'keywords' , 'genres', 'directors']
for feature in features:
    movies[feature] = movies[feature].apply(get_list)


for feature in features:
        movies[feature] =  movies[feature].apply(clean_data)

# Replacing NaN with empty string
movies['overview'] = movies['overview'].fillna('')


movies['combine_overview'] =movies.apply(create_combine_overview, axis=1)

movies[['title_tmdb', 'actors', 'directors', 'genres', 'keywords', 'combine_overview']].head()


### ############################################################################
#  Calculating Score using IMDB’s weighted rating formulae
###############################################################################
# getting only the movies which vote_count greater than m
movies_list =  movies.copy().loc[movies['vote_count']>=m]

# Applying Score
movies_list['score']= movies_list.apply(weighted_rating, axis=1)

# Sorting the movies as per score
movies_list = movies_list.sort_values('score', ascending=False)

# Creating a reverse map of indices and movie title_tmdb
movies_list = movies_list.reset_index()
indices = pd.Series(movies_list.index, index=movies_list['title_tmdb']).drop_duplicates()
movies_list['index_col'] = movies_list.index

###################################################################
#  Defining a TF-IDF vectorizer object and Removing all stop words
###################################################################
tfidf = TfidfVectorizer(stop_words='english')

# Making the TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(movies_list['combine_overview'])

print("tfidf_matrix", tfidf_matrix.shape)

# Calculating the Cosine Similarity matrix
# # Calculating the Cosine Similarity matrix
start = time.time()
cosine_sim =cosine_similarity_n_space(tfidf_matrix, tfidf_matrix, batch_size=100)
print("Time taken: %s seconds" %(time.time() - start))

###################################################################
#  Defining a Count vectorizer object and Removing all stop words
###################################################################

# count = CountVectorizer(stop_words='english')
# count_matrix = count.fit_transform(movies_list['combine_overview'])
#
# # compute the Cosine Similiarity matrix based on the count_matrix
# cosine_sim2  = cosine_similarity(count_matrix, count_matrix)


# Movie Recommender Function
# movie_recommender('Toy Story (1995)',cosine_sim)

movie_keywords = {'title_tmdb': ['Toy Story','Jumanji'] }

df = pd.DataFrame(movie_keywords, columns = ['title_tmdb'])
for index, row in df.iterrows():
    globals()[f"df_content_movie_{index}"]= movie_recommender(row['title_tmdb'],cosine_sim)

print (df_content_movie_0)
print (df_content_movie_1)