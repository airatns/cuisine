from django.contrib import admin

from .models import FavoriteRecipe, Ingredient, Recipe, ShoppingCart, Tag


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_editable = ('name', 'measurement_unit')
    list_display_links = None
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'to_favorites')
    search_fields = ('name', 'author__username')
    list_filter = ('tags__name',)
    filter_horizontal = ['ingredients']
    list_editable = ('name',)
    list_display_links = None
    empty_value_display = '-empty-'

    def to_favorites(self, obj):
        """Сколько раз добавили в избранное.
        """
        return obj.favorite_recipe.count()


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name',)
    list_editable = ('name', 'color', 'slug')
    list_display_links = None
    empty_value_display = '-пусто-'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
