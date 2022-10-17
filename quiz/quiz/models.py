from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime, date
# from django.db.models import DateTimeField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

class Assessment(models.Model):
    user = models.ForeignKey(User, null = False, on_delete = models.CASCADE)
    name = models.CharField(max_length = 255, default="Exam")
    duration = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return(self.name)


class QuestionSet(models.Model):
    assessment = models.ForeignKey(Assessment, null = False, on_delete = models.CASCADE)
    # TODO add question image feature 
    questionTitle = models.CharField(max_length = 1023, default= "question statement")
    information = models.CharField(max_length = 10000)