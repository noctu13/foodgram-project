import json
from recipes.models import Ingredient, Tag


with open('ingredients.json', 'r') as f:
    data = json.load(f)
for item in data:
    Ingredient.objects.create(**item)

Tag.objects.create(name='Завтрак', color='orange')
Tag.objects.create(name='Обед', color='green')
Tag.objects.create(name='Ужин', color='purple')
