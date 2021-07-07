from django import template

register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def favorite_by(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()


@register.filter
def translate_verbose_name(num):
    last_two_digits = num % 100
    last_digit = num % 10
    if 5 <= last_two_digits <= 20 or last_two_digits in {0, 5, 6, 7, 8, 9}:
        return f'{num} рецептов'
    if last_digit in {2, 3, 4}:
        return f'{num} рецепта'
    return f'{num} рецепт'


@register.filter
def tags_list(get):
    return get.getlist('tags')


@register.filter
def set_tag_qs(request, tag):
    new_request = request.GET.copy()
    tags = request.GET.getlist('tags')
    if tag.name in tags:
        tags.remove(tag.name)
    else:
        tags.append(tag.name)
    new_request.setlist('tags', tags)
    return new_request.urlencode()


@register.filter
def tags_to_url_params(tags):
    url_param_tags = [f'tags={tag}' for tag in tags]
    return '&' + '&'.join(url_param_tags)
