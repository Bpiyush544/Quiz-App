# Generated by Django 4.0.8 on 2022-11-17 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_candidatedetails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CandidateDetails',
            new_name='CandidateDetail',
        ),
    ]
