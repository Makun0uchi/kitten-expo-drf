from django.contrib import admin
from .models import Kitten, Breed, KittenRating

admin.site.register(Breed)
admin.site.register(Kitten)
admin.site.register(KittenRating)
