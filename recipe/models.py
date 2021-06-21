from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from slugify import slugify

User = get_user_model()


class Measurement(models.Model):
    name = models.CharField(max_length=32, unique=True,
                            verbose_name='Название ')

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    title = models.CharField(
        'Ингредиент',
        max_length=200,
        unique=True,
        db_index=True
    )
    measure = models.ForeignKey(
        Measurement,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ingredients',
        verbose_name='Единицы измерения')

    class Meta:
        ordering = ('title', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'measure'],
                name='unique_ingredient')
        ]

    def __str__(self):
        return f'{self.title}, {self.measure}'


class TagChoices(models.TextChoices):
    BREAKFAST = ('breakfast', 'Breakfast')
    LUNCH = ('lunch', 'Lunch')
    DINNER = ('dinner', 'Dinner')


class Tag(models.Model):
    title = models.CharField(
        'Имя тега',
        max_length=50,
        db_index=True,
        choices=TagChoices.choices,
        unique=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField(
        'Цвет тега',
        max_length=50,
        blank=True,
        unique=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ('display_name', )

    def __str__(self):
        return self.title

    def clean(self, *args, **kwargs):
        colors = {'breakfast': 'orange', 'lunch': 'green', 'dinner': 'purple'}
        color = colors.get(str(self.title), 'red')
        titles = {'breakfast': 'Завтрак', 'lunch': 'Обед', 'dinner': 'Ужин'}
        display_name = titles.get(str(self.title))
        self.color = color
        self.display_name = display_name
        super(Tag, self).clean()

    def full_clean(self, *args, **kwargs):
        return self.clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Tag, self).save(*args, **kwargs)


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
