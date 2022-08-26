from rest_framework import serializers

from .models import Ingredient, IngredientForRecipe, Recipe, Tag
from users.serializers import UserListSerializer
from users.models import User
from users.serializers import UserListSerializer
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagID2ObjectSerializer(serializers.RelatedField):
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
    id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField(write_only=True)

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'quantity',)


class RecipeListSerializer(serializers.ModelSerializer):
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
        read_only_fields = ('author',)


class RecipeCreateSerializer(serializers.ModelSerializer):
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
        read_only_fields = ('author',)
    

    def create(self, validated_data):
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
        return recipe


    def to_representation(self, instance):
        serializer = RecipeListSerializer(
            instance,
            context=self.context
        )
        return serializer.data

