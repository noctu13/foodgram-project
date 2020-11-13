from django.contrib import admin
from .models import Recipe, Ingredient  # , Favor, Follow


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "pub_date")
    search_fields = ("name",)
    list_filter = ("author", "name", "tags")
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")
    search_fields = ("name",)
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
