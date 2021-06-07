from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        'Ингредиент',
        max_length=200,
        unique=True,
        db_index=True
    )
    measure = models.CharField('Единицы измерения', max_length=100)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['title']

    def __str__(self):
        return f'{self.title}, {self.measure}'


class Tag(models.Model):
    COLORS = (
        ('green', 'Зеленый'),
        ('orange', 'Оранжевый'),
        ('purple', 'Пурпурный')
    )
    title = models.CharField('Имя тега', max_length=50, db_index=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50, choices=COLORS)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(
        'Название рецепта',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='images/',
        blank=True,
        null=True,
    )
    description = models.TextField(
        'Описание рецепта',
        max_length=200
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиент'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    cook_time = models.PositiveSmallIntegerField(
        'Время готовки',
        null=False,
        default=5,
        help_text='Добавьте время приготовления в минутах',
    )
    tag = models.ManyToManyField(
        'Tag',
        related_name='recipes',
        verbose_name='Теги'
    )
    slug = AutoSlugField(populate_from='title', allow_unicode=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.title}, {self.author}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amounts'
    )
    quantity = models.DecimalField(
        max_digits=6,
        decimal_places=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = ('ingredient', 'recipe')
