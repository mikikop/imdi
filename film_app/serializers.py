from rest_framework import serializers
from .models import Film, Director


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ('id', 'title', 'release_date', 'poster', 'votes', 'review', 'streaming', 'director')
        extra_kwargs = {'director':{'required':False}}

class DirectorSerializer(serializers.ModelSerializer):
    all_films_director = FilmSerializer(many=True, read_only=True)

    class Meta:
        model = Director
        fields = ('id','first_name','last_name','all_films_director')
        extra_kwargs = {'all_films_director': {'required':False}}