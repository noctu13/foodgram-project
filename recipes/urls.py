from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("recipes/add/", views.recipe_add, name="recipe_add"),
    path("recipes/<int:recipe_id>/", views.recipe_view, name="recipe"),
    path(
        "recipes/<int:recipe_id>/edit/",
        views.recipe_edit,
        name="recipe_edit"
    ),
    path(
        "recipes/<int:recipe_id>/delete/",
        views.recipe_delete,
        name="recipe_delete"
    ),
    path("users/<username>/", views.profile_view, name="profile"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("favorites/", views.favorites, name="favorites"),
    path("purchases/", views.purchases, name="purchases"),
    path("purchases/text/", views.get_cart_text, name="get_cart_text"),

    path("about/", views.about, name="about"),
    path("spec/", views.spec, name="spec"),

    path(
        "404/",
        views.page_not_found,
        name="page_not_found",
        kwargs={'exception': Exception("Page not Found!")}
    ),
    path(
        "403/",
        views.permission_denied,
        name="permission_denied",
        kwargs={'exception': Exception("Permission denied!")}
    ),
    path("500/", views.server_error, name="server_error"),
]
