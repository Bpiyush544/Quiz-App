from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Assessment,QuestionSet

# Create your views here.
def home(request):
    return render(request, 'home.html')

def assessments(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        allUsers = User.objects.all()
        findUser = User.objects.get(username = user)
        ass = Assessment(user=findUser,name = name, duration = duration)
        ass.save()
        return redirect('home')
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