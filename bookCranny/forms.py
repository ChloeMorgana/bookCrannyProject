from django import forms
from django.contrib.auth.models import User
from bookCranny.models import User, Book, Rating, Genre


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'password')


class BookForm(forms.ModelForm):
    GENRES = [Genre.objects.all()]
    ISBN = forms.CharField(max_length=13, help_text = "Unique identifier of the book (10/13 digits long)")
    title = forms.CharField(max_length=100, help_text = "Title of the book")
    author = forms.CharField(max_length=50, help_text = "Author of the book")
    blurb = forms.CharField(widget = forms.Textarea, max_length=1000, help_text = "Enter a short description for the book (maximum 1000 characters")
    genre = forms.ChoiceField(choices = GENRES)
    
    
    class Meta:
        model = Book
        fields = ('ISBN', 'title', 'author', 'blurb')


class RatingForm(forms.ModelForm):
    title = forms.CharField(max_length=100, help_text="Please enter a title for your review")
    stars = forms.DecimalField(widget=forms.HiddenInput(), min_value = 1, max_value = 5)
    review = forms.CharField(widget = forms.Textarea, help_text = "(Optional) A detailed review of the book")

    class Meta:
        model = Rating
        exclude = ('ISBN', 'username')