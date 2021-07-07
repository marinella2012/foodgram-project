from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from slugify import slugify

User = get_user_model()


class TagChoices(models.TextChoices):
    BREAKFAST = ('breakfast', 'Breakfast')
    LUNCH = ('lunch', 'Lunch')
    DINNER = ('dinner', 'Dinner')


class Measurement(models.Model):
    name = models.CharField(max_length=32, unique=True,
                            verbose_name='Название')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Название')
    unit_of_measurement = models.ForeignKey(Measurement,
                                            on_delete=models.SET_NULL,
                                            null=True,
                                            related_name='ingredients',
                                            verbose_name='Единицы измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'unit_of_measurement'],
                name='unique_ingredient')
        ]

    def __str__(self):
        return f'{self.name}, {self.unit_of_measurement}'


class Recipe(models.Model):
    author = models.ForeignKey('users.User',
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    title = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        verbose_name='slug',
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='static/images/recipes/%Y/%m/%d',
                              blank=True, verbose_name='Изображение')
    body = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField('Tag', related_name='recipes',
                                  verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    blank=True, verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        raw_slug = self.slug or self.title
        if Recipe.objects.exists():
            new_id = Recipe.objects.order_by('id').last().id + 1
        else:
            new_id = 1
        self.slug = slugify(raw_slug + str(new_id))
        return super().save(*args, **kwargs)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredient',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиент')
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


class Tag(models.Model):
    name = models.CharField(max_length=32, choices=TagChoices.choices,
                            unique=True, verbose_name='Название')
    show_name = models.CharField(max_length=32,
                                 verbose_name='Отображаемое имя')
    color = models.CharField(max_length=50, blank=True, verbose_name='Цвет')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def clean(self, *args, **kwargs):
        colors = {'breakfast': 'orange', 'lunch': 'green', 'dinner': 'purple'}
        color = colors.get(str(self.name), 'blue')
        names = {'breakfast': 'Завтрак', 'lunch': 'Обед', 'dinner': 'Ужин'}
        show_name = names.get(str(self.name))
        self.color = color
        self.show_name = show_name
        super(Tag, self).clean()

    def full_clean(self, *args, **kwargs):
        return self.clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Tag, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        related_name='shopping'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_cart_recipe'
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.recipe}\tin cart of\t{self.user}'
