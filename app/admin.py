from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerLike)
admin.site.register(QuestionLike)
admin.site.register(Tag)
