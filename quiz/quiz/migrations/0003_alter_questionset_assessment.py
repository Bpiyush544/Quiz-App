# Generated by Django 4.1.1 on 2022-10-17 04:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_alter_assessment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionset',
            name='assessment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.assessment'),
        ),
    ]
