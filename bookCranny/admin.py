from django.contrib import admin
from bookCranny.models import Wishlist, Book, Rating, Genre

class BookAdmin(admin.ModelAdmin):
    list_display = ('ISBN', 'title', 'author', 'genre')

admin.site.register(Book, BookAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('ISBN', 'username', 'stars', 'review')

admin.site.register(Rating, RatingAdmin)

admin.site.register(Genre)