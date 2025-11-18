from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.auth_view, name='auth'),
    path('breeds/', views.BreedListView.as_view(), name='breeds'),
    path('dogs/', views.DogListView.as_view(), name='dogs'),
    path('answer/', views.answer_view, name='answer'),
    path('statistics/', views.statistics_view, name='statistics'),  # Para testing
]