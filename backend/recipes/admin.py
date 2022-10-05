from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientForRecipeInline(admin.TabularInline):
    model = IngredientForRecipe
    extra = 0


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
    readonly_fields = ('pub_date',)
    list_filter = ('tags__name',)
    list_editable = ('name',)
    list_display_links = None
    empty_value_display = '-empty-'
    inlines = (IngredientForRecipeInline,)

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
