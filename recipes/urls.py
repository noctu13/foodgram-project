from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("api/ingredients/", views.api_ingredients),
    path("api/subscriptions/", views.api_subscription),
    path("api/favorites/", views.api_favorites),

    path("recipes/add/", views.recipe_add, name="recipe_add"),
    path("recipes/<int:recipe_id>/", views.recipe_view, name="recipe"),
    path(
        "recipes/<int:recipe_id>/edit/",
        views.recipe_edit,
        name="recipe_edit"
    ),
    path("users/<username>/", views.profile_view, name="profile"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("favorites/", views.favorites, name="favorites"),

    # path("cart/", views.cart_index, name="cart_index"),
    # path(
    #     "cart/add_recipe/<int:recipe_id>/",
    #     views.cart_add_recipe,
    #     name="cart_add_recipe"
    # ),
    # path(
    #     "cart/remove_recipe/<int:recipe_id>/",
    #     views.cart_remove_recipe,
    #     name="cart_remove_recipe"
    # ),

    path("about/", views.about, name="about"),
    path("spec/", views.spec, name="spec"),
]

error_patterns = [
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
