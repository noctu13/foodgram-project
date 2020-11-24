from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Sum

from .models import (
    Recipe, User, Tag, Composition, Ingredient, Follow,
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
    cart = Recipe.objects.filter(
        carts__user=request.user
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
            'favor': favor,
            'cart': cart
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
    return render(request, 'recipe_form_create.html', {'form': form})


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
        'recipe_form_edit.html',
        {'form': form}
    )


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe_id)
    recipe.delete()
    return redirect('index')


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    tags = Tag.objects.all()
    follow = Follow.objects.filter(
        user=request.user,
        author=recipe.author
    ).exists() if request.user.is_authenticated else None
    favor = Recipe.objects.filter(
        favorites__user=request.user
    ) if request.user.is_authenticated else None
    cart = Recipe.objects.filter(
        carts__user=request.user
    ) if request.user.is_authenticated else None
    return render(
        request,
        'recipe.html',
        {
            'recipe': recipe,
            'tags': tags,
            'follow': follow,
            'favor': favor,
            'cart': cart
        }
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
    favor = Recipe.objects.filter(
        favorites__user=request.user
    ) if request.user.is_authenticated else None
    cart = Recipe.objects.filter(
        carts__user=request.user
    ) if request.user.is_authenticated else None
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
            'follow': follow,
            'favor': favor,
            'cart': cart
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


@login_required
def purchases(request):
    cart = Recipe.objects.filter(carts__user=request.user)
    return render(request, 'purchases.html', {'cart': cart})


@login_required
def get_cart_text(request):
    filename = 'cart.txt'
    content = ''
    cart = Recipe.objects.filter(carts__user=request.user)
    compositions = Composition.objects.filter(
        recipe__in=cart).values('ingredient').annotate(value=Sum('quantity'))
    for item in compositions:
        ingredient = Ingredient.objects.get(pk=item['ingredient'])
        content += str(ingredient) + ', ' + str(item['value']) + '\n'
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    return response


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
