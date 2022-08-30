from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import User, Subscribe



class UserRegistrSerializer(serializers.ModelSerializer):
    """Сериализатор на создание пользователя.
    """
    is_subscribed = serializers.BooleanField(default=False)

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
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'last_name', 'first_name', 'is_subscribed')
    
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscribe.objects.filter(user=user, author=obj).exists()



class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    # recipes = serializers.SerializerMethodField()
    # recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(user=obj.user, author=obj.author).exists()