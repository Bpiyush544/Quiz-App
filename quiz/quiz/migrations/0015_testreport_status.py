# Generated by Django 4.0.8 on 2022-11-22 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_sectionreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='testreport',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('Completed', 'Completed')], default='In Progress', max_length=100),
        ),
    ]
