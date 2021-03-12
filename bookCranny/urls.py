from django.urls import path
from bookcranny import views

app_name = 'bookcranny'

urlpatterns = [
    path('', views.index, name='index'), 
    path('signup/', views.signup, name='signup'), 
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('books/', views.books, name='books'),
    path('book/<isbn>/', views.book, name='book'),
    path('user/<username>/', views.user, name='user'),
    path('review/<reviewer>/<isbn>/', views.review, name='review'),
    path('newbook/', views.newbook, name='newbook'), 
]