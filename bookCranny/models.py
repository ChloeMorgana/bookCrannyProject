from django.db import models
from django.contrib.auth.models import User

#class User(models.Model):
#    user = models.OneToOneField(User, max_length = 20, on_delete=models.CASCADE)
#    password = models.CharField(max_length=20)

 #   def __str__(self):
  #      return self.user.username
        
class Genre(models.Model):
    name= models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name
        
class Book(models.Model):
    ISBN= models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    blurb = models.CharField(max_length=1000)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ISBN = Book._meta.get_field('ISBN')
    #ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    review = models.CharField(max_length=1000)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return str(self.stars)

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
