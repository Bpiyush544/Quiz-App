# Generated by Django 4.0.8 on 2022-11-23 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_questionset_multichoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionset',
            name='optionStatement',
            field=models.CharField(default='No Statement Provided', max_length=1023),
        ),
    ]