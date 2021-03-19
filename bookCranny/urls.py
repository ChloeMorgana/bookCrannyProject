from django.urls import path
from bookCranny import views

app_name = 'bookCranny'

urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/', views.signup, name='signup'), 
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('books/', views.books, name='books'),
    path('book/<ISBN>/', views.book, name='book'),
    path('user/<username>/', views.user, name='user'),
    path('review/<username>/<ISBN>/', views.rating, name='rating'),
    path('newbook/', views.newbook, name='newbook'), 
]