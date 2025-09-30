from django.urls import path
from . import apis

app_name= 'api'
urlpatterns = [
    path('register/', apis.register, name='register'),
    path('login/', apis.login_user, name='login'),
    path('logout/', apis.logout_user, name='logout'),
]