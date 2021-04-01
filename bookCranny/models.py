from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    time = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    ISBN = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    blurb = models.CharField(max_length=1000)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    wishlist = models.ManyToManyField(Wishlist)

    def __str__(self):
        return self.title


class Rating(models.Model):
    ratingID = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    review = models.CharField(max_length=1000)
    stars = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stars
