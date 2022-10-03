import django_filters

from .models import Ingredient, Tag


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
    slug = django_filters.ChoiceFilter(
        field_name='slug',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Tag
        fields = ('slug',)
