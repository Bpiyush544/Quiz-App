from optparse import Option
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Assessment,QuestionSet,OptionSet

# Create your views here.
def home(request):
    return render(request, 'home.html')

def assessments(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        name = request.POST.get('name')
        duration = request.POST.get('duration')
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
    options = []
    for obj in OptionSet.objects.all():
        if str(obj.Question) == ass:
            options.append(obj)
    # all the questions would be displayed here
    return render(request, 'viewAndEdit.html',{'newObj':newObj, 'options': options})


def questionView(request, pk):
    # here we have to figure out which id i have to pass currently we are doing it incorrectly
    findQuestion = QuestionSet.objects.filter(id = pk)
    # print(findQuestion[0].questionTitle)
    options = OptionSet.objects.filter(Question = findQuestion[0])
    # print(options)
    return render(request, 'questionView.html',{'question':findQuestion,'options': options})


# so i am done with pretty much all basic stuff i have to add update and delete functnality and correct option as well
# and at last the functnality where child gave test and got reportcard