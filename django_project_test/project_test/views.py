import random
from os.path import exists

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from . import movie_metadata
from .WebsiteRecommendations import recommendations

import re
import requests

lookup_dict = {
    'project_test/similarity/func2_Reviews': 'The recommendations of TF-IDF model based on movies\' reviews',
    'project_test/similarity/func3_Others': 'The recommendations of TF-IDF model based on movies\' titles, keywords and other information',
    'project_test/similarity/func4_DL-Summary': 'The recommendations by Glove embedding based on movies\' summary',
    'project_test/similarity/func8_BERT-Review': 'The recommendations of BERT model based on movies\' reviews',
    'project_test/similarity/func9_BERT-Summary-Reviews': 'The recommendations of BERT model based on movies\' titles, keywords and other information'
    }


def style_genres(genres):
    separated_genres = genres.replace(" ", ", ")
    styled_genres = re.sub('(^|[,])\s*([a-zA-Z])', lambda p: p.group(0).upper(), separated_genres)
    return styled_genres


# Create your views here.
def index(request):
    good_rated_movies = []
    cookies_set = {}
    cookies_empty = True

    if 'genres' in request.COOKIES:
        cleaned_cookies = re.sub(r"['\[\]\s+]", "", request.COOKIES['genres'])
        if cleaned_cookies == "":
            welcome_recomm_title = "Top rated movies"
        else:
            cookies_set = set((cleaned_cookies.lower()).split(","))
            cookies_empty = False
            welcome_recomm_title = "Prefered genres"
    else:
        return redirect(
        '/project_test/personal'
    )

    for movie_object in movie_metadata.movies_df.iterrows():
        movie = movie_object[1]
        movie_id = movie['Id']

        genres_set = set((movie['genres'].lower()).split(" "))

        if not cookies_empty and len(cookies_set.intersection(genres_set)) > 0:
            if movie['rating'] >= 4:
                good_rated_movies.append({
                    'id': movie_id,
                    'title': movie['title'],
                    'genres': style_genres(movie['genres']),
                    'avgRating': round(movie['rating'], 1)
                })
        elif cookies_empty:
            if movie['rating'] >= 4:
                movie_genres = movie['genres'].replace("|", ", ")

                good_rated_movies.append({
                    'id': movie_id,
                    'title': movie['title'],
                    'genres': movie_genres,
                    'avgRating': round(movie['rating'], 1)
                })

    random_movies = random.choices(good_rated_movies, k=6)

    if request.method == "GET":
        return render(
            request,
            "index.html",
            {
                #'movies_title': movies_title,
                'random_movies': random_movies,
                'welcome_recomm_title': welcome_recomm_title
            }
        )


def search(request):
    query = request.GET.get('q', '')

    if query == '':
        return JsonResponse([], safe=False)

    movie_results = []

    for movie_object in movie_metadata.movies_df.iterrows():
        movie = movie_object[1]

        if re.search(query, movie['title'], re.IGNORECASE):
            movie_results.append({
                'id': movie['Id'],
                'title': movie['title'],
                'genres': style_genres(movie['genres']),
                'avgRating': round(movie['rating'], 1),
                # todo?
                #'numRatings': movie['numRatings']
            })

        if len(movie_results) >= 10:
            break

    return JsonResponse(movie_results, safe=False)


def poster(request, movie_id):
    """
    Get poster to movie by id.
    First check MLP-20M folder, if image already exits.
    Second check if poster exists via poster path from tmdb site.
    Third take a default image.
    :param request:
    :param movie_id: Movie id for which the poster is needed
    :return: return HttpResponse image as file
    """
    poster_path = ''

    if exists(f'project_test/static/media/MLP-20M/{movie_id}.jpg'):
        with open(f'project_test/static/media/MLP-20M/{movie_id}.jpg', 'rb') as file:
            response = HttpResponse(file.read(), content_type="image/jpeg")
            response['Content-Disposition'] = 'inline;'
            return response

    for movie in movie_metadata.metadata:
        if movie['movielensId'] == movie_id:
            poster_path = movie['movielens']['posterPath']
            break

    tmdb_response = requests.get(f'https://image.tmdb.org/t/p/original{poster_path}',timeout=None)

    if tmdb_response.status_code == 200:
        response = HttpResponse(tmdb_response.content, content_type=tmdb_response.headers['Content-Type'])
        response['Content-Disposition'] = 'inline;'
        return response
    else:
        with open(f'project_test/static/media/default.jpg', 'rb') as file:
            response = HttpResponse(file.read(), content_type="image/jpeg")
            response['Content-Disposition'] = 'inline;'
            return response


def similarmovies(request, movie_id):
    movie_title = movie_metadata.movies_df[movie_metadata.movies_df['Id'] == movie_id]['title'].values[0]
    recom = recommendations(movie_title)

    recommendation = dict()
    for function, movies in recom.items():
        recommendation[function] = dict()
        for movie in movies:
            id = movie_metadata.movies_df.loc[movie_metadata.movies_df['title'] == movie, 'Id'].iloc[0]
            m_genres = movie_metadata.movies_df.loc[movie_metadata.movies_df['title'] == movie, 'genres'].iloc[0]

            movie_info = {'title': movie,
                          'genres': style_genres(m_genres),
                          'avgRating': round(
                              movie_metadata.movies_df.loc[movie_metadata.movies_df['title'] == movie, 'rating'].iloc[
                                  0], 1)}
            recommendation[function][id] = movie_info

    for movie_object in movie_metadata.metadata:
        if movie_object['movielensId'] == movie_id:
            movie = movie_object['movielens']

            movie_details = {
                'adult': movie_object['tmdb']['adult'],
                'avgRating': round(movie['avgRating'], 1),
                'cast': (', ').join(movie['actors'][:11]),
                'country': movie_object['imdb']['country'],
                'directors': (', ').join(movie['directors']),
                'genres': movie['genres'],
                'id': movie_id,
                'languages': (', ').join(movie['languages']),
                'numRatings': movie['numRatings'],
                'plotSummary': movie['plotSummary'],
                'releaseYear': movie['releaseYear'],
                'reviews': movie_object['imdb']['reviews'],
                'runtimeHours': int(movie['runtime'] / 60),
                'runtimeMinutes': movie['runtime'] % 60,
                'title': movie['title']
            }

    return render(
        request,
        "details.html",
        {
            'movie': movie_details,
            'result_dict': recommendation,
            'lookup_dict': lookup_dict
        }
    )


def personal(request):
    all_movie_genres = {}

    for movie_object in movie_metadata.movies_df.iterrows():
        movie = movie_object[1]
        movie_genres = movie['genres'].split(" ")

        for genre in movie_genres:
            if not genre in all_movie_genres:
                cap_genre = genre.capitalize()
                all_movie_genres[cap_genre] = False

    my_keys = list(all_movie_genres.keys())
    my_keys.sort()
    all_movie_genres = {i: all_movie_genres[i] for i in my_keys}

    if 'genres' in request.COOKIES:
        cleaned_cookies = re.sub(r"['\[\]\s+]", "", request.COOKIES['genres'])
        cookies_list = cleaned_cookies.split(",")
        if not cleaned_cookies == "":
            for genre in cookies_list:
                all_movie_genres[genre] = True

    return render(
        request,
        "personal.html",
        {
            'genres': all_movie_genres
        }
    )


def change_preferences(request):
    selected_values = request.POST.getlist('genre')

    response = redirect(
        '/project_test'
    )
    response.set_cookie('genres', selected_values)
    return response

