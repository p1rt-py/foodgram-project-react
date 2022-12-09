# from django.contrib.auth import get_user_model
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
#
# User = get_user_model()
#
#
# def download_cart(request):
#     user = get_object_or_404(User, username=request.user.username)
#     shopping_cart = user.cart.all()
#     shopping_dict = {}
#     for num in shopping_cart:
#         ingredients_queryset = num.recipe.ingredient.all()
#         for ingredient in ingredients_queryset:
#             name = ingredient.ingredients.name
#             amount = ingredient.amount
#             measurement_unit = ingredient.ingredients.measurement_unit
#             if name not in shopping_dict:
#                 shopping_dict[name] = {
#                     'measurement_unit': measurement_unit,
#                     'amount': amount}
#             else:
#                 shopping_dict[name]['amount'] = (
#                     shopping_dict[name]['amount'] + amount
#                 )
#     shopping_list = []
#     for index, key in enumerate(shopping_dict, start=1):
#         shopping_list.append(
#             f'{index}. {key} - {shopping_dict[key]["amount"]} '
#             f'{shopping_dict[key]["measurement_unit"]}\n')
#     filename = 'shopping_cart.txt'
#     response = HttpResponse(shopping_list, content_type='text/plain')
#     response['Content-Disposition'] = f'attachment; filename={filename}'
#     return response
