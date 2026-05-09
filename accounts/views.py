from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import  APIView
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, LoginSerializer, LoginResponseSerializer, RegisterResponseSerializer, LogoutSerializer
from django.contrib.auth import login, authenticate, logout
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse



# Create your views here.

@extend_schema(
        summary="User Registration",
        request=UserSerializer,
        responses={201: RegisterResponseSerializer},
        examples=[
            OpenApiExample(
                name="Register Request",
                value={
                    "email": "test@gmail.com",
                    "password": "12345678",
                    "preferred_mood": "happy"
                },
                request_only=True
            )
        ]
    )
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "User registered successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "preferred_mood": user.preferred_mood
            }
        }, status=status.HTTP_201_CREATED)





@extend_schema(
        summary="Login User",
        description="Authenticate user and return JWT tokens",
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
            400: OpenApiResponse(description="Invalid credentials")
        },
        examples=[
            OpenApiExample(
                name="Login Example",
                value={
                    "username": "your_username",
                    "password": "password123"
                },
                request_only=True
            ),
            OpenApiExample(
                "Login Response Example",
                value={
                    "message": "Login successful",
                    "access": "jwt_access_token",
                    "refresh": "jwt_refresh_token",
                    "user": {
                        "id": 1,
                        "email": "user@example.com"
                    }
                },
                response_only=True
            )
        ]
    )
class LoginView(generics.GenericAPIView):
    # parser_classes = [FormParser, MultiPartParser]
    serializer_class = LoginSerializer


    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.username,
                "preferred_mood": user.preferred_mood
            }, 
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)






@extend_schema(
    summary="Logout User",
    request=UserSerializer,
    responses={200: OpenApiResponse(description="Logged out successfully")},
    examples=[
        OpenApiExample(
            name="Logout Request",
            value={
                "refresh": "your_refresh_token_here"
            },
            request_only=True
        )
    ]
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"})
        
        except TokenError as e:
            return Response(
                {"error": str(e)},  # 👈 SHOW REAL ERROR
                status=400
            )