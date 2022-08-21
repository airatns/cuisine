from rest_framework import serializers

from .models import Ingredients, Tags


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'quantity', 'measurement_unit')
