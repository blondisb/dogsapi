from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('register/', views.register_view, name='register'),
    path('breeds/', views.breeds_view, name='breeds'),
    path('dogs/', views.dogs_view, name='dogs'),
    path('answer/', views.answer_view, name='answer'),
]