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


##########
# TODO
# templates
#   base done
#   index done
#   book done
#   ratings done
#   books
#   newbook
#   user 
# forms and their views
# registration
##########


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class ModelTests(TestCase):
    """
    Check that models are set up correctly.
    """
    fixtures = ['data.json', ]
    def test_book_model(self):
        """
        Check that the book model is set up correctly.
        """
        genre = Genre.objects.get(pk = 1)
        book = Book.objects.get(ISBN='9780312150846')
        self.assertEqual(book.ISBN, '9780312150846', f"{FAILURE_HEADER}Book ISBN does not match.{FAILURE_FOOTER}")
        self.assertEqual(book.title, 'The Colour of Magic', f"{FAILURE_HEADER}Book title does not match.{FAILURE_FOOTER}")
        self.assertEqual(book.author, 'Terry Pratchet', f"{FAILURE_HEADER}Book author does not match.{FAILURE_FOOTER}")
        self.assertEqual(book.description, "The Colour of Magic is a collection of four stories set on Discworld, a flat planet that is carried by four huge elephants that stand on the back of the giant turtle Great A'Tuin. The stories pivot on the hapless failed wizard Rincewind.", f"{FAILURE_HEADER}Book description does not match.{FAILURE_FOOTER}")
        self.assertEqual(book.genre, genre, f"{FAILURE_HEADER}Book genre does not match.{FAILURE_FOOTER}")

    def test_rating_model(self):
        """
        Check that the rating model is set up correctly.
        """
        user_py = User.objects.get(pk = 2)
        book_py = Book.objects.get(pk = 2)
        rating = Rating.objects.get(username = user_py, ISBN = book_py)
        self.assertEqual(rating.title, "Emotional doesn't quite describe the experience", f"{FAILURE_HEADER}Rating title does not match.{FAILURE_FOOTER}")
        self.assertEqual(rating.review, "I've never been so inspired to live in Hobbiton. Even the mention of Hobbiton is enough to bring my flatmate to emotional wreckage", f"{FAILURE_HEADER}Rating review does not match.{FAILURE_FOOTER}")
        self.assertEqual(rating.stars, 5, f"{FAILURE_HEADER}Rating stars does not match.{FAILURE_FOOTER}")

    def test_str_method(self):
        """
        Check whether the correct __str__() method has been implemented for each model.
        """
        user_py = User.objects.get(pk = 2)
        book_py = Book.objects.get(title = 'The Hobbit')
        genre_py = Genre.objects.get(name='Art')
        rating_py = Rating.objects.get(username = user_py, ISBN = book_py)
        
        
        self.assertEqual(str(book_py), 'The Hobbit', f"{FAILURE_HEADER}The __str__() method in the Book class has not been implemented correctly.{FAILURE_FOOTER}")
        self.assertEqual(str(rating_py), '5', f"{FAILURE_HEADER}The __str__() method in the Rating class has not been implemented correctly.{FAILURE_FOOTER}")
        self.assertEqual(str(genre_py), 'Art', f"{FAILURE_HEADER}The __str__() method in the Genre class has not been implemented correctly.{FAILURE_FOOTER}")


class IndexNoItemsTests(TestCase):
    """
    Test the index view and template without populating.
    """
    def setUp(self):
        self.response = self.client.get(reverse('bookCranny:index'))
        self.content = self.response.content.decode()
    
    def test_base_loaded_correctly(self):
        """
        Check that the header bar is loaded in correctly.
        """
        base_regex = r'<a href="/bookcranny/" class="a_button large_a_button">(\s*|\n*)Book Cranny(\s*|\n*)</a>'
        self.assertTrue(re.search(base_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the home page.{FAILURE_FOOTER}")

    
    def test_empty_index_context_dictionary(self):
        """
        Check that the index view is configured correctly.
        """
        self.assertTrue('books' in self.response.context, f"{FAILURE_HEADER}The 'books' variable does not exist in the context dictionary. (Empty check){FAILURE_FOOTER}")
        self.assertEqual(type(self.response.context['books']), QuerySet, f"{FAILURE_HEADER}The 'books' variable in the context dictionary does not yield a QuerySet object. (Empty check){FAILURE_FOOTER}")
        self.assertEqual(len(self.response.context['books']), 0, f"{FAILURE_HEADER}The 'books' variable in the context dictionary is not empty. (Empty check){FAILURE_FOOTER}")

        self.assertTrue('reviews' in self.response.context, f"{FAILURE_HEADER}The 'reviews' variable does not exist in the context dictionary. (Empty check){FAILURE_FOOTER}")
        self.assertEqual(type(self.response.context['reviews']), QuerySet, f"{FAILURE_HEADER}The 'reviews' variable in the context dictionary does not yield a QuerySet object. (Empty check){FAILURE_FOOTER}")
        self.assertEqual(len(self.response.context['reviews']), 0, f"{FAILURE_HEADER}The 'reviews' variable in the context dictionary is not empty. (Empty check){FAILURE_FOOTER}")
    
    def test_empty_index_response(self):
        """
        Check whether the correct messages appear for no books and reviews.
        """
        self.assertIn('There are no books in the database.', self.content, f"{FAILURE_HEADER}Cannot find the required string that displays when no books are in the database.{FAILURE_FOOTER}")
        self.assertIn('There are no reviews in the database.', self.content, f"{FAILURE_HEADER}Cannot find the required string that displays when no reviews are in the database.{FAILURE_FOOTER}")
    
    def test_sample_book(self):
        """
        Check whether the correct output is displayed when books and reviews are added.
        """
        user_py = User.objects.create_user(username='TestUser')
        genre_py = Genre.objects.get_or_create(name='TestGenre')
        book_py = Book.objects.get_or_create(ISBN = '1234567890', title='TestTitle', author='TestAuthor', description='TestDescription', genre = genre_py[0])
        Rating.objects.get_or_create(username = user_py, ISBN = book_py[0], title='TestTitle', review='TestReview', stars= 5)
        
        updated_response = self.client.get(reverse('bookCranny:index')).content.decode()

        book_regex = r'<a href="/bookcranny/book/1234567890/" class="a_button hb_right">View</a>'
        self.assertTrue(re.search(book_regex, updated_response), f"{FAILURE_HEADER}Cannot find the link to the new book in the template.{FAILURE_FOOTER}")
        review_regex = r'<a href="/bookcranny/review/TestUser/1234567890/" class="a_button hb_right">Full Review</a>'
        self.assertTrue(re.search(review_regex, updated_response), f"{FAILURE_HEADER}Cannot find the link to the new review in the template.{FAILURE_FOOTER}")

class IndexTests(TestCase):
    """
    Test the index view and template.
    """
    fixtures = ['data.json', ]
    def setUp(self):
        self.response = self.client.get(reverse('bookCranny:index'))
        self.content = self.response.content.decode()
        
    def test_index_context_dictionary(self):
        """
        Check that the index view context dictionary is configured correctly.
        """
        self.assertEqual(len(self.response.context['books']), 5, f"{FAILURE_HEADER}The 'books' variable in the context dictionary is not empty. (Empty check){FAILURE_FOOTER}")
        self.assertEqual(len(self.response.context['reviews']), 4, f"{FAILURE_HEADER}The 'reviews' variable in the context dictionary is not empty. (Empty check){FAILURE_FOOTER}")
    
    def test_links_in_template(self):
        """
        Check whether the link to the books and reviews are in the template.
        """
        book_regex = r'<a href="/bookcranny/book/9780261103306/" class="a_button hb_right">View</a>'
        self.assertTrue(re.search(book_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the book in the template.{FAILURE_FOOTER}")
        review_regex = r'<a href="/bookcranny/review/Arthur/9781594133299/" class="a_button hb_right">Full Review</a>'
        self.assertTrue(re.search(review_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the new review in the template.{FAILURE_FOOTER}")
    
class BookTests(TestCase):
    """
    Test the book view and template.
    """
    fixtures = ['data.json', ]
    def setUp(self):
        self.response = self.client.get(reverse('bookCranny:book', kwargs={'ISBN':'9780261103306'}))
        self.content = self.response.content.decode()

    def test_base_loaded_correctly(self):
        """
        Check that the header bar is loaded in correctly.
        """
        base_regex = r'<a href="/bookcranny/" class="a_button large_a_button">(\s*|\n*)Book Cranny(\s*|\n*)</a>'
        self.assertTrue(re.search(base_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the home page.{FAILURE_FOOTER}")

    
    def test_context_dictionary(self):
        """
        Check that the context dictionary is configured correctly.
        """
        book = Book.objects.get(ISBN='9780261103306')
        self.assertEqual(self.response.context['book'], book, f"{FAILURE_HEADER}The context dictionary does not contain the correct data.{FAILURE_FOOTER}")
        
    def test__review_links_in_template(self):
        """
        Check whether the link to the users and reviews are in the template.
        """
        user_regex = r'<a href="/bookcranny/user/Steven/" class="a_button">Steven</a>'
        self.assertTrue(re.search(user_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the user in the template.{FAILURE_FOOTER}")
        review_regex = r'<a href="/bookcranny/review/Steven/9780261103306/" class="a_button hb_right">Full Review</a>'
        self.assertTrue(re.search(review_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the review in the template.{FAILURE_FOOTER}")
    
    def test_no_reviews(self):
        """
        Test that the correct message appears when there are no reviews for the book.
        """
        updated_response = self.client.get(reverse('bookCranny:book', kwargs={'ISBN':'9780192827609'})).content.decode()
        self.assertIn('There are no reviews for this book in the database.', updated_response, f"{FAILURE_HEADER}Cannot find the required string that displays when no reviews exist for the book.{FAILURE_FOOTER}")

class RatingTests(TestCase):
    """
    Test the rating view and template.
    """
    fixtures = ['data.json', ]
    def setUp(self):
        self.response = self.client.get(reverse('bookCranny:rating', kwargs={'ISBN':'9780261103306', 'username':'Steven'}))
        self.content = self.response.content.decode()

    def test_base_loaded_correctly(self):
        """
        Check that the header bar is loaded in correctly.
        """
        base_regex = r'<a href="/bookcranny/" class="a_button large_a_button">(\s*|\n*)Book Cranny(\s*|\n*)</a>'
        self.assertTrue(re.search(base_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the home page.{FAILURE_FOOTER}")

    
    def test_context_dictionary(self):
        """
        Check that the context dictionary is configured correctly.
        """
        user_py = User.objects.get(username = 'Steven')
        book_py = Book.objects.get(ISBN = '9780261103306')
        rating = Rating.objects.get(username = user_py, ISBN = book_py)
        self.assertEqual(self.response.context['rating'], rating, f"{FAILURE_HEADER}The context dictionary does not contain the correct data.{FAILURE_FOOTER}")
        
    def test__review_links_in_template(self):
        """
        Check whether the link to the user and the book are in the template.
        """
        user_regex = r'<a href="/bookcranny/user/Steven/" class="a_button">Steven</a>'
        self.assertTrue(re.search(user_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the user in the template.{FAILURE_FOOTER}")
        book_regex = r'<a href="/bookcranny/book/9780261103306/" class="a_button hb_right">Back to the book</a>'
        self.assertTrue(re.search(book_regex, self.content), f"{FAILURE_HEADER}Cannot find the link to the book in the template.{FAILURE_FOOTER}")
       
