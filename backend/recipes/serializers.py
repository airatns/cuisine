from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.serializers import UserListSerializer

from .models import (FavoriteRecipe, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, в каком формате ожидаем увидеть
    данные по Тегам, извлеченные из БД.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, в каком формате ожидаем увидеть
    данные по Ингредиентам, извлеченные из БД.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagID2ObjectSerializer(serializers.RelatedField):
    """Сериализатор переопределяет, в каком формате ожидаем увидеть
    данные по Тегам для Рецепта, извлеченные из БД.
    """
    def to_internal_value(self, data):
        return data

    def to_representation(self, data):
        return {
            'id': data.id,
            'name': data.name,
            'color': data.color,
            'slug': data.slug,
        }


class IngredientForRecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, в каком формате ожидаем увидеть
    данные по Ингредиентам для Рецепта, извлеченные из БД.
    """
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class IngredientForRecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, какие поля будут заполнены
    по Ингредиентам для Рецепта при добавлении нового объекта в БД и их типы.
    """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, в каком формате ожидаем увидеть
    данные по Рецептам, извлеченные из БД.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = UserListSerializer(read_only=True)
    ingredients = IngredientForRecipeListSerializer(
        source='recipe_ingred',
        many=True,
        read_only=True
    )
    image = Base64ImageField(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time',)

    def get_is_favorited(self, obj):
        """Метод определяет, находится ли Рецепт в списке Избранного.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        """Метод определяет, находится ли Рецепт в списке Покупок.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, какие поля будут заполнены
    по Рецептам при добавлении нового объекта в БД и их типы.
    """
    tags = TagID2ObjectSerializer(many=True, queryset=Tag.objects.all())
    author = UserListSerializer(read_only=True)
    ingredients = IngredientForRecipeCreateSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',)

    def create(self, validated_data):
        """Метод по созданию нового объекта Рецептов (POST-запрос).
        """
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        objs = [
            IngredientForRecipe(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    pk=ingredient.get('id')
                ),
                amount=ingredient.get('amount'),
            )
            for ingredient in ingredients
        ]
        IngredientForRecipe.objects.bulk_create(objs)

        recipe.save()
        return recipe

    def update(self, recipe, validated_data):
        """Метод по изменению объекта Рецептов (PATCH-запрос).
        """
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe.tags.set(tags)

        IngredientForRecipe.objects.filter(recipe=recipe).delete()

        objs = [
            IngredientForRecipe(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient,
                    pk=ingredient.get('id')
                ),
                amount=ingredient.get('amount'),
            )
            for ingredient in ingredients
        ]
        IngredientForRecipe.objects.bulk_create(objs)

        recipe.save()
        return recipe

    def to_representation(self, instance):
        """Метод переопределяет, в каком формате ожидаем увидеть
        данные по Рецептам, извлеченные из БД.
        """
        serializer = RecipeListSerializer(
            instance,
            context=self.context
        )
        return serializer.data

    def validate_name(self, name):
        """Валидация на название Рецепта.
        Если у данного автора уже есть Рецепт с таким названием ,
        создание нового Рецепта невозможно.
        """
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            recipes_by_user = Recipe.objects.filter(author=user)
            for recipe in recipes_by_user:
                if recipe.name.lower() == name.lower():
                    raise serializers.ValidationError(
                        'Рецепт с таким названием уже был опубликован Вами!'
                    )
        return name

    def validate_ingredients(self, ingredients):
        """Валидация на дублирование Ингредиента.
        Если несколько раз введен один и тот же Ингредиент,
        его количество суммируется.
        """
        dict = {}
        for ingredient in ingredients:
            if ingredient['id'] in dict:
                dict[ingredient['id']] += ingredient['amount']
            else:
                dict[ingredient['id']] = ingredient['amount']
        return [
            {'id': key,
             'amount': value} for key, value in dict.items()
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор на вывод на экран данных об Избранных рецептах.
    """
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ReadOnlyField(source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор на вывод на экран данных о рецептах из Списка покупок.
    """
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.ReadOnlyField(source='recipe.image')
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'name', 'image', 'cooking_time',)

    def validate_ingredients(self, ingredients):
        """Валидация на дублирование Ингредиента.
        Если несколько раз введен один и тот же Ингредиент,
        его количество суммируется.
        """
        dict = {}
        for ingredient in ingredients:
            if ingredient['id'] in dict:
                dict[ingredient['id']] += ingredient['amount']
            else:
                dict[ingredient['id']] = ingredient['amount']
        return [
            {'id': key,
             'amount': value} for key, value in dict.items()
        ]
