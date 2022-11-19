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
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="Exam")
    duration = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(self.name)


class Section(models.Model):
    assessment = models.ForeignKey(
        Assessment, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024, default="Section")

    def __str__(self):
        return str(self.assessment) + " " + self.name


class QuestionSet(models.Model):
    assessment = models.ForeignKey(
        Assessment, null=False, on_delete=models.CASCADE)
    # TODO add question image feature
    questionTitle = models.CharField(
        max_length=1023, default="question statement")
    mark = models.IntegerField()
    section = models.IntegerField(default=1)

    def __str__(self):
        return(str(self.assessment))


class OptionSet(models.Model):
    Question = models.ForeignKey(
        QuestionSet, null=True, on_delete=models.CASCADE)
    optionStatement = models.CharField(max_length=1023)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return(self.optionStatement)


class Evaluation(models.Model):
    candidate = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    marks = models.IntegerField()


class CandidateDetail(models.Model):
    assessment = models.ForeignKey(
        Assessment, null=False, on_delete=models.CASCADE)
    fullName = models.BooleanField(default=False)
    workExperience = models.BooleanField(default=False)
    city = models.BooleanField(default=False)
    rollNo = models.BooleanField(default=False)
    email = models.BooleanField(default=False)
    gradYear = models.BooleanField(default=False)
    cgpa = models.BooleanField(default=False)
    gpa = models.BooleanField(default=False)
    collegeName = models.BooleanField(default=False)
    contactNo = models.BooleanField(default=False)
    contactRec = models.BooleanField(default=False)
    stream = models.BooleanField(default=False)
    major = models.BooleanField(default=False)
    degree = models.BooleanField(default=False)
    gender = models.BooleanField(default=False)
    jobRole = models.BooleanField(default=False)
    resume = models.BooleanField(default=False)
    disclaimer = models.CharField(
        max_length=5000, default="I agree not to copy code from any source(including websites, books or friends and colleagues) to complete this assessment. I may, however, reference programming language documentation or use an IDE that has code completion features")
    disclaimerCheck = models.BooleanField(default=True)

    def __str__(self):
        return str(self.assessment)


class Invitation(models.Model):
    invitedBy = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, related_name="teacher")
    invitedTo = models.ForeignKey(
        User, null=False, on_delete=models.CASCADE, related_name="student")
    assessment = models.ForeignKey(
        Assessment, null=False, on_delete=models.CASCADE)
    isAttempted = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default="none")
    link = models.CharField(max_length=1024, default="")

    def __str__(self):
        return str(self.invitedBy) + " " + str(self.assessment)
