from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_protect

from .models import Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeListSerializer, RecipeCreateSerializer, TagSerializer



class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет по работе с Тегами.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет по работе с Ингредиентами.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    """Вьюсет по работе с Рецептами.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer

    def get_serializer_class(self):
        """Используем разные сериализаторы для GET и POST-запросов.
        """
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer
        
    def perform_create(self, serializer):
        """В поле Author передадим объект пользователя, отправшего запрос,
        при создании объекта Рецепта.
        """
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """В поле Author передадим объект пользователя, отправшего запрос,
        при изменении объекта Рецепта.
        """
        serializer.save(author=self.request.user)


