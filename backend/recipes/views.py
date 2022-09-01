from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404

from .models import FavoriteRecipe, Ingredient, Recipe, Tag
from .serializers import IngredientSerializer, RecipeListSerializer, RecipeCreateSerializer, TagSerializer
from .serializers import FavoriteSerializer


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


@api_view(['POST', 'DELETE'])
@action(detail=True, url_path='favorite')
def fav_recipe(request, recipe_id):
    """Метод по добавлению и удалению рецептов в Избранное.
    """
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        if FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
            return Response({
                'message': 'Этот рецепт уже находится в Избранном'
            }, status=status.HTTP_400_BAD_REQUEST)
        favorite_recipe = FavoriteRecipe.objects.create(user=user, recipe=recipe)
        serializer = FavoriteSerializer(
            favorite_recipe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        favorite_recipe = FavoriteRecipe.objects.filter(user=user, recipe=recipe)
        if favorite_recipe.exists():
            favorite_recipe.delete()
            return Response({
                'message': 'Рецепт удален из Избранного',
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
                'message': 'Этого рецепта нет у Вас в Избранном',
            }, status=status.HTTP_400_BAD_REQUEST)
