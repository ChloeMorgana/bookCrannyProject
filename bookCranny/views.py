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
    
    if request.user.is_authenticated:
        context_dict['username'] = request.user.username
        try:
            wishlist = Wishlist.objects.get(user=request.user)
        except Wishlist.DoesNotExist:
            wishlist = Wishlist(user = request.user)
            wishlist.save()
        context_dict['in_wishlist'] = book in wishlist.books.all()
    return render(request, 'bookcranny/book.html', context=context_dict)    


def rating(request, ISBN, username):
    context_dict = {}
    user_is_editing = False
    user = User.objects.get(username = username)
    book = Book.objects.get(ISBN=ISBN)
    try:
        rating = Rating.objects.get(username=user,ISBN=book)
        context_dict["rating"]=rating
        form = RatingForm(instance = rating)
        rating_username = username
        rating_user_id = rating.username.id
    except Rating.DoesNotExist:
        form = RatingForm()
        user_is_editing = True
        rating_username = request.user.username
        rating_user_id = request.user.id
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            if form.data["username"] == str(request.user.id):
                try:
                    existing_rating = Rating.objects.get(username=request.user,ISBN__id=int(form.data["ISBN"]))
                    existing_rating.title = form.data["title"]
                    existing_rating.review = form.data["review"]
                    existing_rating.stars = int(form.data["stars"])
                    existing_rating.save()
                except Rating.DoesNotExist:
                    rating = form.save()
            return redirect(reverse('bookCranny:rating', kwargs={"username": username, "ISBN": ISBN}))
        else:
            #DEBUG
            print(form.errors)
    context_dict['form'] = form
    context_dict['ISBN'] = ISBN
    context_dict['username'] = username
    context_dict["book"] = book
    context_dict["rating_username"] = rating_username
    context_dict["rating_user_id"] = rating_user_id
    user_is_owner = (request.user.username==username)
    context_dict["user_is_owner"] = user_is_owner
    context_dict["user_is_editing"]=user_is_editing
    
    return render(request, 'bookcranny/rating.html', context=context_dict)

@login_required
def deletereview(request, ISBN):
    try:
        rating = Rating.objects.get(username=request.user, ISBN__ISBN=ISBN)
        rating.delete()
    except Rating.DoesNotExist:
        pass
    return redirect(reverse('bookCranny:book', kwargs={"ISBN": ISBN}))


#override registration form
def register(request):
    form = UserForm()
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('bookCranny:index'))
        else:
            #DEBUG
            print(form.errors)
        
    context_dict = {'form': form}
    
    return render(request, 'registration/register.html', context=context_dict)

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

@login_required
def addtowishlist(request, ISBN):
    book = Book.objects.get(ISBN = ISBN)
    try:
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist(user = request.user)
        wishlist.save()
    wishlist.books.add(book)
    
    if "redirectToUser" in request.GET and request.GET["redirectToUser"] == "yes":
        return redirect(reverse('bookCranny:user', kwargs={"username": request.user.username}))
    else:
        return redirect(reverse('bookCranny:book', kwargs={"ISBN": ISBN}))
 
@login_required
def removefromwishlist(request, ISBN):
    book = Book.objects.get(ISBN = ISBN)
    try:
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist(user = request.user)
        wishlist.save()
    wishlist.books.remove(book)
    
    if "redirectToUser" in request.GET and request.GET["redirectToUser"] == "yes":
        return redirect(reverse('bookCranny:user', kwargs={"username": request.user.username}))
    else:
        return redirect(reverse('bookCranny:book', kwargs={"ISBN": ISBN}))
    

class UserView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        ratings = Rating.objects.filter(username = user).order_by('-time')
        try:
            wishlist = Wishlist.objects.get(user=user.pk)
        except Wishlist.DoesNotExist:
            wishlist = Wishlist(user = user)
            wishlist.save()

        
        return (ratings, wishlist)
    
    def get(self, request, username):
        try:
            (ratings, wishlist) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('bookCranny:index'))
            
        context_dict = {}
        context_dict['username'] = username
        context_dict['ratings'] = ratings
        context_dict['books'] = Book.objects.filter(wishlist=wishlist)
        user_is_owner = (request.user.username==username)
        context_dict["user_is_owner"] = user_is_owner
        
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
        user_is_owner = (request.user.username==username)
        context_dict["user_is_owner"] = user_is_owner
        
        return render(request, 'bookcranny/user.html', context=context_dict)
        