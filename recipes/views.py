from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Recipe, User, Follow  # , Favor
from .forms import RecipeForm


class PageBack:
    def __init__(self, request, _list):
        if _list:
            self.paginator = Paginator(_list, 9)
            self.page = self.paginator.get_page(request.GET.get('page'))
        else:
            self.paginator = None
            self.page = None


def index(request):
    recipe_list = Recipe.objects.all().order_by("-pub_date")
    page_back = PageBack(request, recipe_list)
    return render(
        request,
        'index.html',
        {'page': page_back.page, 'paginator': page_back.paginator}
    )


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        return redirect('index')
    return render(request, "formRecipe.html", {"form": form})


def profile_view(request, username):
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(
        user=request.user,
        author=author
    ).exists() if request.user.is_authenticated else None
    recipe_list = author.recipes.all().order_by("-pub_date")
    paginator = Paginator(recipe_list, 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(
        request,
        "authorRecipe.html",
        {
            "author": author,
            'following': following,
            'page': page,
            'paginator': paginator
        }
    )


def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if author != recipe.author:
        raise Http404()
    form = RecipeForm(request.POST or None)
    return render(
        request,
        "formRecipe.html",
        {
            "author": author,
            "form": form,
            "recipe": recipe
        }
    )


@login_required
def recipe_edit(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        return redirect('recipe', username=username, recipe_id=recipe_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('recipe', username=username, recipe_id=recipe_id)
    return render(request, "formRecipe.html", {"form": form, "recipe": recipe})


# @login_required
# def add_comment(request, username, post_id):
#     author = get_object_or_404(User, username=username)
#     post = get_object_or_404(Post, pk=post_id)
#     if author != post.author:
#         raise Http404()
#     form = CommentForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.author = request.user
#         comment.save()
#         return redirect('post', username=username, post_id=post_id)
#     return redirect('post', username=username, post_id=post_id)


# @login_required
# def follow_index(request):
#     follow_list = Follow.objects.filter(user=request.user)
#     author_list = User.objects.filter(following__in=follow_list) if follow_list else None
#     post_list = Post.objects.filter(author__in=author_list).order_by("-pub_date") if author_list else []
#     paginator = Paginator(post_list, 10)
#     page = paginator.get_page(request.GET.get('page'))
#     return render(request, "follow.html", {'page': page, 'paginator': paginator})


# @login_required
# def profile_follow(request, username):
#     author = get_object_or_404(User, username=username)
#     if author != request.user and not Follow.objects.filter(user=request.user, author=author):
#         Follow.objects.create(user=request.user, author=author)
#     return redirect('profile', username=username)


# @login_required
# def profile_unfollow(request, username):
#     author = get_object_or_404(User, username=username)
#     follow = get_object_or_404(Follow, user=request.user, author=author)
#     follow.delete()
#     return redirect('profile', username=username)


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def permission_denied(request, exception):
    return render(request, "misc/403.html", {"path": request.path}, status=403)


def server_error(request):
    return render(request, "misc/500.html", status=500)


def about(request):
    return render(request, "about.html")


def spec(request):
    return render(request, "spec.html")
