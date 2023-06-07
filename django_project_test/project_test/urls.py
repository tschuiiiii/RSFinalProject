from django.urls import path

from . import views

app_name = "project_test"
urlpatterns = [
    path("", views.index, name="index"),
    path("/search", views.search, name="search"),
    path("/similarmovies/<int:movie_id>", views.similarmovies, name="similarmovies"),
    path("/<int:movie_id>/poster", views.poster, name="poster")
]
