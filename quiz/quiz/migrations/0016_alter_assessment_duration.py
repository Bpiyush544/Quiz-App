# Generated by Django 4.0.8 on 2022-11-23 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_testreport_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='duration',
            field=models.IntegerField(default=1),
        ),
    ]