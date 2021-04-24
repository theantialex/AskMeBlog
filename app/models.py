from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count


class QuestionManager(models.Manager):
 def popular(self):
     return self.prefetch_related('likes', 'author').annotate(like_sum=Sum('likes__like')).order_by('-like_sum')

 def new(self):
     return self.prefetch_related('likes', 'author').annotate(like_sum=Sum('likes__like')).order_by('-date')

 def tagged(self, str):
     return self.prefetch_related('likes', 'author').filter(tags__name=str).annotate(like_sum=Sum('likes__like'))


class AnswerManager(models.Manager):
    def all_ans(self, pk):
        return self.prefetch_related('likes', 'author').filter(question__id=pk).annotate(like_sum=Sum('likes__like'))


class TagManager(models.Manager):
    def popular(self):
        return self.annotate(count=Count('questions')).order_by('-count')


class ProfileManager(models.Manager):
    def best(self):
        return self.annotate(count=Count('answers')).order_by('-count')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateField()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True)
    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.TextField()
    date = models.DateField()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    objects = AnswerManager()

    def __str__(self):
        return self.text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()
    objects = ProfileManager()

    def __str__(self):
        return self.user.__str__()


class QuestionLike(models.Model):
    LIKE_CHOICES = (('LIKE', '1'), ('DISLIKE', '-1'))
    like = models.IntegerField(choices=LIKE_CHOICES, default=0)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.like) + ' ' + self.question.__str__()


class AnswerLike(models.Model):
    LIKE_CHOICES = (('LIKE', '1'), ('DISLIKE', '-1'))
    like = models.IntegerField(choices=LIKE_CHOICES, default=0)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.like) + ' ' + self.answer.__str__()


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    objects = TagManager()

    def __str__(self):
        return self.name
