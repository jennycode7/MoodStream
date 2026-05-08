from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import  APIView
from .models import User
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class LoginView(generics.GenericAPIView):
    # parser_classes = [FormParser, MultiPartParser]
    serializer_class = LoginSerializer

    @extend_schema(
        description="Authenticate user and return JWT tokens. Also Email for username",
        examples=[
            {
                "name": "Login Example",
                "value": {
                    "email": "user@example.com",
                    "password": "password123"
                }
            }
        ]
    )


    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username
            }, 
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)



class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_200_OK
        )