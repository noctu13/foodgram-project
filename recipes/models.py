from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    title = models.CharField(max_length=20)
    dimension = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='Composition'
    )
    tags = models.ManyToManyField(Tag)
    time = models.PositiveIntegerField()
    pub_date = models.DateTimeField(
        'date published',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.name


class Composition(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='compositions'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='compositions'
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ['recipe', 'ingredient']

    def __str__(self):
        return "{} contain {}".format(self.recipe.name, self.ingredient.title)


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
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return "{} favor {}".format(self.user.username, self.recipe.name)


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts'
    )

    class Meta:
        unique_together = ['user', 'recipe']

    def __str__(self):
        return "{} add to cart {}".format(
            self.user.username, self.recipe.name
        )
