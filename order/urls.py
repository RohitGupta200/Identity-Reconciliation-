from django.urls import path,re_path
from .views import create,identify

urlpatterns = [
    path('create', create),
    path('identify', identify)
    
]