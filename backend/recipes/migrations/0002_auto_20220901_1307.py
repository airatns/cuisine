# Generated by Django 2.2.19 on 2022-09-01 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipe', to='recipes.Recipe', verbose_name='Избранный рецепта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_favorite', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
            },
        ),
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique recipe'),
        ),
    ]
