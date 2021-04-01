from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from bookCranny.models import User, Book, Rating, Wishlist
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
    context_dict['books'] = books_list
    
    return render(request, 'bookcranny/books.html', context=context_dict)


def book(request, ISBN):
    book = Book.objects.filter(ISBN = ISBN)
    ratings = Rating.objects.get(ISBN = ISBN)
    totratings = ratings.count()
    
    if ratings.count != 0:
        # find the cumulative rating 
        for r in ratings:
            totstars += r.stars;
        avgrating = totstars/totratings
    else:
        totstars = 0
        avgrating = 0
    
    context_dict = {}
    context_dict['book'] = book
    context_dict['ISBN'] = ISBN
    context_dict['totratings'] = totratings
    context_dict['avgrating'] = avgrating
    
    return render(request, 'bookcranny/book.html', context=context_dict)


def user(request, username):
    profile = User.objects.filter(username = username)
    ratings = Rating.objects.filter(username = username).order_by('-time')
    wishlist = Wishlist.objects.filter(username = username).order_by('-time')
    
    context_dict = {}
    context_dict['ratings'] = ratings
    context_dict['wishlist'] = wishlist
    context_dict['username'] = username
    
    return render(request, 'bookcranny/user.html', context=context_dict)
    

def rating(request, ISBN, user):
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
    context_dict['username'] = user
    
    return render(request, 'bookcranny/rating.html', context=context_dict)


@login_required
def newbook(request):
    form = PageForm()
    
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