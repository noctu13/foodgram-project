from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Recipe, Tag


class RecipeForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form__input'})
        self.fields['time'].widget.attrs.update({'class': 'form__input'})
        self.fields['text'].widget.attrs.update({'class': 'form__textarea'})

    class Meta:
        model = Recipe
        fields = ['name', 'tags', 'text', "image", "time"]
        labels = {
            'name': _('Название'),
            'tags': _("Теги"),
            'text': _('Текст'),
            'image': _('Картинка'),
            'time': _('Время готовки'),
        }
