from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    measure = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Recipe(models.Model):

    class Meal(models.TextChoices):
        BREAKFAST = 'B', _('Breakfast')
        LUNCH = 'L', _('Lunch')
        DINNER = 'D', _('Dinner')

    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='recipes',
    )
    tags = models.CharField(
        max_length=1,
        choices=Meal.choices,
    )
    time = models.PositiveIntegerField()
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        unique_together = ['user', 'author']

    def __str__(self):
        return "{} follow {}".format(self.user.username, self.author.username)


class Favor(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hunter'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='target'
    )

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return "{} favor {}".format(self.user.username, self.recipe.name)
