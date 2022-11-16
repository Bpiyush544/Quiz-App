from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Assessment, QuestionSet, OptionSet

# Create your views here.


def home(request):
    return render(request, 'home.html')


def assessments(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        name = request.POST.get('name')
        duration = request.POST.get('duration')
        findUser = User.objects.get(username=user)
        ass = Assessment(user=findUser, name=name, duration=duration)
        ass.save()
        return redirect('home')
    exams = Assessment.objects.all()
    return render(request, 'assessments2.html', {'exams': exams})


def viewAndEdit(request, ass):
    if request.method == "POST" and request.POST.get('questionTitle') and request.POST.get('mark'):
        print(ass)
        assessment = []
        for obj in Assessment.objects.all():
            if str(obj.name) == ass:
                assessment.append(obj)
                break
        print(assessment)
        questionTitle = request.POST.get("questionTitle")
        mark = request.POST.get("mark")
        question = QuestionSet(
            assessment=assessment[0], questionTitle=questionTitle, mark=mark)
        question.save()
        return redirect(".")
    newObj = []
    for obj in QuestionSet.objects.all():
        if str(obj.assessment) == ass:
            newObj.append(obj)
    options = []
    for obj in OptionSet.objects.all():
        if str(obj.Question) == ass:
            options.append(obj)
    # only update and delete funcnality remains for test , question statement and question options
    # all the questions would be displayed here
    return render(request, 'viewAndEdit.html', {'newObj': newObj, 'options': options})


def deleteAssessment(request, pk):
    deleteAss = Assessment.objects.get(id=pk)
    deleteAss.delete()
    return redirect("home")


def questionView(request, pk):
    if request.method == "POST":
        optionStatement = request.POST.get('optionStatement')
        optionCheckbox = request.POST.get('optionCheckbox')
        check = False
        if optionCheckbox == "on":
            check = True
        Question = QuestionSet.objects.get(id=pk)
        opt = OptionSet(Question=Question,
                        optionStatement=optionStatement, correct=check)
        opt.save()
        return redirect(".")
    # here we have to figure out which id i have to pass currently we are doing it incorrectly
    print(pk)
    findQuestion = QuestionSet.objects.filter(id=pk)
    print(findQuestion[0])
    options = OptionSet.objects.filter(Question=findQuestion[0])
    print(options)
    return render(request, 'questionView.html', {'question': findQuestion, 'options': options})


def questionDelete(request, pk):
    print(pk)
    question = QuestionSet.objects.get(id=pk)
    print(question)
    question.delete()
    return redirect("..")


def optionDelete(request, pk):
    print(pk)
    option = OptionSet.objects.get(id=pk)
    option.delete()
    # print(option)
    return render(request, "secret.html")

# so i am done with pretty much all basic stuff i have to add update and delete functnality and correct option as well
# and at last the functnality where child gave test and got reportcard


def testAssessment(request, pk):
    assessment = Assessment.objects.get(id=pk)
    # so basically we have to use this technique we dont have any other option
    questions = QuestionSet.objects.filter(assessment=assessment)
    options = OptionSet.objects.all()
    data = {'question': []}
    for ques in questions:
        data['question'].append(ques.questionTitle)
        print(ques.questionTitle)
    print(data)
    return render(request, 'takeTest.html', {"assessment": assessment, "questions": questions, "options": options, 'data': data})


def result(request):
    score = 0
    if request.method == 'POST':
        assessment = request.POST.get('assessment_id')
        user = request.POST.get('user_id')
        information = request.POST.get('information')
        print(assessment, user, information)
        ass = Assessment.objects.get(id=assessment)
        options = information.split(',')
        answerSet = {}
        allQuestions = QuestionSet.objects.all()
        for ques in allQuestions:
            answerSet[ques.pk] = []
            originalOptions = OptionSet.objects.filter(Question=ques)
            for opts in originalOptions:
                print(opts.correct)
                if opts.correct == True:
                    answerSet[ques.pk].append(opts.pk)

        print(answerSet, 'This is the answerSet')
        query = {}

        for opt in range(len(options)-1):
            check = options[opt].split('-')
            # print(check[0], check[1])
            if int(check[0]) not in query:
                query[int(check[0])] = []
                query[int(check[0])].append(int(check[1]))
            else:
                query[int(check[0])].append(int(check[1]))
        print(query, 'This is querySet')
        # now time to check the answers
        for q in query:
            query[q].sort()
            answerSet[q].sort()
            if query[q] == answerSet[q]:
                score += QuestionSet.objects.get(pk=q).mark
        print(score)
    return render(request, 'result.html', {'score': score})
