import os
import random
from os.path import exists

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import movie_metadata
from .Main import Main

import re
import requests
import csv


# Create your views here.
def index(request):
    good_rated_movies = []

    for movie_object in movie_metadata.metadata:
    #for movie_object in movie_metadata.movies_df:
        movie = movie_object['movielens']
        movie_id = movie_object['movielensId']

        if movie['avgRating'] >= 4:

            good_rated_movies.append({
                'id': movie_id,
                'title': movie['title'],
                'genres': movie['genres'],
                'avgRating': round(movie['avgRating'], 1),
                'numRatings': movie['numRatings']
            })

    random_movies = random.choices(good_rated_movies, k=6)

    if request.method == "GET":
        return render(
            request,
            "index.html",
            {
                #'movies_title': movies_title,
                'random_movies': random_movies
            }
        )


def search(request):
    query = request.GET.get('q', '')

    if query is '':
        return JsonResponse([], safe=False)

    movie_results = []

    for movie_object in movie_metadata.metadata:
        movie = movie_object['movielens']
        movie_genres = ""

        for genre in movie['genres']:
            movie_genres += genre + ' | '

        if re.search(query, movie['title'], re.IGNORECASE):
            movie_results.append({
                'id': movie_object['movielensId'],
                'title': movie['title'],
                'genres': movie_genres[:-2],
                'avgRating': round(movie['avgRating'], 1),
                'numRatings': movie['numRatings']
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
    movie_title = movie_metadata.movies_df[movie_metadata.movies_df['movieId'] == movie_id]['title'].values[0]

    main_obj = Main()
    results = main_obj.title(movie_title)
    #recom = obj.title("Men in Black (a.k.a. MIB) (1997)")

    # {movieId : {title, genres, avgRating, numRatings}}
    result_dict = {}

    for result_key, result_titles in results.items():
        result_dict[result_key] = {}
        for title in result_titles:
            result_mid = int(movie_metadata.movies_df[movie_metadata.movies_df['title'] == title]['movieId'].values[0])
            result_dict[result_key][result_mid] = {'title': title}

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

        for key, value_dict in result_dict.items():
            if movie_object['movielensId'] in value_dict:
                movie = movie_object['movielens']

                value_dict[movie_object['movielensId']].update({
                    'genres': movie['genres'],
                    'avgRating': round(movie['avgRating'], 1),
                    'numRatings': movie['numRatings']
                })


        # elif movie_object['movielensId'] in result_dict:
        #     movie = movie_object['movielens']
        #
        #     result_dict[movie_object['movielensId']].update({
        #         'genres' : movie['genres'],
        #         'avgRating' : round(movie['avgRating'], 1),
        #         'numRatings' : movie['numRatings']
        #     })


    return render(
        request,
        "details.html",
        {
            'movie': movie_details,
            'result_dict': result_dict
        }
    )
