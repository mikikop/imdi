from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'films', views.FilmViewSet)
router.register(r'directors', views.DirectorViewSet)

urlpatterns = [
    path('homepage', views.home, name='home'),
    path('add_director/', views.AddDirector.as_view(), name='add-director'),
    path('add_film', views.add_film, name='add-film'),
    path('add_from_imdb/<int:id>', views.add_from_imdb, name='add_from_imdb'),
    path('search_imdb', views.search_imdb, name='search-imdb'),
    path('detail_imdb/<int:id>', views.detail_imdb, name='detail_imdb'),
    path('films_results', views.films_results, name='films-results'),
    path('film_results/delete/<int:id>', views.delete_film, name='delete_film'),
    path('film/vote/', views.update_vote, name='film_vote'),
    path('templates/404', views.films_results, name='404'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]