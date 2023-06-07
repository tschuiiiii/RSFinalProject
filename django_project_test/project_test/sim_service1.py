from . import movie_metadata

class SimilarityService1:

    def calculate_plot_sim_by_tf_idf(self):
        for data in movie_metadata.metadata:
            print(data)