from os.path import exists

import numpy
from django.apps import AppConfig

import os, json, sys
import pandas as pd
from . import movie_metadata


class ProjectTestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_test'

    def ready(self):
        '''
        TODO: Comment
        :return:
        '''

        print('Start extracting json-file.')
        if exists('movie-metadata.npy'):
            movie_metadata.metadata = numpy.load('movie-metadata.npy', allow_pickle=True)
        else:
            for json_file_name in os.listdir('./extracted_content_ml-latest'):
                with open(os.path.join('./extracted_content_ml-latest', json_file_name), encoding='utf-8') as json_file:
                    movie_metadata.metadata.append(json.load(json_file))
            numpy.save('movie-metadata.npy', movie_metadata.metadata)
        print('Finished json-file!')

        print('Start reading txt-file')
        try:
            # movie_metadata.movies_df = pd.read_csv('project_test/movies.csv', low_memory=False)
            # TODO: sample dataset of Faisal
            movie_metadata.movies_df = pd.read_csv("project_test/FinalVersion.txt", sep="\t")
        except FileNotFoundError:
            # print('File project_test/movies.csv does not exist')
            print('File project_test/FinalVersion.txt does not exist')
            sys.exit()
        print('Finished txt-file!')
