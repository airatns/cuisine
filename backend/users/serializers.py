from rest_framework import serializers
from .models import User


class UserRegistrSerializer(serializers.ModelSerializer):
    """Сериализатор на создание пользователя.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'last_name', 'first_name', 'is_subscribed')

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            last_name=self.validated_data['last_name'],
            first_name=self.validated_data['first_name'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор на вывод на экран данных о пользователе(-ях).
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_name', 'first_name', 'is_subscribed')

