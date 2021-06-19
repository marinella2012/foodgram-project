from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from slugify import slugify

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
    color = models.CharField(
        'Цвет тега',
        max_length=50,
        choices=COLORS,
        unique=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ('title', )

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
    slug = models.SlugField(
        verbose_name='slug',
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        raw_slug = self.slug or self.title
        new_id = Recipe.objects.order_by('id').last()
        if new_id is not None:
            new_id = new_id.id + 1
        else:
            new_id = 1
        self.slug = slugify(raw_slug + str(new_id))
        return super().save(*args, **kwargs)

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
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe')
        ]
