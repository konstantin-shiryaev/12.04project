from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('post/<str:slug>', views.post_detail, name='post'),
    path('post_create', views.post_create, name='post_create'),
    path('like/', views.like, name='like'),
    path('delete_post/<str:slug>', views.delete_post, name='delete_post')
]
