from django.contrib import admin
from . models import Profile, Assessment, QuestionSet, OptionSet, Evaluation, CandidateDetail
# Register your models here.
admin.site.register(Profile)
admin.site.register(Assessment)
admin.site.register(QuestionSet)
admin.site.register(OptionSet)
admin.site.register(Evaluation)
admin.site.register(CandidateDetail)
