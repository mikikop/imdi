from django.contrib import admin
from .models import *

admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Director)
admin.site.register(Film)

admin.site.site_url = '/film_app/homepage'
