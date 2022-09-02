from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view, action
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
import os
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4

from .models import FavoriteRecipe, Ingredient, Recipe, Tag, ShoppingCart, IngredientForRecipe
from .serializers import IngredientSerializer, RecipeListSerializer, RecipeCreateSerializer, TagSerializer
from .serializers import FavoriteSerializer, ShoppingCartSerializer


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


@api_view(['POST', 'DELETE'])
@action(detail=True, url_path='shopping_cart')
def shopping_cart(request, recipe_id):
    """Метод для работы со Списком покупок (добавление, удаление рецептов).
    """
    user = request.user
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
            return Response({
                'message': 'Этот рецепт уже находится в Списке покупок'
            }, status=status.HTTP_400_BAD_REQUEST)
        shopping_cart = ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = ShoppingCartSerializer(
            shopping_cart, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        shopping_cart = ShoppingCart.objects.filter(user=user, recipe=recipe)
        if shopping_cart.exists():
            shopping_cart.delete()
            return Response({
                'message': 'Рецепт удален из Списка покупок',
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
                'message': 'Этого рецепта нет в Вашем Списке покупок',
            }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET',])
def download_cart(request):
    """Метод предоставляет pdf-файл со списком необходимых ингредиентов.
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachement; filename="ShoppingCart.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Start writitng the PDF here
    p.setFont('Helvetica', 15, leading=None)
    p.setFillColorRGB(0.29296875, 0.453125, 0.609375)
    p.drawString(210, 800, 'Ingredients for purchase')
    p.line(0, 780, 1000, 780)
    p.line(0, 778, 1000, 778)
    x1 = 20
    y1 = 750

    # Data to print
    user = request.user
    ingredient_list = {}
    ingredients = IngredientForRecipe.objects.filter(recipe__shopper_recipe__user=user)

    for item in ingredients:
        key = f'{item.ingredient.name} ({item.ingredient.measurement_unit})'.capitalize()
        ingredient_list[key] = ingredient_list.setdefault(key, 0) + item.quantity
    for key, value in ingredient_list.items():
        p.setFont('Helvetica', 10, leading=None)
        message = f'* {key} - {value}'
        p.drawString(x1, y1-12, message)
        y1 = y1-15

    p.setTitle('Ingredients for purchase')
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
