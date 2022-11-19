from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Assessment, QuestionSet, OptionSet, CandidateDetail, Invitation, Section
import datetime

# Create your views here.


def home(request):
    return render(request, 'home.html')


def assessments(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        name = request.POST.get('name')
        print(user, name)
        duration = 20
        findUser = User.objects.get(username=user)
        ass = Assessment(user=findUser, name=name, duration=duration)
        ass.save()
        section = Section(assessment=ass)
        section.save()
        details = CandidateDetail(assessment=ass)
        details.save()
        # return redirect('home')
    exams = Assessment.objects.all()
    return render(request, 'assessments2.html', {'exams': exams})


def viewAndEdit(request, ass):
    print("The name of the Assignment is : ", ass)
    if request.method == 'POST':
        assessment = Assessment.objects.get(name=ass)
        sectionName = request.POST.get('sectionName')
        section = Section(assessment=assessment, name=sectionName)
        section.save()
    assessment = Assessment.objects.get(name=ass)
    # from this i can grab all the sections contained in this assessment
    sections = Section.objects.filter(assessment=assessment)
    # print(len(sections))

    information = {}

    for section in sections:
        # print(section.name)
        information[section.name] = []
        information[section.name].append(section.id)

    for question in QuestionSet.objects.filter(assessment=assessment):
        information[question.section.name].append(question)
    print(information)

    for info in information:
        print(information[info])
    return render(request, 'viewAndEdit2.html', {'test': ass, 'information': information})


# def viewAndEdit(request, ass):
#     if request.method == "POST" and request.POST.get('questionTitle') and request.POST.get('mark'):
#         print(ass)
#         assessment = []
#         for obj in Assessment.objects.all():
#             if str(obj.name) == ass:
#                 assessment.append(obj)
#                 break
#         print(assessment)
#         questionTitle = request.POST.get("questionTitle")
#         mark = request.POST.get("mark")
#         question = QuestionSet(
#             assessment=assessment[0], questionTitle=questionTitle, mark=mark)
#         question.save()
#         return redirect(".")
#     newObj = []
#     # print("This is my ASS", ass)
#     print(QuestionSet.objects.all())
#     for obj in QuestionSet.objects.all():
#         if str(obj.assessment) == ass:
#             newObj.append(obj)
#     options = []
#     for obj in OptionSet.objects.all():
#         if str(obj.Question) == ass:
#             options.append(obj)
#     # print(newObj, "     NEWOBJ")
#     # only update and delete funcnality remains for test , question statement and question options
#     # all the questions would be displayed here
#     return render(request, 'viewAndEdit2.html', {'questions': newObj, 'options': options, 'test': ass})


def deleteAssessment(request, pk):
    deleteAss = Assessment.objects.get(id=pk)
    deleteAss.delete()
    return redirect("home")


def addQues(request, assgn):
    if request.method == "POST":
        assignmentName = request.POST.get('assignment')
        sectionName = request.POST.get('sectionName')
        problemName = request.POST.get('problemName')
        score = request.POST.get('score')
        time = request.POST.get('time')
        description = request.POST.get('description')
        optionInformation = request.POST.get('optionInformation')
        # problemName = request.POST.get('problemName')
        asses = Assessment.objects.get(name=assgn)
        print("this is assess", asses)
        print(sectionName)
        requiredSection = Section.objects.get(name=sectionName)
        print(requiredSection)
        question = QuestionSet(
            assessment=asses, questionTitle=problemName, mark=score, section=requiredSection)

        question.save()

        print(question, "this is my question")
        options = optionInformation.split('##')
        print(options)
        for i in range(0, len(options), 2):
            chk = False
            if(options[i+1] == "on"):
                chk = True
            option = OptionSet(Question=question,
                               optionStatement=options[i], correct=chk)
            print(option)
            option.save()
            # print(options[i], options[i+1])
    print(assgn)
    return render(request, 'addQues.html', {'assignment': assgn})


def candidateSettings(request, assgn):
    if request.method == "POST":
        fullName = request.POST.get('fullName')
        workExperience = request.POST.get('workExperience')
        city = request.POST.get('city')
        rollNo = request.POST.get('rollNo')
        email = request.POST.get('email')
        gradYear = request.POST.get('gradYear')
        cgpa = request.POST.get('cgpa')
        gpa = request.POST.get('gpa')
        collegeName = request.POST.get('collegeName')
        contactNo = request.POST.get('contactNo')
        contactRec = request.POST.get('contactRec')
        stream = request.POST.get('stream')
        major = request.POST.get('major')
        degree = request.POST.get('degree')
        gender = request.POST.get('gender')
        jobRole = request.POST.get('jobRole')
        resume = request.POST.get('resume')
        disclaimer = request.POST.get('disclaimer')
        disclaimerCheck = request.POST.get('disclaimerCheck')
        dataFields = ["fullName", "workExperience", "city", "rollNo", "email", "gradYear", "cgpa",
                      "gpa", "collegeName", "contactNo", "contactRec", "stream", "major", "degree", "gender", "jobRole", "resume", "disclaimerCheck"]
        data = [fullName, workExperience, city, rollNo, email, gradYear, cgpa,
                gpa, collegeName, contactNo, contactRec, stream, major, degree, gender, jobRole, resume, disclaimerCheck]
        updatedData = []
        assessmentName = str(assgn)
        assessment = Assessment.objects.get(name=assessmentName)

        for i in range(0, len(data)):
            if data[i] == "on":
                updatedData.append(True)
            else:
                updatedData.append(False)
        print(data)
        print(updatedData)
        print(assessment)
        CandidateDetail.objects.filter(assessment=assessment).update(
            fullName=updatedData[0], workExperience=updatedData[1], city=updatedData[2], rollNo=updatedData[3], email=updatedData[4], gradYear=updatedData[5], cgpa=updatedData[6], gpa=updatedData[7], collegeName=updatedData[8], contactNo=updatedData[9], stream=updatedData[10], major=updatedData[11], degree=updatedData[12], gender=updatedData[13], jobRole=updatedData[14], resume=updatedData[15], disclaimerCheck=updatedData[16])
        # assDetail = CandidateDetail.objects.get(assessment=assessment).update()
    print(assgn)
    return render(request, 'candidateSettings.html')


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


def invites(request):
    if request.method == "POST":
        user = request.POST.get('user')
        userName = request.POST.get('userName')
        assessment = request.POST.get('assessment')
        invitedBy = User.objects.get(username=user)
        invitedTo = User.objects.get(username=userName)
        assessmentTaken = Assessment.objects.get(name=assessment)
        invite = Invitation(invitedBy=invitedBy,
                            invitedTo=invitedTo, assessment=assessmentTaken)
        # http://127.0.0.1:8000/assessments/test/5/
        print(invite)
        invite.save()
        # print(invitedBy, invitedTo, assessmentTaken)

    return render(request, 'invites.html', {'invites': Invitation.objects.all()})


def unused(request):
    return render(request, 'unused.html', {'invites': Invitation.objects.all()})


def attempted(request):
    return render(request, 'attempted.html', {'invites': Invitation.objects.all()})
