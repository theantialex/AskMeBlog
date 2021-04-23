from django.core.management.base import BaseCommand
from app.models import *
from random import choice
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Fills database with fake data'

    avatar_list = ['1.png', '2.jpeg', '3.jpg', '4.jpg', '5.jpg',
                   '5.jpg', '6.jpg']

    def add_arguments(self, parser):
        parser.add_argument('--db_size', default='small', type=str, help='The size of database data to create.')

    def fill_profiles(self, cnt):
        usernames = set()
        for i in range(cnt):
            username = fake.simple_profile().get('username')
            while username in usernames:
                username = fake.simple_profile().get('username')
            user = User.objects.create(
                username=username,
                password=fake.password(length=9, special_chars=True)
            )
            Profile.objects.create(
                user_id=user.id,
                avatar=choice(self.avatar_list)
            )
            usernames.add(username)

    def fill_questions(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        tags_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            q = Question(
                author_id=choice(author_ids),
                text='. '.join(fake.sentences(fake.random_int(min=5, max=15))),
                title=fake.sentence()[:-1] + '?',
                date=fake.date_between(start_date='-1y', end_date='today'),
            )
            q.save()
            tag1 = Tag.objects.get(id=choice(tags_ids))
            tag2 = Tag.objects.get(id=choice(tags_ids))
            if tag1 != tag2:
                q.tags.add(tag1, tag2)
            else:
                q.tags.add(tag1)

    def fill_tags(self, cnt):
        for i in range(cnt):
            Tag.objects.create(
                name=fake.unique.word(),
            )

    def fill_answers(self, cnt):
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            question_id = choice(questions_ids)
            Answer.objects.create(
                text='. '.join(fake.sentences(fake.random_int(min=5, max=10))),
                author_id=choice(author_ids),
                question_id=question_id,
                date=Question.objects.get(id=question_id).date
            )

    def fill_question_likes(self, cnt):
        LIKE_CHOICES = ['1', '-1']
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            QuestionLike.objects.create(
                like=choice(LIKE_CHOICES),
                author_id=choice(author_ids),
                question_id=choice(questions_ids)
            )

    def fill_answer_likes(self, cnt):
        LIKE_CHOICES = ['1', '-1']
        answers_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        author_ids = list(
            Profile.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(cnt):
            AnswerLike.objects.create(
                like=choice(LIKE_CHOICES),
                author_id=choice(author_ids),
                answer_id=choice(answers_ids)
            )

    def handle(self, *args, **options):
        if options['db_size'] == 'large':
            sizes = [10001, 11000, 100001, 1000001, 450000, 600000]
        elif options['db_size'] == 'medium':
            sizes = [50, 100, 120, 250, 180, 300]
        else:
            sizes = [10, 20, 20, 40, 20, 20]

        self.fill_profiles(sizes[0])
        self.fill_tags(sizes[1])
        self.fill_questions(sizes[2])
        self.fill_answers(sizes[3])
        self.fill_question_likes(sizes[4])
        self.fill_answer_likes(sizes[5])
