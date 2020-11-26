# Generated by Django 3.1.2 on 2020-11-26 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Composition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'композицию',
                'verbose_name_plural': 'композиции',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('dimension', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('color', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': 'теги',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/')),
                ('time', models.PositiveIntegerField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date published')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='recipes.Composition', to='recipes.Ingredient')),
                ('tags', models.ManyToManyField(to='recipes.Tag')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
            },
        ),
        migrations.AddField(
            model_name='composition',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='compositions', to='recipes.ingredient'),
        ),
        migrations.AddField(
            model_name='composition',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compositions', to='recipes.recipe'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'подписку',
                'verbose_name_plural': 'подписки',
                'unique_together': {('user', 'author')},
            },
        ),
        migrations.CreateModel(
            name='Favor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'избранное',
                'verbose_name_plural': 'избранное',
                'unique_together': {('user', 'recipe')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='composition',
            unique_together={('recipe', 'ingredient')},
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'покупку',
                'verbose_name_plural': 'список покупок',
                'unique_together': {('user', 'recipe')},
            },
        ),
    ]
