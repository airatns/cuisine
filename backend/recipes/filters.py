import django_filters

from .models import Ingredient, Recipe, Tag


class IngredientFilter(django_filters.FilterSet):
    """Кастомный фильтр на поиск ингредиента
    по вхождению в произвольном месте.
    """
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeTagFilter(django_filters.FilterSet):
    """Кастомный фильтр Рецепта по тегам.
    """
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
    )

    class Meta:
        model = Recipe
        fields = ('tags',)
