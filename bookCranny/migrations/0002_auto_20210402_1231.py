# Generated by Django 2.2.17 on 2021-04-02 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookCranny', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='wishlist',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='books',
            field=models.ManyToManyField(to='bookCranny.Book'),
        ),
    ]
