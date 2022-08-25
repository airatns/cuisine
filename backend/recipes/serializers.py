import json
from unicodedata import name

from rest_framework import serializers

from .models import MEASUREMENT_CHOICES, Ingredients, Recipes, Tags
from users.serializers import UserListSerializer
from users.models import User
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class TagsPK2Object(serializers.RelatedField):
    def to_internal_value(self, data):
        return data

    def to_representation(self, data):
        return {
            'id': data.id,
            'name': data.name,
            'color': data.color,
            'slug': data.slug
        }


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsSerializer(many=True)
    tags = TagsPK2Object(many=True, queryset=Tags.objects.all())

    class Meta:
        model = Recipes
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                #   'image',
                  'text',
                  'cooking_time',
        )
        read_only_fields = ('author',)

    
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            current_ingredient = Ingredients.objects.get(
                name=ingredient.get('name'),
                measurement_unit=ingredient.get('measurement_unit'),
            )
            recipe.ingredients.add(current_ingredient)
        return recipe
