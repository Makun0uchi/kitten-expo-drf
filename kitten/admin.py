from django.contrib import admin
from .models import Kitten, Breed


admin.site.register(Breed)
admin.site.register(Kitten)
