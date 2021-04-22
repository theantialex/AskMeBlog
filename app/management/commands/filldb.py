from django.core.management.base import BaseCommand
from app.models import *
from random import choice
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Fills database with fake data'

    avatar_list = ['media/1.jpg', 'media/2.jpeg', 'media/3.jpg', 'media/4.jpg', 'media/5.jpg',
                   'media/5.jpg', 'media/6.jpg']

    def add_arguments(self, parser):
        parser.add_argument('--db_size', default='small', type=str, help='The size of database data to create.')

    def fill_profiles(self, cnt):
        for i in range(cnt):
            Profile.objects.create(
                user__username=fake.unique.simple_profile().username,
                user__password=fake.pystr(8, 16),
                avatar=choice(self.avatar_list)
            )

    def fill_questions(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            Question.objects.create(
                author_id=choice(author_ids),
                text='. '.join(fake.sentences(fake.random_int(min=2, max=5))),
                title=fake.sentence()[:128],
                date=fake.date(),
               # tags=
            )

    def fill_tags(self, cnt):
        for i in range(cnt):
            Tag.objects.create(
                name=fake.word(),
            )

    def handle(self, *args, **options):
        cnt = 10
        self.fill_profiles(cnt)
        self.tags(cnt)