# Generated by Django 3.1.4 on 2020-12-11 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizTest', '0011_auto_20201211_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizquestion',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizTest.courses'),
        ),
    ]