from django_filters import AllValuesMultipleFilter
from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget
from recipes.models import Recipe
from rest_framework.filters import SearchFilter


class TagFavoritShopingFilter(filters.FilterSet):
    is_in_shopping_cart = filters.BooleanFilter(widget=BooleanWidget())
    is_favorited = filters.BooleanFilter(widget=BooleanWidget())
    tags = AllValuesMultipleFilter(field_name="tags__slug")
    author = AllValuesMultipleFilter(field_name="author__id")

    class Meta:
        model = Recipe
        fields = ["author__id", "tags__slug", "is_favorited", "is_in_shopping_cart"]


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'

# from django_filters import AllValuesMultipleFilter
# from django_filters.rest_framework import FilterSet, filters
#
# from recipes.models import Recipe
#
#
# class RecipeFilter(FilterSet):
#     is_in_shopping_cart = filters.BooleanFilter(
#         method='get_is_in_shopping_cart',
#         label='shopping_cart',)
#     is_favorited = filters.BooleanFilter(
#         method='get_favorite',
#         label='favorite',
#     )
#     tags = AllValuesMultipleFilter(
#         field_name='tags__slug',
#         label='tags'
#     )
#
#     def get_favorite(self, queryset, name, value):
#         if value:
#             return queryset.filter(in_favorite__user=self.request.user)
#         return queryset.exclude(
#             in_favorite__user=self.request.user
#         )
#
#     def get_is_in_shopping_cart(self, queryset, name, value):
#         if value:
#             return Recipe.objects.filter(
#                 shopping_recipe__user=self.request.user
#             )
#
#     class Meta:
#         model = Recipe
#         fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
