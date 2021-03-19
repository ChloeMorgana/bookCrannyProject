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


def signup(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            
            # hash password and update user object
            user.set_password(user.password)
            user.save()
            
            registered = True
        else:
            #DEBUG
            print(user_form.errors)
    else:
        user_form = UserForm()
    
    return render(request, 'bookcranny/register.html',
                  context = {'user_form': user_form,
                             'registered': registered})


def user_login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        # details correct if User object exists
        # None if no matching credentials found
        if user:
            login(request, user)
            return redirect(reverse('bookcranny:index'))
        else:
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'bookcranny/login.html', context=context_dict)


def books(request):
    books_list = Book.objects.order_by('-time')
    
    context_dict = {}
    context_dict['books'] = books_list
    
    return render(request, 'bookcranny/books.html', context=context_dict)


def book(request, ISBN):
    book = Book.objects.filter(ISBN = ISBN)
    
    context_dict = {}
    context_dict['book'] = book
    context_dict['ISBN'] = ISBN
    
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
    

def rating(request):
    form = RatingForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.save()
            return redirect(reverse('bookcranny:book.html'))
        else:
            #DEBUG
            print(form.errors)
    
    context_dict = {}
    context_dict['form'] = form
    context_dict['ISBN'] = form.cleaned_data['ISBN']
    context_dict['username'] = form.cleaned_data['username']
    
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
            
            return redirect(reverse('bookcranny:index'))
        else:
            #DEBUG
            print(form.errors)
        
    context_dict = {'form': form}
    
    return render(request, 'bookcranny/newbook.html', context=context_dict)
 
 
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('bookcranny:index'))