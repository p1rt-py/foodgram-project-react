from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Cart, Favorite, Ingredient, IngredientAmount, Recipe, Tag


@admin.register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color')


@admin.register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')


@admin.register(IngredientAmount)
class IngredientAmountAdmin(ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('recipe__name',)
    list_filter = ('recipe__tags',)


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('recipe__name',)
    list_filter = ('recipe__tags',)
