from rest_framework import serializers
from .models import Breed, Kitten, KittenRating


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ('name',)


class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ('name', 'color', 'age_in_months', 'description', 'breed',)


class KittenRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = KittenRating
        fields = ('id', 'kitten', 'user', 'score',)
        extra_kwargs = {
            'user': {'read_only': True}
        }


class KittenRatingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = KittenRating
        fields = ('score',)
