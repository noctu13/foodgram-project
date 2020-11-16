from django.contrib import admin
from .models import Tag, Recipe, Ingredient, Composition


class CompositionInline(admin.TabularInline):
    model = Composition
    autocomplete_fields = ['ingredient']
    extra = 1


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "pub_date")
    search_fields = ("name",)
    list_filter = ("author", "name", "tags")
    filter_horizontal = ("tags",)
    empty_value_display = '-пусто-'
    inlines = (CompositionInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    search_fields = ("title",)
    empty_value_display = '-пусто-'


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredient")
    search_fields = ("recipe", "ingredient")
    empty_value_display = '-пусто-'
