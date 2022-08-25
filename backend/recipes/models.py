from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


MEASUREMENT_CHOICES = (
    ('банка', 'банка'),
    ('батон', 'батон'),
    ('бутылка', 'бутылка'),
    ('веточка', 'веточка'),
    ('г', 'г'),
    ('горсть', 'горсть'),
    ('долька', 'долька'),
    ('звездочка', 'звездочка'),
    ('зубчик', 'зубчик'),
    ('капля', 'капля'),
    ('кг', 'кг'),
    ('кусок', 'кусок'),
    ('л', 'л'),
    ('лист', 'лист'),
    ('мл', 'мл'),
    ('пакет', 'пакет'),
    ('пакетик', 'пакетик'),
    ('пачка', 'пачка'),
    ('пласт', 'пласт'),
    ('по вкусу', 'по вкусу'),
    ('пучок', 'пучок'),
    ('ст. л.', 'ст. л.'),
    ('стакан', 'стакан'),
    ('стебель', 'стебель'),
    ('стручок', 'стручок'),
    ('тушка', 'тушка'),
    ('упаковка', 'упаковка'),
    ('ч. л.', 'ч. л.'),
    ('шт.', 'шт.'),
    ('щепотка', 'щепотка'),
)

class Ingredients(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=150,
        unique=True,
        db_index=True,
    )
    # quantity = models.IntegerField(
    #     'Количество ингредиента',
    #     validators=[
    #         MinValueValidator(0),
    #         MaxValueValidator(1000)
    #     ],
    # )
    measurement_unit = models.CharField(
        'Величина измерения ингредиента',
        max_length=15,
        choices=MEASUREMENT_CHOICES,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(
        'Теги',
        max_length=15,
        unique=True,
        db_index=True,
    )
    color = models.CharField(
        'Цветовой HEX-код',
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


class Recipes(models.Model):
    tags = models.ManyToManyField(
        Tags,
        related_name='recipes',
        verbose_name='Тег', 
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
    )
    # image = models.ImageField(
    #     'Картинка',
    #     upload_to='../static/recipes/',
    #     width_field=None,
    #     height_field=None,
    # )
    text = models.TextField(
        'Описание рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления в минутах',
        help_text='Время приготовления в минутах',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10080)
        ]
    )
    is_favorited = models.BooleanField(
        'Присутствие в списке Избранного',
        default = False,
    )
    is_in_shopping_cart = models.BooleanField(
        'Присутствие в списке покупок',
        default = False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

