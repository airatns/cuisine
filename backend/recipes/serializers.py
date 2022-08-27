from rest_framework import serializers

from .models import Ingredient, IngredientForRecipe, Recipe, Tag
from users.serializers import UserListSerializer
from users.models import User
from users.serializers import UserListSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from drf_extra_fields.fields import Base64ImageField
from rest_framework.response import Response

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
    данные по Тегам, извлеченные из БД.
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
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'quantity',)


class IngredientForRecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, какие поля будут заполнены
    по Ингредиентам для Рецепта при добавлении нового объекта в БД и их типы.
    """
    id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'quantity',)


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, в каком формате ожидаем увидеть
    данные по Рецептам, извлеченные из БД.
    """
    tags = TagSerializer(many=True, read_only=True)
    author = UserListSerializer(read_only=True)
    ingredients = IngredientForRecipeListSerializer(
        source='ingred_recipe',
        many=True,
        read_only=True
    )
    # image = Base64ImageField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                #   'is_favorited',
                #   'is_in_shopping_cart',
                  'name',
                #   'image',
                  'text',
                  'cooking_time',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор определяет, какие поля будут заполнены
    по Рецептам при добавлении нового объекта в БД и их типы.
    """
    tags = TagID2ObjectSerializer(many=True, queryset=Tag.objects.all())
    author = UserListSerializer(read_only=True)
    ingredients = IngredientForRecipeCreateSerializer(many=True)
    # image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                #   'is_favorited',
                #   'is_in_shopping_cart',
                  'name',
                #   'image',
                  'text',
                  'cooking_time',
        )

    def create(self, validated_data):
        """Метод по созданию нового объекта Рецептов (POST-запрос).
        """
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            id = ingredient.get('id')
            quantity = ingredient.get('quantity')
            current_ingredient = get_object_or_404(Ingredient, pk=id)
            IngredientForRecipe.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                quantity=quantity,
            )
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        """Метод по изменению объекта Рецептов (PATCH-запрос).
        """
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        for item in validated_data:
            if Recipe._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.tags.set(tags)

        IngredientForRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            id = ingredient.get('id')
            quantity = ingredient.get('quantity')
            current_ingredient = get_object_or_404(Ingredient, pk=id)
            IngredientForRecipe.objects.create(
                recipe=instance,
                ingredient=current_ingredient,
                quantity=quantity,
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        """Метод переопределяет, в каком формате ожидаем увидеть
        данные по Рецептам, извлеченные из БД.
        """
        serializer = RecipeListSerializer(
            instance,
            context=self.context
        )
        return serializer.data


    def validate_name(self, value):
        """Валидация на название Рецепта.
        Если у данного автора уже есть Рецепт с таким названием ,
        создание нового Рецепта невозможно.
        """
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            recipes_by_user = Recipe.objects.filter(author=user)
            for recipe in recipes_by_user:
                if recipe.name.lower() == value.lower():
                    raise serializers.ValidationError(
                        'Рецепт с таким названием уже был опубликован Вами!'
                    )
        return value

