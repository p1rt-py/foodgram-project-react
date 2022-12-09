from django.contrib.auth import get_user_model
from django.db.models import BooleanField, Exists, OuterRef, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (FollowSerializer, IngredientSerializer,
                             RecipeReadSerializer, RecipeWriteSerializer,
                             ShortRecipeSerializer, TagSerializer)
from users.models import Follow

User = get_user_model()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class FollowViewSet(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(
        methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': 'Ошибка подписки, нельзя подписываться на себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'Ошибка подписки, вы уже подписаны на пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({
                'errors': 'Ошибка отписки, нельзя отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.filter(user=user, author=author)
        if not follow.exists():
            return Response({
                'errors': 'Ошибка отписки, вы уже отписались'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    filter_class = RecipeFilter
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Recipe.objects.all()

        if user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(Favorite.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
                ),
                is_in_shopping_cart=Exists(Cart.objects.filter(
                    user=user, recipe__pk=OuterRef('pk'))
                )
            )
        else:
            queryset = queryset.annotate(
                is_favorited=Value(False, output_field=BooleanField()),
                is_in_shopping_cart=Value(False, output_field=BooleanField())
            )
        return queryset

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        return self.add_obj(Favorite, request.user, pk)

    @favorite.mapping.delete
    def del_from_favorite(self, request, pk=None):
        return self.delete_obj(Favorite, request.user, pk)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        return self.add_obj(Cart, request.user, pk)

    @shopping_cart.mapping.delete
    def del_from_shopping_cart(self, request, pk=None):
        return self.delete_obj(Cart, request.user, pk)

    def add_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Ошибка добавления рецепта в список'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Ошибка удаления рецепта из списка'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = get_object_or_404(User, username=request.user.username)
        shopping_cart = user.cart.all()
        shopping_dict = {}
        for num in shopping_cart:
            ingredients_queryset = num.recipe.ingredient.all()
            for ingredient in ingredients_queryset:
                name = ingredient.ingredients.name
                amount = ingredient.amount
                measurement_unit = ingredient.ingredients.measurement_unit
                if name not in shopping_dict:
                    shopping_dict[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount}
                else:
                    shopping_dict[name]['amount'] = (
                        shopping_dict[name]['amount'] + amount)

        shopping_list = []
        for index, key in enumerate(shopping_dict, start=1):
            shopping_list.append(
                f'{index}. {key} - {shopping_dict[key]["amount"]} '
                f'{shopping_dict[key]["measurement_unit"]}\n')
        filename = 'shopping_cart.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

# from django.contrib.auth import get_user_model
# from django.db.models import BooleanField, Exists, OuterRef, Value
# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
# from djoser.views import UserViewSet
# from rest_framework import status, viewsets
# from rest_framework.decorators import action
# from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
# from rest_framework.response import Response
#
# from .utils import download_cart
# from .filters import RecipeFilter
# from .pagination import LimitPageNumberPagination
# from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
# from .serializers import (FollowSerializer, IngredientSerializer,
#                              RecipeGetSerializer, RecipePostSerializer,
#                              ShortRecipeSerializer, TagSerializer)
# from recipes.models import Cart, Favorite, Ingredient, Recipe, Tag
# from users.models import Follow
#
# User = get_user_model()
#
#
# class FollowViewSet(UserViewSet):
#     pagination_class = LimitPageNumberPagination
#
#     @action(
#         methods=['post', 'delete'],
#         detail=True,
#         permission_classes=[IsAuthenticated]
#     )
#     def subscribe(self, request, id=None):
#         user = request.user
#         author = get_object_or_404(User, id=id)
#         if request.method == 'POST':
#             if user == author:
#                 return Response({
#                     'errors': 'Нельзя подписываться на себя'
#                 },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             if Follow.objects.filter(user=user, author=author).exists():
#                 return Response({
#                     'errors': 'Уже подписаны на пользователя'
#                 },
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             follow = Follow.objects.create(user=user, author=author)
#             serializer = FollowSerializer(
#                 follow, context={'request': request}
#             )
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         if request.method == 'DELETE':
#             if user == author:
#                 return Response({
#                     'errors': 'Нельзя отписываться от самого себя'
#                 }, status=status.HTTP_400_BAD_REQUEST)
#             if not Follow.objects.filter(user=user, author=author).exists():
#                 return Response(
#                     {'errors': 'Вы не подписаны'},
#                     status.HTTP_400_BAD_REQUEST
#                 )
#             Follow.objects.filter(user=user, author=author).delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#
#     @action(detail=False, permission_classes=[IsAuthenticated])
#     def subscriptions(self, request):
#         user = request.user
#         queryset = Follow.objects.filter(user=user)
#         pages = self.paginate_queryset(queryset)
#         serializer = FollowSerializer(
#             pages,
#             many=True,
#             context={'request': request}
#         )
#         return self.get_paginated_response(serializer.data)
#
#
# class TagsViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Tag.objects.all()
#     permission_classes = (IsAdminOrReadOnly,)
#     serializer_class = TagSerializer
#     pagination_class = None
#
#
# class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Ingredient.objects.all()
#     permission_classes = (IsAdminOrReadOnly,)
#     serializer_class = IngredientSerializer
#     filter_backends = [DjangoFilterBackend]
#     search_fields = ('^name',)
#     pagination_class = None
#
#
# class RecipeViewSet(viewsets.ModelViewSet):
#     queryset = Recipe.objects.all()
#     filter_class = RecipeFilter
#     permission_classes = [IsOwnerOrReadOnly]
#     pagination_class = LimitPageNumberPagination
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#     def get_serializer_class(self):
#         if self.request.method in SAFE_METHODS:
#             return RecipeGetSerializer
#         return RecipePostSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         queryset = Recipe.objects.all()
#
#         if user.is_authenticated:
#             queryset = queryset.annotate(
#                 is_favorited=Exists(Favorite.objects.filter(
#                     user=user, recipe__pk=OuterRef('pk'))
#                 ),
#                 is_in_shopping_cart=Exists(Cart.objects.filter(
#                     user=user, recipe__pk=OuterRef('pk'))
#                 )
#             )
#         else:
#             queryset = queryset.annotate(
#                 is_favorited=Value(False, output_field=BooleanField()),
#                 is_in_shopping_cart=Value(False, output_field=BooleanField())
#             )
#         return queryset
#
#     @action(detail=True, methods=['post'],
#             permission_classes=[IsAuthenticated])
#     def favorite(self, request, pk=None):
#         return self.add_obj(Favorite, request.user, pk)
#
#     @favorite.mapping.delete
#     def del_from_favorite(self, request, pk=None):
#         return self.delete_obj(Favorite, request.user, pk)
#
#     @action(detail=True, methods=['post'],
#             permission_classes=[IsAuthenticated])
#     def shopping_cart(self, request, pk=None):
#         return self.add_obj(Cart, request.user, pk)
#
#     @shopping_cart.mapping.delete
#     def del_from_shopping_cart(self, request, pk=None):
#         return self.delete_obj(Cart, request.user, pk)
#
#     def add_obj(self, model, user, pk):
#         if model.objects.filter(user=user, recipe__id=pk).exists():
#             return Response({
#                 'errors': 'Ошибка добавления рецепта в список'
#             }, status=status.HTTP_400_BAD_REQUEST)
#         recipe = get_object_or_404(Recipe, id=pk)
#         model.objects.create(user=user, recipe=recipe)
#         serializer = ShortRecipeSerializer(recipe)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     def delete_obj(self, model, user, pk):
#         obj = model.objects.filter(user=user, recipe__id=pk)
#         if obj.exists():
#             obj.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response({
#             'errors': 'Ошибка удаления рецепта из списка'
#         }, status=status.HTTP_400_BAD_REQUEST)
#
#     @action(detail=False, permission_classes=[IsAuthenticated])
#     def download_shopping_cart(self, request):
#         return download_cart(request)
