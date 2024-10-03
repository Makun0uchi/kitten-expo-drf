from rest_framework import serializers
from .models import Breed, Kitten


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ('name',)


class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ('name', 'color', 'age_in_months', 'description', 'breed',)
