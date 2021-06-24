import json

from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from recipes.models import Ingredient, Measurement

file_name = f'{BASE_DIR}/fixtures/ingredients.csv'


class Command(BaseCommand):

    def handle(self, *args, **options):
        source = json.load(open('fixtures/ingredients.json', 'r'))
        for line in source:
            ingredient_name = line['title']
            measure_name = line['dimension']
            measure = Measurement.objects.get_or_create(name=measure_name)[0]
            Ingredient.objects.get_or_create(
                name=ingredient_name,
                unit_of_measurement=measure
            )
        print('loaded')
