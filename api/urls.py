from django.urls import path
from . import views

urlpatterns = [
    path("ingredients/", views.ingredients),
    path("subscriptions/", views.subscription),
    path("favorites/", views.favorites),
    path("cart/", views.cart),
]
