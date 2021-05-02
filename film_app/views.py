from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddFilmForm, AddDirectorForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import *
from imdb import IMDb
from django.contrib import messages
import json
from cprint import *
from django.http import HttpResponse
import os
import datetime
from rest_framework import viewsets, filters
from .serializers import FilmSerializer, DirectorSerializer

def home(request):
    return render(request, 'homepage.html', {'movies':Film.objects.all()})


def add_film(request):

    if request.method == "GET":
        return render(request, 'add_film.html', {'form': AddFilmForm()})

    if request.method == "POST":
        form = AddFilmForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,'Your movie is just added')
            return redirect('add-film')
        else:
            messages.error(request,'Your movie is not added')
            return render(request, 'add_film.html', {'form': form})
#search button
def films_results(request):
        if request.method == "POST":
            search = request.POST['search']
            movies = Film.objects.filter(title__icontains = search)
            if movies:
                return render(request, 'films_results.html', {'movies': movies})
            else:
                return render(request, '404.html')


def delete_film(request,id):
    movie = Film.objects.filter(pk=id).last()
    if movie:
        movie.delete()
        messages.success(request,f'{movie.title} has been deleted')
        return render(request, 'films_results.html')
    else:
        messages.error(request,f'{movie.title} has not been deleted properly')
        redirect('home')

def update_vote(request):
    data = json.loads(request.body)
    film = Film.objects.get(id=data['movie_id'])
    action = data['action']
    if action == 'like':
        film.votes += 1
    if action == 'dislike':
        if film.votes != 0:
            film.votes -= 1
    film.save()
    return HttpResponse(json.dumps({'votes': film.votes}))


class AddDirector(CreateView):
    form_class = AddDirectorForm
    template_name = 'add_director.html'
    success_url = reverse_lazy('add-director')

def search_imdb(request):
    ia = IMDb()
    if request.method == "GET":
        return render(request, 'search_imdb.html')

    if request.method == "POST":
        search = request.POST['search']
        movies = ia.search_movie(search)
        if not movies :
            return render(request, '404.html')

    return render(request, 'search_imdb.html', {'movies': movies})

def detail_imdb(request,id):
    ia = IMDb()
    movie = ia.get_movie(id)
    # context = {
    #     'title': movie['title'],
    #     'year': movie['year'],
    #     'plot': movie['plot'],
    #     'coverurl': movie['cover url']
    # }
    return render(request, 'detail_imdb.html', {'movie':movie})    


def add_from_imdb(request,id):
    ia = IMDb()
    
    single_movie = ia.get_movie(id)
    movie_url = single_movie['full-size cover url']
    #function get_or_create returns the object and a boolean  and we take the object only
    country = Country.objects.get_or_create(name=single_movie['country'][0])[0]

    #function get_or_create returns the object and a boolean 
    new_film, created = Film.objects.get_or_create(
        title = single_movie['title'],
        release_date = datetime.datetime.strptime(str(single_movie['year']),'%Y'),
        # release_date = allow_year(single_movie['year']),
        poster = url_clean(movie_url),
        created_in_country = country
    )
    if created:
        #list comprehension
        directors = [
            Director.objects.get_or_create(
                first_name=director['name'].split(' ')[0],
                last_name=director['name'].split(' ')[-1]
                )[0] 
            for director in single_movie['director']
        ]
        # same as film.directors.add(directors[0],directors[1],directors[2]...)
        new_film.director.add(*directors)

        #list comprehension
        categorys = [
            Category.objects.get_or_create(
                name=category
                )[0] 
            for category in single_movie['genre']
        ]
        # same as film.directors.add(directors[0],directors[1],directors[2]...)
        new_film.category.add(*categorys)

        messages.success(request,f'{new_film.title} has been added to the catalogue')
        return redirect('detail_imdb',id)
    else:
        messages.success(request,f'{new_film.title} has already been added to the catalogue')
        return redirect('home')

    
# allow to get a clean url cover size
def url_clean(url):
    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url

def allow_year(year):
    return f'{year}-10-05 00:00:00'


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all().order_by('title')
    serializer_class = FilmSerializer

class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['last_name']