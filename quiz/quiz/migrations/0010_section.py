# Generated by Django 4.0.8 on 2022-11-19 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_questionset_section_alter_invitation_link_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1024)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.assessment')),
            ],
        ),
    ]
