from django.contrib import admin

# Register your models here.
from catalog.models import Author
from catalog.models import Genre
from catalog.models import Book,UserProfile


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(UserProfile)




