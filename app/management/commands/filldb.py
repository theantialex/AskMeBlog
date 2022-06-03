from django.core.management.base import BaseCommand
from app.models import *
from django.db.models import F
from random import choice
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Fills database with fake data'

    avatar_list = ['1.png', '2.jpeg', '3.jpg', '4.jpg', '5.jpg', '5.jpg', '6.jpg', '7.jpeg',
                   '8.jpg', '9.jpg', '10.jpg', '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.png',
                   '16.jpg', '17.jpg', '18.jpg', '19.jpg']

    def add_arguments(self, parser):
        parser.add_argument('--db_size', default='small', type=str, help='The size of database data to create.')

    def fill_profiles(self, cnt):
        usernames = set()
        profiles = []
        for i in range(cnt):
            username = fake.simple_profile().get('username')
            while username in usernames:
                username = fake.simple_profile().get('username')
            user = User.objects.create(
                username=username,
                password=fake.password(length=9, special_chars=True)
            )
            profiles.append(Profile(
                user_id=user.id,
                avatar=choice(self.avatar_list)
            ))
            usernames.add(username)

        Profile.objects.bulk_create(profiles)

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
        questions = []
        for i in range(cnt):
            questions.append(Question(
                author_id=choice(author_ids),
                text=' '.join(fake.sentences(fake.random_int(min=5, max=15))),
                title=fake.sentence()[:-1] + '?',
                date=fake.date_between(start_date='-1y', end_date='today'),
            ))

        Question.objects.bulk_create(questions)
        for q in Question.objects.all():
            tag1 = Tag.objects.get(id=choice(tags_ids))
            tag2 = Tag.objects.get(id=choice(tags_ids))
            if tag1 != tag2:
                q.tags.add(tag1, tag2)
            else:
                q.tags.add(tag1)

    def fill_tags(self, cnt):
        tags = set()
        tags_list = []
        for i in range(cnt):
            tag = fake.word()
            while tag in tags:
                tag += '_' + fake.word()
                if len(tag) > 49:
                    tag = fake.pystr(min_chars=2, max_chars=15)
            tags_list.append(Tag(
                name=tag,
            ))
            tags.add(tag)
        Tag.objects.bulk_create(tags_list)

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
        answers = []
        for i in range(cnt):
            question_id = choice(questions_ids)
            answers.append(Answer(
                text=' '.join(fake.sentences(fake.random_int(min=5, max=10))),
                author_id=choice(author_ids),
                question_id=question_id,
                date=Question.objects.get(id=question_id).date
            ))
        Answer.objects.bulk_create(answers)


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
        question_likes = []
        for i in range(cnt):
            question_id = choice(questions_ids)
            like = choice(LIKE_CHOICES)
            question_likes.append(QuestionLike(
                like=like,
                author_id=choice(author_ids),
                question_id=question_id
            ))
            Question.objects.get(id=question_id).update(rating=F('rating') + like)

        QuestionLike.objects.bulk_create(question_likes)

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
        answers_likes = []
        for i in range(cnt):
            answers_likes.append(AnswerLike(
                like=choice(LIKE_CHOICES),
                author_id=choice(author_ids),
                answer_id=choice(answers_ids)
            ))
        AnswerLike.objects.bulk_create(answers_likes)

    def fill_rating(self):
        questions_ids = list(
            Question.objects.values_list(
                'id', flat=True
            )
        )
        for id in questions_ids:
            rating = QuestionLike.objects.filter(question_id=id).aggregate(sum=Sum('like'))
            if rating['sum']:
                Question.objects.filter(id=id).update(rating=rating['sum'])

    def handle(self, *args, **options):
        if options['db_size'] == 'large':
            sizes = [10001, 11000, 100001, 1000001, 900000, 1200000]
        elif options['db_size'] == 'medium':
            sizes = [500, 1000, 1200, 2500, 1800, 3000]
        else:
            sizes = [10, 20, 20, 40, 20, 20]

        self.fill_profiles(sizes[0])
        self.fill_tags(sizes[1])
        self.fill_questions(sizes[2])
        self.fill_answers(sizes[3])
       # self.fill_question_likes(sizes[4])
       # self.fill_answer_likes(sizes[5])
        # self.fill_rating()
