from django.contrib.auth.models import User
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class Breed(models.Model):
    name = models.CharField(max_length=255, primary_key=True,)

    class Meta:
        verbose_name = 'Порода'
        verbose_name_plural = 'Породы'

    def __str__(self):
        return self.name


class Kitten(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    age_in_months = models.PositiveIntegerField()
    description = models.TextField()
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        related_name='kittens',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='kittens',
    )

    class Meta:
        verbose_name = 'Котенок'
        verbose_name_plural = 'Котята'

    def __str__(self):
        return f'{self.owner.username}: {self.breed.name} {self.name}'


class KittenRating(models.Model):
    kitten = models.ForeignKey(Kitten, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1),
        ],
    )

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return f'{self.user}: {self.kitten.name} - {self.score}'
