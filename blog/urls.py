
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('blogcomment/', views.blogComment, name='blogComment'),
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>/', views.blogPost, name='blogPost')
    # path('blogpost/', views.blogPost, name='blogPost')
]