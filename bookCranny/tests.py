import os
import re
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User, UserManager
from django.forms import fields as django_fields
from django.db.models.query import QuerySet
from bookCranny.models import Genre, User, Book, Rating, Wishlist
from bookCranny.forms import UserForm, BookForm, RatingForm
#from populate_rango import populate


##########
# TODO
# population script
# admin interface
##########


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"


class ConfigurationTests(TestCase):
    """
    Tests the configuration of the project
    """
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.bookCranny_app_dir = os.path.join(self.project_base_dir, 'bookCrannyProject')
        #populate{}

class ModelTests(TestCase):
    """
    Are the models set up correctly, and do all the required attributes (post exercises) exist?
    """
   
    def setUp(self):
        user_py = User.objects.create_user(username='TestUser')
        genre_py = Genre.objects.get_or_create(name='TestGenre')
        book_py = Book.objects.get_or_create(ISBN = '1234567890', title='TestTitle', author='TestAuthor', description='TestDescription', genre = genre_py[0])
        Rating.objects.get_or_create(username = user_py, ISBN = book_py[0], title='TestTitle', review='TestReview', stars= 5)

    def test_book_model(self):
        """
        Runs some tests on the book model.
        Do the correct attributes exist?
        """
        genre_py = Genre.objects.get(name='TestGenre')
        book = Book.objects.get(ISBN='1234567890')
        self.assertEqual(book.ISBN, '1234567890', f"{FAILURE_HEADER}Tests on the Book model failed. Check you have all required attributes.{FAILURE_FOOTER}")
        self.assertEqual(book.title, 'TestTitle', f"{FAILURE_HEADER}Tests on the Book model failed. Check you have all required attributes.{FAILURE_FOOTER}")
        self.assertEqual(book.author, 'TestAuthor', f"{FAILURE_HEADER}Tests on the Book model failed. Check you have all required attributes.{FAILURE_FOOTER}")
        self.assertEqual(book.description, 'TestDescription', f"{FAILURE_HEADER}Tests on the Book model failed. Check you have all required attributes.{FAILURE_FOOTER}")
        self.assertEqual(book.genre, genre_py, f"{FAILURE_HEADER}Tests on the Book model failed. Check you have all required attributes.{FAILURE_FOOTER}")

    def test_rating_model(self):
        """
        Runs some tests on the rating model.
        Do the correct attributes exist?
        """
        user_py = User.objects.get(username='TestUser')
        book_py = Book.objects.get(ISBN='1234567890')
        genre_py = Book.objects.get(ISBN='1234567890').genre
        rating = Rating.objects.get(username = user_py, ISBN = book_py)
        self.assertEqual(rating.title, 'TestTitle', f"{FAILURE_HEADER}Tests on the Rating model failed. Check you have all required attributes.{FAILURE_FOOTER}")
        self.assertEqual(rating.review, 'TestReview', f"{FAILURE_HEADER}Tests on the Rating model failed. Check you have all required attributes.{FAILURE_FOOTER}")
        self.assertEqual(rating.stars, 5, f"{FAILURE_HEADER}Tests on the Rating model failed. Check you have all required attributes.{FAILURE_FOOTER}")

    def test_str_method(self):
        """
        Tests to see if the correct __str__() method has been implemented for each model.
        """
        user_py = User.objects.get(username='TestUser')
        book_py = Book.objects.get(ISBN='1234567890')
        genre_py = Genre.objects.get(name='TestGenre')
        rating_py = Rating.objects.get(username = user_py, ISBN = book_py)
        
        
        self.assertEqual(str(book_py), 'TestTitle', f"{FAILURE_HEADER}The __str__() method in the Book class has not been implemented correctly.{FAILURE_FOOTER}")
        self.assertEqual(str(rating_py), '5', f"{FAILURE_HEADER}The __str__() method in the Book class has not been implemented correctly.{FAILURE_FOOTER}")
        self.assertEqual(str(genre_py), 'TestGenre', f"{FAILURE_HEADER}The __str__() method in the Book class has not been implemented correctly.{FAILURE_FOOTER}")
        



