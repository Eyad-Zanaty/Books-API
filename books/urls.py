from django.urls import path
from . import api


app_name= 'books'
urlpatterns = [
    path('', api.api_overview, name='api-overview'),
    path('books-list/', api.books_list, name='book-list'),
    path('book-detail/<str:pk>/', api.book_detail, name='book-detail'),
    path('books-edit/', api.books_edit, name='book-create'),
]