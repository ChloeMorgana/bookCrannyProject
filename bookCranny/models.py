from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    username= models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username

class Book(models.Model):
    ISBN= models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    blurb = models.CharField(max_length=1000)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Rating(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return self.stars

class Genre(models.Model):
    name= models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
