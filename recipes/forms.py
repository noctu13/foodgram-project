from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=True
    )

    class Meta:
        model = Recipe
        fields = ['name', 'text', "image", "time"]
        labels = {
            'name': _('Название'),
            'text': _('Текст'),
            'image': _('Картинка'),
            'time': _('Время готовки'),
        }
