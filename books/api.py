import json
from .models import Book
from .permissions import IsActiveUser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from .serializer import BookSerializer



@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def api_overview(request):
    api_urls = {
        'List': 'books/books-list/',
        'Detail View': 'books/book-detail/<str:pk>/',
        'Create / Update / Delete': 'books/books-edit/',
    }
    return Response({'api_urls': api_urls, 'username': request.user.username}, template_name= 'books/api_overview.html')

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def books_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    pretty_json = json.dumps(serializer.data, indent=2, ensure_ascii=False)
    return Response({'data': pretty_json, 'username': request.user.username}, template_name='books/books_list.html')

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])
def book_detail(request, pk):
    try:
        book = Book.objects.get(id=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book, many=False)
    pretty_json = json.dumps(serializer.data, indent=2, ensure_ascii=False)
    return Response({'data': pretty_json, 'username': request.user.username}, template_name='books/books_list.html')

@api_view(['GET', 'POST'])
@renderer_classes([TemplateHTMLRenderer])
def books_edit(request, pk=None):
    if request.method == 'GET':
        return Response({'username': request.user.username},template_name='books/books_edit.html')

    id = request.data.get('id')
    title = request.data.get('title')
    author = request.data.get('author')
    pages= request.data.get('pages')
    
    if request.method== 'POST' and 'create' in request.data:
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, template_name='books/books_edit.html')
        return Response(serializer.errors, template_name='books/books_edit.html')
    
    if request.method== 'POST' and 'update' in request.data:
        try:
            book = Book.objects.get(id=request.data.get('id'))
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, template_name='books/books_edit.html')
        
        serializer = BookSerializer(instance=book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, template_name='books/books_edit.html')
        return Response({'data': serializer.errors}, template_name='books/books_edit.html')

    if request.method == 'POST' and 'delete' in request.data:
            try:
                book = Book.objects.get(id=request.data.get('id'))
                book.delete()
                return Response({'msg': 'Book deleted successfully!'},
                                template_name='books/books_edit.html')
            except Book.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND ,
                                template_name='books/books_edit.html')
