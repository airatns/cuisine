from django.contrib import admin
from .models import Ingredient, Recipe, Tag


@admin.register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    list_editable = ('name', 'measurement_unit')
    list_display_links = None
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'author')
    list_filter = ('author', 'name', 'tags')
    list_editable = ('name', 'text')
    list_display_links = None
    empty_value_display = '-пусто-'

    def to_favorites(self):
        """Сколько раз добавили в избранное.
        """
        pass


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    list_display_links = None
    empty_value_display = '-пусто-'

