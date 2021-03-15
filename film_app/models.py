from django.db import models
from django.utils.timezone import now

class Country(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        verbose_name_plural = "Countries"
    

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"

class Category(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        verbose_name_plural = "Categories"
    

    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"

class Director(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
 
    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Film(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.DateTimeField(default=now, editable=True)
    poster = models.URLField(max_length=200, null=True)
    votes = models.IntegerField(default=0)
    review = models.CharField(max_length=500, blank = True)
    streaming = models.URLField(max_length=200, null=True)
    created_in_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    available_in_countries = models.ManyToManyField(Country, related_name="all_films_country")
    category = models.ManyToManyField(Category, related_name="all_films_category")
    director = models.ManyToManyField(Director, related_name="all_films_director")

    def __repr__(self):
        return f"{self.title}"

    def __str__(self):
        return f"{self.title}"