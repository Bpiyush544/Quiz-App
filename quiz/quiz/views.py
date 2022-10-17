from django.shortcuts import render
from .models import Assessment
# Create your views here.
def home(request):
    return render(request, 'home.html')

def assessments(request):
    exams = Assessment.objects.all()
    return render(request, 'assessments.html', {'exams':exams})

def viewAndEdit(request, ass):
    print(ass)
    # all the questions would be displayed here
    return render(request, 'viewAndEdit.html')