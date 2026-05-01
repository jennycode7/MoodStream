from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/', views.RecommendationView.as_view()),

    path('mood/', views.MoodView.as_view()),
    path('history/', views.HistoryView.as_view()),
    path('favorites/', views.FavoritesView.as_view()),
    path('history/', views.HistoryView.as_view()),
    path('content/', views.ContentView.as_view())
]