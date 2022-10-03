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
    # author = django_filters.NumberFilter(
    #     field_name='author__id',
    #     lookup_expr='exact'
    # )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    # is_favorited = django_filters.BooleanFilter(field_name='is_favorited')
    # is_in_shopping_cart = django_filters.BooleanFilter(
    #     field_name='is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags']

    # def get_is_favorited(self, queryset, name, value):
    #     if value:
    #         return Recipe.objects.filter(
    #             favorite_recipe__user=self.request.user
    #         )
    #     return Recipe.objects.all()

    # def get_is_in_shopping_cart(self, queryset, name, value):
    #     if value:
    #         return Recipe.objects.filter(
    #             shopper_recipe__user=self.request.user)
    #     return Recipe.objects.all()
