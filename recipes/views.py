from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
import json

from .models import (
    Recipe, User, Tag, Composition, Ingredient, Follow, Favor
)
from .forms import RecipeForm


class PageBack:
    def __init__(self, request, _list):
        if _list:
            self.paginator = Paginator(_list, 6)
            self.page = self.paginator.get_page(request.GET.get('page'))
        else:
            self.paginator = None
            self.page = None


def index(request):
    tags = Tag.objects.all()
    get_data = request.GET.getlist('tag')
    query = Tag.objects.filter(
        name__in=get_data) if get_data else tags
    recipe_list = Recipe.objects.filter(
        tags__in=query).distinct().order_by('-pub_date')
    favor = Recipe.objects.filter(
        favorites__user=request.user
    ) if request.user.is_authenticated else None
    page_back = PageBack(request, recipe_list)
    return render(
        request,
        'index.html',
        {
            'page': page_back.page,
            'paginator': page_back.paginator,
            'tags': tags,
            'query': query,
            'favor': favor
        }
    )


@login_required
def favorites(request):
    tags = Tag.objects.all()
    get_data = request.GET.getlist('tag')
    query = Tag.objects.filter(
        name__in=get_data) if get_data else tags
    recipe_list = Recipe.objects.filter(
        favorites__user=request.user).filter(
        tags__in=query).distinct().order_by('-pub_date')
    favor = recipe_list
    page_back = PageBack(request, recipe_list)
    return render(
        request,
        'index.html',
        {
            'page': page_back.page,
            'paginator': page_back.paginator,
            'tags': tags,
            'query': query,
            'favor': favor
        }
    )


def api_ingredients(request):
    return JsonResponse(
        list(Ingredient.objects.filter(
            title__startswith=request.GET.get('query')).values()
        ),
        safe=False
    )


@login_required
@require_http_methods(['POST', 'DELETE'])
@csrf_protect
def api_subscription(request):
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
def api_favorites(request):
    data = json.loads(request.body)
    recipe = get_object_or_404(Recipe, pk=data.get('id'))
    if request.method == 'POST':
        Favor.objects.create(user=request.user, recipe=recipe)
    else:
        favor = get_object_or_404(Favor, user=request.user, recipe=recipe)
        favor.delete()
    return JsonResponse({'success': True})


def post_ingredient_save(recipe, post_data):
    for key in filter(
        lambda x: x.startswith('nameIngredient'), post_data
    ):
        item_id = key.split('_')[1]
        ingredient = Ingredient.objects.get(title=post_data[key])
        quantity = post_data['valueIngredient_' + item_id]
        Composition.objects.create(
            recipe=recipe, ingredient=ingredient, quantity=quantity
        )


@login_required
def recipe_add(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        form.save_m2m()
        post_ingredient_save(recipe, dict(request.POST.items()))
        return redirect('index')
    return render(request, 'recipeFormCreate.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        recipe.ingredients.clear()
        post_ingredient_save(recipe, dict(request.POST.items()))
        return redirect('recipe', recipe_id=recipe_id)
    return render(
        request,
        'recipeFormEdit.html',
        {'form': form}
    )


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    tags = Tag.objects.all()
    follow = Follow.objects.filter(
        user=request.user,
        author=recipe.author
    ).exists() if request.user.is_authenticated else None
    return render(
        request,
        'recipeView.html',
        {'recipe': recipe, 'tags': tags, 'follow': follow}
    )


def profile_view(request, username):
    author = get_object_or_404(User, username=username)
    tags = Tag.objects.all()
    get_data = request.GET.getlist('tag')
    query = Tag.objects.filter(
        name__in=get_data) if get_data else tags
    follow = Follow.objects.filter(
        user=request.user,
        author=author
    ).exists() if request.user.is_authenticated else None
    recipe_list = author.recipes.filter(
        tags__in=query).distinct().order_by('-pub_date')
    page_back = PageBack(request, recipe_list)
    return render(
        request,
        'author.html',
        {
            'page': page_back.page,
            'paginator': page_back.paginator,
            'tags': tags,
            'author': author,
            'query': query,
            'follow': follow
        }
    )


@login_required
def subscriptions(request):
    author_list = User.objects.filter(following__user=request.user)
    page_back = PageBack(request, author_list)
    return render(
        request,
        'subscriptions.html',
        {
            'page': page_back.page,
            'paginator': page_back.paginator
        }
    )


def page_not_found(request, exception):
    return render(
        request,
        'errors/404.html',
        {'path': request.path},
        status=404
    )


def permission_denied(request, exception):
    return render(
        request,
        'errors/403.html',
        {'path': request.path},
        status=403
    )


def server_error(request):
    return render(request, 'errors/500.html', status=500)


def about(request):
    return render(request, 'about.html')


def spec(request):
    return render(request, 'spec.html')
