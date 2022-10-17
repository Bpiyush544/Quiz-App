from django.shortcuts import render
from .models import Assessment,QuestionSet
# Create your views here.
def home(request):
    return render(request, 'home.html')

def assessments(request):
    exams = Assessment.objects.all()
    return render(request, 'assessments.html', {'exams':exams})

def viewAndEdit(request, ass):
    newObj = []
    for obj in QuestionSet.objects.all():
        if str(obj.assessment) == ass:
            newObj.append(obj)
    print(newObj)
    # all the questions would be displayed here
    return render(request, 'viewAndEdit.html',{'newObj':newObj})


def questionView(request, pk):
    # print(pk)
    # for obj in QuestionSet.objects.all():
    #     print(obj.id)
    findQuestion = QuestionSet.objects.filter(id = 1)
    # print(findQuestion)
    return render(request, 'questionView.html',{'question':findQuestion})