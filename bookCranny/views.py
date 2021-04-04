from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from bookCranny.models import Book, Rating, Wishlist
from bookCranny.forms import UserForm, BookForm, RatingForm

def index(request):
    books_list = Book.objects.order_by('-time')[:5]
    ratings_list = Rating.objects.order_by('-time')[:5]
    
    context_dict = {}
    context_dict['books'] = books_list
    context_dict['reviews'] = ratings_list
    
    return render(request, 'bookcranny/index.html', context=context_dict)

def books(request):
    books_list = Book.objects.order_by('-time')
    
    context_dict = {}
    
    if request.user.is_authenticated:
        reviews = Rating.objects.filter(username=request.user)
        # create a set of genres the user likes
        liked_genres = {r.ISBN.genre for r in reviews if r.stars >= 3}
        books_in_liked_genres = []
        other_books = []
        for book in books_list:
            if book.genre in liked_genres:
                books_in_liked_genres.append(book)
            else:
                other_books.append(book)
        context_dict['books'] = books_in_liked_genres
        context_dict['other_books'] = other_books
    else:
        context_dict['books'] = books_list
    
    return render(request, 'bookcranny/books.html', context=context_dict)


def book(request, ISBN):
    book = Book.objects.get(ISBN = ISBN)
    ratings = Rating.objects.filter(ISBN = book)
    totratings = ratings.count()
    
    totstars = 0
    if totratings != 0:
        # find the cumulative rating 
        for r in ratings:
            totstars += r.stars;
        avgrating = totstars/totratings
    else:
        totstars = 0
        avgrating = 0
    
    avgratingstars = "★" * int(avgrating) + "☆" * (5 - int(avgrating))
    
    context_dict = {}
    context_dict['book'] = book
    context_dict['ISBN'] = ISBN
    context_dict['totratings'] = totratings
    context_dict['avgrating'] = avgrating
    context_dict['avgratingstars'] = avgratingstars
    
    context_dict['author'] = book.author
    context_dict['genre'] = book.genre
    context_dict['description'] = book.description
    
    context_dict['reviews'] = ratings
    
    return render(request, 'bookcranny/book.html', context=context_dict)    

def rating(request, ISBN, username):
    form = RatingForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.save()
            return redirect(reverse('bookCranny:book.html'))
        else:
            #DEBUG
            print(form.errors)
    
    context_dict = {}
    context_dict['form'] = form
    #ISBN of the reviewed book
    context_dict['ISBN'] = ISBN
    #username of the reviewer
    context_dict['username'] = username
    
    user = User.objects.get(username=username)
    book = Book.objects.get(ISBN=ISBN)
    context_dict["book"] = book
    
    rating = Rating.objects.get(username=user,ISBN=book)
    context_dict["rating"]=rating
    
    return render(request, 'bookcranny/rating.html', context=context_dict)


@login_required
def newbook(request):
    form = BookForm()
    
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.reviewcount = 0
            book.save()
            
            return redirect(reverse('bookCranny:index'))
        else:
            #DEBUG
            print(form.errors)
        
    context_dict = {'form': form}
    
    return render(request, 'bookcranny/newbook.html', context=context_dict)
    
class UserView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        ratings = Rating.objects.filter(username = username).order_by('-time')
        wishlist = Wishlist.objects.filter(username = username).order_by('-time')
        
        return (ratings, wishlist)
    
    def get(self, request, username):
        try:
            (ratings, wishlist) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('bookCranny:index'))
            
        context_dict = {}
        context_dict['username'] = username
        context_dict['ratings'] = ratings
        context_dict['wishlist'] = wishlist
        
        return render(request, 'bookcranny/user.html', context=context_dict)
    
    @login_required    
    def post(self, request, username):
        try:
            (ratings, wishlist) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('bookCranny:index'))
        
        form = UserForm(request.post, instance = user)
        if form.is_valid():
            form.save(commit=True)
            return redirect('bookCranny:user', username)
        else:
            print(form.errors)
            
        context_dict = {}
        context_dict['username'] = username
        context_dict['ratings'] = ratings
        context_dict['wishlist'] = wishlist
        context_dict['form'] = form
        
        return render(request, 'bookcranny/user.html', context=context_dict)
        