import csv
from django.template.defaultfilters import slugify

from django.core.management.base import BaseCommand
from phones.models import Phone
import re


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r', encoding='utf8') as file:
            # phones = list(csv.DictReader(file, delimiter=';'))
            phones = csv.reader(file, delimiter=';')
            #next(phones)


    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            # TODO: Добавьте сохранение модели
            added_phone = Phone(
                id=phone['id'],
                name=phone['name'],
                price=int(phone['price']),
                image=phone['image'],
                release_date=phone['release_date'],
                lte_exists=bool(phone['lte_exists'].capitalize()),
                slug=slugify(phone['name'])
            )

            added_phone.save()