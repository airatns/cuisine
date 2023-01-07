import django_filters
from users.models import User

from .models import Ingredient, Recipe, Tag


class IngredientFilter(django_filters.FilterSet):
    """Custom filter to find an ingredient in the list.
    """
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Custom filter to find a recipe by tags.
    """
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    author = django_filters.ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
