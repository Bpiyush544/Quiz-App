from django.contrib import admin
from . models import Profile,Assessment,QuestionSet,OptionSet
# Register your models here.
admin.site.register(Profile)
admin.site.register(Assessment)
admin.site.register(QuestionSet)
admin.site.register(OptionSet)