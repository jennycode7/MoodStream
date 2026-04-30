from django.urls import path
from . import views


urlpatterns = [
    path('api/accounts/register/', views.RegisterView.as_view())
]