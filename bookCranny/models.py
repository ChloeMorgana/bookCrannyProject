from django.db import models
from django.contrib.auth.models import User

class Genre(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    ISBN = models.CharField(max_length=13, unique=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    def __str__(self):
        return self.title
        
    # for admin functionality, only show first 50 characters
    def short_description(self):
        return self.description if len(self.description) < 50 else (self.description[:50])

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    books = models.ManyToManyField(Book)
    time = models.DateTimeField(auto_now_add=True, verbose_name="created time")
    
    # for admin functionality, show first 10 books
    def get_books_ISBN(self):
        ISBNs =  ",".join([str(s) for s in self.books.all().values_list('ISBN', flat = True)[:10]])
        return ISBNs
    get_books_ISBN.short_description = 'ISBN'

class Rating(models.Model):
    STARS_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    ratingID = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="book title")
    title = models.CharField(max_length=100)
    review = models.CharField(max_length=1000, blank = True)
    stars = models.IntegerField(choices = STARS_CHOICES)
    time = models.DateTimeField(auto_now_add=True, verbose_name="created time")

    def __str__(self):
        return str(self.stars)
        
    @property
    def as_stars(self):
        return "★" * self.stars + "☆" * (5 - self.stars)
    
    # for admin functionality, only show first 50 characters
    def short_review(self):
        return self.review if len(self.review) < 50 else (self.review[:50])
    
    

