from django.contrib import admin
from bookCranny.models import Wishlist, Book, Rating, Genre
from django import forms

class BookModelForm(forms.ModelForm):
    description = forms.CharField(widget = forms.Textarea, max_length=1000, help_text = "Enter a short description for the book (maximum 1000 characters", required = False)
    
    class Meta:
        model = Book
        fields = ('ISBN', 'title', 'author', 'genre', 'description')

class BookAdmin(admin.ModelAdmin):
    list_filter = ('genre', 'time')
    list_display = ('ISBN', 'title', 'author', 'genre', 'short_description', 'time')
    form = BookModelForm
    
    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True;
        return False;
        
    def has_delete_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True;
        return False;

admin.site.register(Book, BookAdmin)

class RatingForm(forms.ModelForm):
    review = forms.CharField(widget = forms.Textarea, help_text = "(Optional) A detailed review of the book", required = False)

    class Meta:
        model = Rating
        exclude = ('time', )

class RatingAdmin(admin.ModelAdmin):
    list_filter = ('ISBN', 'username', 'time', 'ratingID')
    list_display = ('ISBN', 'username', 'stars', 'title', 'short_review', 'time')    
    form = RatingForm
    
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