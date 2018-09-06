from django.urls import path
from catalog import views
from catalog import models


urlpatterns = [
        path('', views.index, name='index'),
        path('books/', views.BookListView.as_view(), name='books'),
        path('subjects/', views.BookSubjectView.as_view(), name='subjects'),
        path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
        path('authors/', views.AuthorListView.as_view(), name='authors'),
        path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
        path('books/search/', views.SearchViewBook.as_view(), name='search-book'),

]


