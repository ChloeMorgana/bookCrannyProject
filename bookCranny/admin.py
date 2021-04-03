from django.contrib import admin
from bookCranny.models import Wishlist, Book, Rating, Genre

class BookAdmin(admin.ModelAdmin):
    list_display = ('ISBN', 'title', 'author', 'genre')
    
    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True;
        return False;
        
    def has_delete_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True;
        return False;

admin.site.register(Book, BookAdmin)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('ISBN', 'username', 'stars', 'title', 'short_review', 'time')    
    
    def has_change_permission(self, request, obj = None):
        if request.user == 'username':
            return True;
        if request.user.is_superuser:
            return True;
        return False;
        
    def has_delete_permission(self, request, obj = None):
        if request.user == 'username':
            return True;
        if request.user.is_superuser:
            return True;
        return False;

admin.site.register(Rating, RatingAdmin)

class GenreAdmin(admin.ModelAdmin):    
    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True;
        return False;
        
    def has_delete_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True;
        return False;
        
admin.site.register(Genre, GenreAdmin)


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_books_ISBN', 'time')
    filter_horizontal = ('books',)
    def has_add_permission(self, request, obj = None):
        if request.user == 'username':
            return True;
        if request.user.is_superuser:
            return True;
        return False;
    
    def has_change_permission(self, request, obj = None):
        if request.user == 'username':
            return True;
        if request.user.is_superuser:
            return True;
        return False;
        
    def has_delete_permission(self, request, obj = None):
        if request.user == 'username':
            return True;
        if request.user.is_superuser:
            return True;
        return False;
        
admin.site.register(Wishlist, WishlistAdmin)