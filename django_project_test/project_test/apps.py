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
        if os.environ.get('RUN_MAIN'):
            print('Start extracting json-file.')
            if exists('movie-metadata.npy'):
                movie_metadata.metadata = numpy.load('movie-metadata.npy', allow_pickle=True)
            else:
                for json_file_name in os.listdir('./extracted_content_ml-latest'):
                    with open(os.path.join('./extracted_content_ml-latest', json_file_name), encoding='utf-8') as json_file:
                        movie_metadata.metadata.append(json.load(json_file))
                numpy.save('movie-metadata.npy', movie_metadata.metadata)
            print('Finished json-file!')

            print('Start reading csv-file')
            try:
                movie_metadata.movies_df = pd.read_csv('./ml-latest-small/movies.csv', low_memory=False)
            except FileNotFoundError:
                print('File ./ml-latest-small/movies.csv does not exist')
                sys.exit()
            print('Finished csv-file!')
