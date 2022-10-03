import os
from io import BytesIO

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import generics, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import (FavoriteRecipe, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingCart, Tag)
from .pagination import RecipePagination
from .permissions import AuthorOrReadOnly, ReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeListSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет по работе с Тегами.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет по работе с Ингредиентами.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = None
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    """Вьюсет по работе с Рецептами.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author', 'tags',)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        """Используем разные сериализаторы для GET и POST-запросов.
        """
        if self.request.method == 'GET':
            return RecipeListSerializer
        return RecipeCreateSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart')

        if is_favorited is not None:
            if is_favorited == '1':
                queryset = queryset.filter(favorite_recipe__user=user,)
            else:
                queryset = queryset.exclude(favorite_recipe__user=user,)

        if is_in_shopping_cart is not None:
            if is_in_shopping_cart == '1':
                queryset = queryset.filter(shopper_recipe__user=user,)
            else:
                queryset = queryset.exclude(shopper_recipe__user=user,)

        return queryset

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
@action(detail=False, url_path='favorite',
        permission_classes=(permissions.IsAuthenticated,),)
def fav_recipe(request, recipe_id):
    """Метод по добавлению и удалению рецептов в Избранное.
    """
    user = request.user
    if user.is_anonymous:
        return Response({
            'message': 'Пожалуйста, войдите в Вашу учетную систему',
        }, status=status.HTTP_401_UNAUTHORIZED)

    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        if FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
            return Response({
                'message': 'Этот рецепт уже находится в Избранном'
            }, status=status.HTTP_400_BAD_REQUEST)
        favorite_recipe = FavoriteRecipe.objects.create(user=user,
                                                        recipe=recipe)
        serializer = FavoriteSerializer(
            favorite_recipe, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        favorite_recipe = FavoriteRecipe.objects.filter(user=user,
                                                        recipe=recipe)
        if favorite_recipe.exists():
            favorite_recipe.delete()
            return Response({
                'message': 'Рецепт удален из Избранного',
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'message': 'Этого рецепта нет у Вас в Избранном'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST', 'DELETE'])
@action(detail=False, url_path='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,),)
def shopping_cart(request, recipe_id):
    """Метод для работы со Списком покупок (добавление, удаление рецептов).
    """
    user = request.user
    if user.is_anonymous:
        return Response({
            'message': 'Пожалуйста, войдите в Вашу учетную систему',
        }, status=status.HTTP_401_UNAUTHORIZED)

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
        return Response(
            {'message': 'Этого рецепта нет в Вашем Списке покупок'},
            status=status.HTTP_400_BAD_REQUEST
        )


class DownloadShoppingCart(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """Метод предоставляет pdf-файл со списком необходимых ингредиентов.
        """
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachement; filename="ShoppingCart.pdf"')
        folder = settings.FONTS_PATH
        ttf_file = os.path.join(folder, 'PT-Astra-Sans_Regular.ttf')
        pdfmetrics.registerFont(TTFont('PTAstraSans', ttf_file, 'UTF-8'))

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setFont('PTAstraSans', 15, leading=None)
        p.setFillColorRGB(0.29296875, 0.453125, 0.609375)
        p.drawString(210, 800, 'Ingredients for purchase')
        p.line(0, 780, 1000, 780)
        p.line(0, 778, 1000, 778)
        x1 = 20
        y1 = 750

        user = request.user
        ingredient_list = {}
        ingredients = IngredientForRecipe.objects.filter(
            recipe__shopper_recipe__user=user)
        for item in ingredients:
            key = (f'{item.ingredient.name} '
                   f'({item.ingredient.measurement_unit})'.capitalize())
            ingredient_list[key] = (
                ingredient_list.setdefault(key, 0) + item.amount)
        for key, value in ingredient_list.items():
            p.setFont('PTAstraSans', 10, leading=None)
            message = f'* {key} - {value}'
            p.drawString(x1, y1 - 12, message)
            y1 = y1 - 15

        p.setTitle('Ingredients for purchase')
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
