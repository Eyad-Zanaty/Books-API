from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from django.shortcuts import redirect


@api_view(['POST', 'GET'])
@renderer_classes([TemplateHTMLRenderer])
@csrf_exempt
@permission_classes([AllowAny])
def register(request):
    if request.method == 'GET':
        return Response({'message': ''},template_name='user/user_register.html')
    
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'},template_name='user/user_register.html')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
@renderer_classes([TemplateHTMLRenderer])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == 'GET':
        return Response(template_name='user/user_login.html')
    
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('books:api-overview'))
    return Response({'error': 'Invalid credentials'}, template_name='user/user_login.html' ,status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST', 'GET'])
@renderer_classes([TemplateHTMLRenderer])
def logout_user(request):
    if request.method == 'GET':
        return Response({'username': request.user.username}, template_name='user/user_logout.html')
    
    if request.method == 'POST':
        logout(request)
        return Response({'message': 'Logout successful'}, template_name='user/user_login.html')
    return Response(status=status.HTTP_400_BAD_REQUEST)