import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from recipes.models import Recipe, User, Ingredient, Follow, Favor, Cart


def ingredients(request):
    return JsonResponse(
        list(Ingredient.objects.filter(
            title__startswith=request.GET.get('query')).values()
        ),
        safe=False
    )


@login_required
@require_http_methods(['POST', 'DELETE'])
@csrf_protect
def subscription(request):
    data = json.loads(request.body)
    author = get_object_or_404(User, pk=data.get('id'))
    if request.method == 'POST':
        Follow.objects.create(user=request.user, author=author)
    else:
        follow = get_object_or_404(Follow, user=request.user, author=author)
        follow.delete()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['POST', 'DELETE'])
@csrf_protect
def favorites(request):
    data = json.loads(request.body)
    recipe = get_object_or_404(Recipe, pk=data.get('id'))
    if request.method == 'POST':
        Favor.objects.create(user=request.user, recipe=recipe)
    else:
        favor = get_object_or_404(Favor, user=request.user, recipe=recipe)
        favor.delete()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['POST', 'DELETE'])
@csrf_protect
def cart(request):
    data = json.loads(request.body)
    recipe = get_object_or_404(Recipe, pk=data.get('id'))
    if request.method == 'POST':
        Cart.objects.create(user=request.user, recipe=recipe)
    else:
        cart_item = get_object_or_404(Cart, user=request.user, recipe=recipe)
        cart_item.delete()
    return JsonResponse({'success': True})
