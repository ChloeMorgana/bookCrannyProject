from django import forms
from django.contrib.auth.models import User
from bookcranny.models import User, Book, Review


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'password',)


class BookForm(forms.ModelForm):
#    GENRES =( 
#        ("1", "G1"), 
#        ("2", "G2"), 
#        ("3", "G3"), 
#        ("4", "G4"), 
#        ("5", "G5"), 
#    )
        
    isbn = forms.DecimalField(min_digits = 10, max_digits=13, help_text = "Unique identifier of the book (10/13 digits long)")
    title = forms.CharField(max_length=128, help_text = "Title of the book")
    author = forms.CharField(max_length=128, help_text = "Author of the book")
    description = forms.CharField(widget = forms.Textarea, max_length=1000, help_text = "Enter a short description for the book (maximum 1000 characters")
#   genre = forms.ChoiceField(choices = GENRES)
    reviews = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
    
    
    class Meta:
        model = Book


class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter a title for your review")
    stars = forms.DecimalField(widget=forms.HiddenInput(), min_value = 1, max_value = 5)
    fullreview = forms.CharField(widget = forms.Textarea, help_text = "(Optional) A detailed review of the book")

    class Meta:
        model = Review
        exclude = ('isbn', 'reviewer')    