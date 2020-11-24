from django.urls import path
from . import views

urlpatterns = [
    path("ingredients/", views.api_ingredients),
    path("subscriptions/", views.api_subscription),
    path("favorites/", views.api_favorites),
    path("cart/", views.cart),
]
