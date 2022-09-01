from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиентов.
    """
    name = models.CharField(
        'Название ингредиента',
        max_length=150,
        # db_index=True,
    )
    measurement_unit = models.CharField(
        'Величина измерения ингредиента',
        max_length=15,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов.
    """
    name = models.CharField(
        'Теги',
        max_length=15,
        unique=True,
    )
    color = models.CharField(
        'Цветовой HEX-код',
        unique=True,
        max_length=7,
    )
    slug = models.SlugField(
        'Slug',
        unique=True,
        max_length=15,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов.
    """
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег', 
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientForRecipe',
        verbose_name='Ингредиенты',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
    )
    # image = models.ImageField(
    #     'Картинка',
    #     upload_to='../static/recipes/',
    # )
    text = models.TextField(
        'Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        help_text='Время приготовления в минутах',
        validators=[
            MinValueValidator(1),
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    """Модель ингредиентов для рецепта.
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingred_recipe',
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingred',
        verbose_name='Рецепт',
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиентов',
        validators=[
            MinValueValidator(1)
        ],
    )

    class Meta:
        verbose_name = 'Количество ингредиента для рецепта'
        verbose_name_plural = 'Количество ингредиентов для рецепта'

    def __str__(self):
        return (f'{self.ingredient.name} - {self.amount}'
                f'{self.ingredient.measurement_unit}')

