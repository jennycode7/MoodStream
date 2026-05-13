from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/accounts/register/', views.RegisterView.as_view()),
    path('api/accounts/login/', views.LoginView.as_view()),
    path('api/accounts/logout/', views.LogoutView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view())
]