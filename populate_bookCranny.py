import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","bookCrannyProject.settings")

import django
django.setup()
from bookCranny.models import Genre,Rating,Wishlist,Book

def populate():
    ratings={}

def add_genre():
    g=Genre.objects.get_or_create()
    g.save()
    return g

def add_rating():
    pass

def add_book():
    pass

def add_wishlist():
    pass

if __name__=="__main__":
    print('Starting Book Cranny population script...')



