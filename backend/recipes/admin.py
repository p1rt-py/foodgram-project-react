from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Cart, Favorite, Ingredient, Recipe, Tag


class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color')


class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)


class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')


class IngredientAmountAdmin(ModelAdmin):
    pass


class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('recipe__name',)
    list_filter = ('recipe__tags',)


class CartAdmin(ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('recipe__name',)
    list_filter = ('recipe__tags',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
