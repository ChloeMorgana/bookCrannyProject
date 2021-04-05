from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bookCranny.models import User, Book, Rating, Genre


class UserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        exclude = {'email', }


class BookForm(forms.ModelForm):
    GENRES = Genre.objects.all()
    ISBN = forms.CharField(max_length=13, help_text = "Unique identifier of the book (10/13 digits long)")
    title = forms.CharField(max_length=100, help_text = "Title of the book")
    author = forms.CharField(max_length=50, help_text = "Author of the book")
    description = forms.CharField(widget = forms.Textarea, max_length=1000, help_text = "Enter a short description for the book (maximum 1000 characters)", required = False)
    genre = forms.ModelChoiceField(queryset = GENRES)
    
    def clean(self):
        title = self.cleaned_data['title']
        author = self.cleaned_data['author']
        ISBN = self.cleaned_data['ISBN']
        try:
            book = Book.objects.get(title=title, author = author)
            if book.ISBN == ISBN:
                msg = "Book with this ISBN already exists."
                self.add_error('ISBN', msg)
            else:
                msg = "Book already exists under a different ISBN code."
                self.add_error('title', msg)
                self.add_error('author', msg)
        except Book.DoesNotExist:
            pass
            
    
    
    class Meta:
        model = Book
        fields = ('ISBN', 'title', 'author', 'genre', 'description')


class RatingForm(forms.ModelForm):
    title = forms.CharField(max_length=100, help_text="Please enter a title for your review")
    stars = forms.IntegerField(min_value = 1, max_value = 5)
    review = forms.CharField(widget = forms.Textarea, help_text = "(Optional) A detailed review of the book", required = False)

    class Meta:
        model = Rating
        exclude = ('username', 'time', 'ISBN')