from rest_framework import serializers
from .models import Subscription, User


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

class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор на вывод на экран данных о текущих подписках на авторов.
    """
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    # recipes = serializers.SerializerMethodField()
    # recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    # def get_recipes(self, obj):
    #     request = self.context.get('request')
    #     limit = request.GET.get('recipes_limit')
    #     queryset = Recipe.objects.filter(author=obj.author)
    #     if limit:
    #         queryset = queryset[:int(limit)]
    #     return CropRecipeSerializer(queryset, many=True).data

    # def get_recipes_count(self, obj):
    #     return Recipe.objects.filter(author=obj.author).count()