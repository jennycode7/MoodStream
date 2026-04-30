from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/', views.RecommendationView.as_view())
]