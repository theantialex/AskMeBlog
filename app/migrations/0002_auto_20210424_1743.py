# Generated by Django 3.2 on 2021-04-24 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerlike',
            name='like',
            field=models.IntegerField(choices=[('LIKE', '1'), ('DISLIKE', '-1')], default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='questions', to='app.Tag'),
        ),
        migrations.AlterField(
            model_name='questionlike',
            name='like',
            field=models.IntegerField(choices=[('LIKE', '1'), ('DISLIKE', '-1')], default=0),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
