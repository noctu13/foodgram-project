from .models import Recipe
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'text', "image", "ingredients", "tags", "time"]
        labels = {
            'name': _('Название'),
            'text': _('Текст'),
            'image': _('Картинка'),
            'ingredients': _('Ингредиенты'),
            'tags': _('Метки'),
            'time': _('Время готовки'),
        }