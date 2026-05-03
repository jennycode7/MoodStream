from django.urls import path
from . import views


urlpatterns = [
    path('api/accounts/register/', views.RegisterView.as_view()),
    path('api/accounts/login/', views.LoginView.as_view()),
    path('api/accounts/logout/', views.LogoutView.as_view())
]