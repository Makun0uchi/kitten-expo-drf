from django.contrib.auth.models import User
from django.db import models


class Breed(models.Model):
    name = models.CharField(max_length=255, primary_key=True,)

    def __str__(self):
        return self.name


class Kitten(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    age_in_months = models.IntegerField()
    description = models.TextField()
    breed = models.ForeignKey(
        Breed,
        on_delete=models.CASCADE,
        related_name='kittens',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users_kittens',
        default=1,
    )

    def __str__(self):
        return f'{self.owner.username}: {self.breed.name} {self.name}'
