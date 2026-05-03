from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'preferred_mood', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def validate(self,data):
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError({
                    "password": "passwords do not match"
                })
            
            return data
            
    def create(self, validated_data):
            validated_data.pop('confirm_password')

            return User.objects.create_user(
                    username=validated_data['username'],
                    email=validated_data.get('email'),
                    password=validated_data['password']
                )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data["user"] = user
        return data