from django.contrib import admin
from . models import Profile,Assessment,QuestionSet
# Register your models here.
admin.site.register(Profile)
admin.site.register(Assessment)
admin.site.register(QuestionSet)