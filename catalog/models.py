from django.db import models
from django.urls import reverse
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author",on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book',null=True, blank=True)
    genre = models.ManyToManyField("Genre", help_text='Select a genre for this book')
    URLS = models.CharField(max_length=200,help_text='Enter th URL of the book to our drive')
    Cover_Pic=models.ImageField(default='reader.png')
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100,default="")
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.CharField('Died',blank=True,null=True,max_length=50,default="Still Alive")
    picture=models.ImageField(default="shakespeare.png")
    class Meta:
        ordering = ['last_name', 'first_name']
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    def get_absolute_url(self):
        """Returns the url to access a detail record for this author."""
        return reverse('author-detail', args=[str(self.id)])
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    avatar = models.ImageField(upload_to='profile_image',null=True,blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES,default="Male")

    def __str__(self):
        return  self.user.username
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=50, help_text='Enter a book genre (e.g. Science Fiction)')
    def __str__(self):
        """String for representing the Model object."""
        return self.name

