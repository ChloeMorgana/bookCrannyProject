import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "bookCrannyProject.settings")

import django

django.setup()
from bookCranny.models import User, Wishlist, Book, Genre, Rating


def populate():
    genres = [{"name": "Horror"}, {"name": "Crime"}, {"name": "Fantasy"},
              {"name": "Romance"}, {"name": "Science Fiction"},
              {"name": "Mystery"}, {"name": "Psychological Fiction"}]

    users = [{"username": "Astrid"}, {"username": "Logan"}, {"username": "Arthur"}, {"username": "Steven"},
             {"username": "Polly"}, {"username": "Morgan"}]

    books = [{"ISBN": "9780312150846",
              "title": "The Colour of Magic",
              "author": "Terry Pratchett",
              "description": "The Colour of Magic is a collection of four stories set on Discworld, a flat planet that is carried by four huge elephants that stand on the back of the giant turtle Great A'Tuin. The stories pivot on the hapless failed wizard Rincewind.",
              "genre": "Fantasy"},

             {"ISBN": "9780261103306",
              "title": "The Hobbit",
              "author": "J.R.R Tolkien",
              "description": "The Hobbit is set within Tolkien's fictional universe and follows the quest of home-loving Bilbo Baggins, the titular hobbit, to win a share of the treasure guarded by Smaug the dragon. Bilbo's journey takes him from light-hearted, rural surroundings into more sinister territory.",
              "genre": "Fantasy"},

             {"ISBN": "9781594133299",
              "title": "Twilight",
              "author": "Stephenie Meyer",
              "description": "Twilight is a series of fantasy/romance novels by Stephenie Meyer. It follows the life of Isabella Swan, a human teenager who moves to Forks, Washington and finds her life turned upside-down when she falls in love with a vampire named Edward Cullen.",
              "genre": "Romance"},

             {"ISBN": "9780192827609",
              "title": "Pride and Prejudice",
              "author": "Jane Austen",
              "description": "Pride and Prejudice follows the turbulent relationship between Elizabeth Bennet, the daughter of a country gentleman, and Fitzwilliam Darcy, a rich aristocratic landowner. They must overcome the titular sins of pride and prejudice in order to fall in love and marry.",
              "genre": "Romance"},

             {"ISBN": "9780375507908",
              "title": "In Cold Blood",
              "author": "Truman Capote",
              "description": "In Cold Blood is a non-fiction novel by American author Truman Capote, first published in 1966. It details the 1959 murders of four members of the Herbert Clutter family in the small farming community of Holcomb, Kansas.",
              "genre": "Crime"},

             {"ISBN": "9780006137122",
              "title": "Murder On The Orient Express",
              "author": "Agatha Christie",
              "description": "A group of passengers trapped on the Orient Express in a snow storm with a murdered body and a Belgian detective to keep them company: Murder on the Orient Express is one of Agatha Christie's most famous stories. ... Mrs Christie makes an improbable tale very real, and keeps her readers enthralled and guessing to the end.",
              "genre": "Crime"},

             {"ISBN": "9781444846195",
              "title": "The Midnight Library",
              "author": "Matt Haig",
              "description": "The Midnight Library is about Nora, a thirty-something woman who is regretful about her life and feels alienated and unneeded in this world. In the depths of her wallowing, she comes across the Midnight Library. In it, each book represents a portal into another variation of what her life could have been.",
              "genre": "Science Fiction"},

             {"ISBN": "9781004015368",
              "title": "Anxious People",
              "author": "Fredrik Backman",
              "description": "Anxious People is the story of a bank robber and a group of hostages at an open house…a bunch of idiots, really (in the most endearing sense of the word). But the real story behind the circumstances is about a bridge and so much more.",
              "genre": "Mystery"},

             {"ISBN": "9781524711771",
              "title": "Transcendent Kingdom",
              "author": "Yaa Gyasi",
              "description": "Transcendent Kingdom is a deeply moving portrait of a family of Ghanaian immigrants ravaged by depression and addiction and grief–a novel about faith, science, religion, love. Exquisitely written, emotionally searing, this is an exceptionally powerful follow-up to Gyasi's phenomenal debut.",
              "genre": "Psychological Fiction"},

             {"ISBN": "9780451139764",
              "title": "The Shining",
              "author": "Stephen King",
              "description": "The Shining centers on the life of Jack Torrance, a struggling writer and recovering alcoholic who accepts a position as the off-season caretaker of the historic Overlook Hotel in the Colorado Rockies.",
              "genre": "Horror"},

             {"ISBN": "9780340364772",
              "title": "It",
              "author": "Stephen King",
              "description": "The story follows the experiences of seven children as they are terrorized by an evil entity that exploits the fears of its victims to disguise itself while hunting its prey.",
              "genre": "Horror"},

             {"ISBN": "9780345019547",
              "title": "Jurassic Park",
              "author": "Michael Crichton",
              "description": "Jurassic Park is a 1990 science fiction novel written by Michael Crichton. A cautionary tale about genetic engineering, it presents the collapse of an amusement park showcasing genetically re-created dinosaurs to illustrate the mathematical concept of chaos theory and its real world implications.",
              "genre": "Science Fiction"}]

    ratings = [{"username": "Morgan",
                "ISBN": "9781594133299",
                "title": "Worst book I've ever read in my life",
                "review": "I could barely get past the first page. I don't understand the hype for this book at all. Twilight sucks!",
                "stars": 1},

               {"username": "Logan",
                "ISBN": "9780312150846",
                "title": "This book took me back",
                "review": "I felt like I was in my youth again",
                "stars": 4},

               {"username": "Polly",
                "ISBN": "97803121508462",
                "title": "This book is amazing!",
                "review": "I felt like I was being transported into another dimension whilst I was reading this. Absolutely wonderful!",
                "stars": 5},

               {"username": "Steven",
                "ISBN": "9780261103306",
                "title": "Emotional doesn't quite describe the experience",
                "review": "I've never been so inspired to live in Hobbiton. Even the mention of Hobbiton is enough to bring my flatmate to emotional wreckage",
                "stars": 5},

               {"username": "Logan",
                "ISBN": "9780451139764",
                "title": "Now this is my sort of book",
                "review": "I just love the build-up of suspense in this book. Stephen has done it again.",
                "stars": 5},

               {"username": "Astrid",
                "ISBN": "9780451139764",
                "title": "Not his best",
                "review": "If you love Stephen King and you're his biggest fan then read this book. If not, grab a better one.",
                "stars": 3},

               {"username": "Logan",
                "ISBN": "9780340364772",
                "title": "I was on the edge of my chair the whole time",
                "review": "Clowns are terrifying and my therapist recommended that I read about them to reduce my fear. Did it work? absolutely not, but I enjoyed the thrill.",
                "stars": 5},

               {"username": "Logan",
                "ISBN": "9780345019547",
                "title": "Better than the films",
                "review": "I have no idea why the youths of today would rather watch weird CGI dinosaurs on screen when they can let their imagination run wild with this book. I shall give this to them next time I hear the little rascals talk about anything other than reading.",
                "stars": 4},

               {"username": "Arthur",
                "ISBN": "9781524711771",
                "title": "This book really hits home for me",
                "review": "Hearing about Gifty and all of the troubles she endured really reminded me of my own life. I would recommend this to anyone who feels like they're alone in this world.",
                "stars": 5},

               {"username": "Arthur",
                "ISBN": "9781004015368",
                "title": "It gave me a chuckle",
                "review": "I found this book very endearing and funny.",
                "stars": 5},

               {"username": "Arthur",
                "ISBN": "9781444846195",
                "title": "Really made me re-evaluate my life",
                "review": "There's so much to reflect upon after reading this that my brain has melted.",
                "stars": 5},

               {"username": "Polly",
                "ISBN": "9780006137122",
                "title": "I was so stressed the whole time!",
                "review": "If I was stuck on a train with a murderer I have no idea what the heck I would do!",
                "stars": 3},

               {"username": "Steven",
                "ISBN": "9780340364772",
                "title": "I like horror and this was good",
                "review": "I would've given it five stars, but Stephen's name is too similar to my own and I dislike that.",
                "stars": 2},

               {"username": "Astrid",
                "ISBN": "9780261103306",
                "title": "Too many wizards and too much magic tbh",
                "review": "Honestly don't understand why everybody talks about the Hobbit. It's not that great and it isn't realistic enough.",
                "stars": 1}
               ]

    wishlists = [{"user": "Morgan", "books": ["9780345019547", "9781004015368", "9780451139764"]},
                 {"user": "Astrid", "books": ["97803121508462", "9781524711771"]},
                 {"user": "Polly", "books": ["9780451139764", "9780261103306", "9780340364772"]},
                 {"user": "Arthur", "books": ["9781594133299"]}]

    for genre in genres:
        add_genre(genre["name"])

    for book in books:
        add_book(book["ISBN"], book["title"], book["author"],
                 book["description"], book["genre"])

    for user in users:
        add_user(user["username"])

    for rating in ratings:
        add_rating(rating["ratingID"], rating["username"], rating["ISBN"],
                   rating["title"], rating["review"], rating["stars"])

    for wishlist in wishlists:
        add_wishlist(wishlist["user"], wishlist["books"])

    print("Database populated.")


def add_genre(name):
    g = Genre.objects.get_or_create(name=name)[0]
    g.save()
    return g


def add_user(username):
    u = User.objects.get_or_create(username=username)[0]
    u.save()
    return u


def add_book(ISBN, title, author, description, genre):
    b = Book.objects.get_or_create(ISBN=ISBN, title=title, author=author,
                                   description=description, genre=genre)[0]
    b.save()
    return b


def add_rating(ratingID, username, ISBN, title, review, stars):
    r = Rating.objects.get_or_create(ratingID=ratingID, username=username,
                                     ISBN=ISBN, title=title, review=review,
                                     stars=stars)[0]
    r.save()
    return r


def add_wishlist(user, books):
    w = Wishlist.objects.get_or_create(user=user, books=books)[0]
    w.save()
    return w


if __name__ == "__main__":
    print("Starting Book Cranny population script...")
    populate()
