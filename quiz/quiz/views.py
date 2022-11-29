from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import Assessment, QuestionSet, OptionSet, CandidateDetail, Invitation, Section, TestReport, SectionReport
import datetime
import secrets
import string
from django.contrib.auth import login
from django.contrib.auth import authenticate
# from django.template.defaulttags import register

# Create your views here.


# @register.filter
# def getList()
def home(request):
    return render(request, 'home.html')


def assessments(request):

    if request.method == 'POST' and request.POST.get('newTestName') != None:
        newTestName = request.POST.get('newTestName')
        oldTestId = request.POST.get('oldTestId')
        newTestName = newTestName.strip()
        Assessment.objects.filter(id=oldTestId).update(name=newTestName)
        print(newTestName, oldTestId)

    elif request.method == 'POST':
        user = request.POST.get('user')
        name = request.POST.get('name')
        print(user, name)
        duration = 1
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
    if request.method == "POST" and request.POST.get('newSectionName'):
        newSectionName = request.POST.get('newSectionName')
        sectionId = request.POST.get('sectionId')
        Section.objects.filter(id=int(sectionId)).update(name=newSectionName)

    elif request.method == 'POST':
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
        information[section] = []

    for question in QuestionSet.objects.filter(assessment=assessment):
        information[question.section].append(question)
    print(information, "this is my inforamtion")
    questions = []
    sections = []
    for info in information:
        # print(info, "this is info")
        questions.append(information[info])
        sections.append(Section.objects.get(id=info.id))
    print(questions)
    print(sections)
    return render(request, 'viewAndEdit2.html', {'test': Assessment.objects.get(name=ass), 'questions': questions, 'sections': sections, 'information': information})


def release(request, pk):
    print(pk)
    if Assessment.objects.get(id=pk).released == True:
        Assessment.objects.filter(id=pk).update(released=False)
    else:
        Assessment.objects.filter(id=pk).update(released=True)
    return redirect(request.META.get('HTTP_REFERER'))


def deleteAssessment(request, pk):
    deleteAss = Assessment.objects.get(id=pk)
    deleteAss.delete()
    return redirect("home")


def addQues(request, assgn):
    if request.method == "POST":
        sectionName = request.POST.get('sectionName')
        problemName = request.POST.get('problemName')
        score = request.POST.get('score')
        time = request.POST.get('time')
        description = request.POST.get('description')
        optionInformation = request.POST.get('optionInformation')
        multiChoice = request.POST.get('multiChoice')
        # problemName = request.POST.get('problemName')
        asses = Assessment.objects.get(name=assgn)
        print("this is assess", asses)
        print(sectionName)
        sectionName = sectionName.strip()
        print(multiChoice, 'This is multiChoice')
        multiChoiceCheck = False
        if multiChoice == 'on':
            multiChoiceCheck = True
        for section in Section.objects.all():
            if(section.assessment == asses):
                print(section, section.name, len(sectionName))
                if(section.name == sectionName):
                    print("Yes the sectionName is matching")
        requiredSection = Section.objects.get(
            assessment=asses, name=sectionName)
        print(requiredSection)
        question = QuestionSet(
            assessment=asses, questionTitle=problemName, mark=score, section=requiredSection, multiChoice=multiChoiceCheck)

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


def updateQues(request, pk):
    if request.method == "POST":
        sectionName = request.POST.get('sectionName')
        sectionName = sectionName.strip()
        problemName = request.POST.get('problemName')
        score = request.POST.get('score')
        time = request.POST.get('time')
        description = request.POST.get('description')
        optionInformation = request.POST.get('optionInformation')
        multiChoice = request.POST.get('multiChoice')
        # problemName = request.POST.get('problemName')
        for ass in Assessment.objects.all():
            print(ass, ass.id)
        asses = QuestionSet.objects.get(id=pk).assessment
        # asses = Assessment.objects.get(id=pk)
        print("this is assess", asses)
        print(sectionName)
        print(multiChoice, 'This is multiChoice')
        multiChoiceCheck = False
        if multiChoice == 'on':
            multiChoiceCheck = True
        requiredSection = Section.objects.get(
            assessment=asses, name=sectionName)
        print(requiredSection)
        # QuestionSet.objects.filter(id=pk).update(
        #     section=requiredSection, multiChoice=multiChoiceCheck)
        print(optionInformation)
        # options = optionInformation.split('##')
        # print(options)
        # for i in range(0, len(options), 2):
        #     chk = False
        #     if(options[i+1] == "on"):
        #         chk = True
        #     option = OptionSet(Question=question,
        #                        optionStatement=options[i], correct=chk)
        #     print(option)
        #     option.save()
    print(pk)
    # from the pk we can get the Question
    question = QuestionSet.objects.get(id=pk)
    assignment = question.assessment.name
    # now we can get the OptionSet
    options = OptionSet.objects.filter(Question=question)
    sectionName = question.section.name
    return render(request, 'updateQues.html', {'question': question, 'options': options, 'assignment': assignment, 'sectionName': sectionName})


def deleteQues(request, pk):
    assessment = QuestionSet.objects.get(id=pk).assessment.name
    QuestionSet.objects.get(id=pk).delete()
    return redirect(f"http://127.0.0.1:8000/assessments/view/{assessment}/")


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
    assessment = Assessment.objects.get(name=assgn)
    return render(request, 'candidateSettings.html', {'assessment': assessment})


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


def invites(request, pk):
    print(pk)
    if request.method == "POST" and request.POST.get('emailInvite') != None:
        # print(''.join(secrets.choice(string.hexdigits + string.punctuation)
        #               for i in range(8)))
        username = ''.join(secrets.choice(
            string.ascii_lowercase + string.ascii_uppercase) for i in range(6))
        password = ''.join(secrets.choice(
            string.hexdigits + string.punctuation) for i in range(8))
        assessment = Assessment.objects.get(id=pk)
        email = request.POST.get('emailInvite')
        invitedBy = request.user
        # invitedTo = None
        user = User.objects.create_user(
            email=email, password=password, username=username)

        print(user, "this is my new user")
        user.save()
        invitedTo = user
        link = f"http://127.0.0.1:8000/testDetails/{assessment.name}/"
        invite = Invitation(invitedBy=invitedBy, link=link, invitedTo=invitedTo,
                            password=password, assessment=assessment, email=email)
        # print(invite)
        if Invitation.objects.filter(invitedBy=invitedBy, assessment=assessment, email=email).exists():
            pass
        else:
            invite.save()
        # print(link)
    elif request.method == "POST":
        teacherUser = request.user
        studentUserName = request.POST.get('userName')
        assessment = request.POST.get('assessment')
        invitedBy = teacherUser
        invitedTo = User.objects.get(username=studentUserName)
        assessmentTaken = Assessment.objects.get(name=assessment)
        if Invitation.objects.filter(invitedBy=invitedBy, invitedTo=invitedTo, assessment=assessmentTaken).exists() == False:
            link = f"http://127.0.0.1:8000/testDetails/{assessmentTaken.name}/"
            invite = Invitation(invitedBy=invitedBy,
                                invitedTo=invitedTo, assessment=assessmentTaken, link=link)
            # print(invite)
        # print(invitedBy, invitedTo, assessmentTaken)
    assessment = Assessment.objects.get(id=pk)
    return render(request, 'invites.html', {'invites': Invitation.objects.filter(assessment=assessment), 'assessment': assessment})


def deleteInvite(request, pk):
    deleteInvitation = Invitation.objects.get(id=pk)
    deleteInvitation.delete()
    return redirect('home')


def unused(request):
    # so to find these unused invitation we can check whether a particular invite has been used to create a testReport
    return render(request, 'unused.html', {'invites': Invitation.objects.all()})


def attempted(request):
    return render(request, 'attempted.html', {'invites': Invitation.objects.all()})


def deleteSection(request, pk):
    print(pk, "THIS IS MY PRIMARY KEY")
    Section.objects.filter(id=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))


def testDetails(request, test):
    print(test)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        assessment = Assessment.objects.get(name=test)
        if Invitation.objects.filter(email=email, password=password, assessment=assessment).exists():
            print("yes this exists")
        # copy the code from CandidateSettings function
        # Find out what we have to do with the collected information and where we have to store it
        print(test, "jhbhjbhj")
        user = authenticate(username=username, email=email, password=password)
        login(request, user)
        print("Currently logged in person is : ", request.user)
        return redirect(f'http://127.0.0.1:8000/takeTest/{test}/')

    assessment = Assessment.objects.get(name=test)
    # next we find all the sections and the information we need

    sections = Section.objects.filter(assessment=assessment)
    candidateDetails = CandidateDetail.objects.get(assessment=assessment)
    # print(candidateDetails.disclaimerCheck)
    # print(len(sections), sections)
    numberOfSections = len(sections)
    information = {}

    for section in sections:
        information[section] = len(QuestionSet.objects.filter(section=section))
    # print(information)
    return render(request, 'testDetails.html', {'numberOfSections': numberOfSections, 'information': information, 'candidateDetails': candidateDetails})


# we can make a redirection from testDetails page to this one and a unique decoder and encoder can be used so that every child gets a unique session to get into the test and take the test

def takeTest2(request, assessmentName):
    if request.method == 'POST':
        sectionId = request.POST.get('sectionId')
        questionsAttempted = request.POST.get('questionsAttempted')
        questionsAttempted = questionsAttempted[:len(questionsAttempted)-1]
        test = Section.objects.get(id=sectionId).assessment.name
        print(questionsAttempted, "This the information about my questionsAttempted")
        currentSectionReport = SectionReport.objects.filter(
            section=Section.objects.get(id=sectionId)).update(attemptInformation=questionsAttempted)
    currentUser = request.user
    print(currentUser)
    assessment = Assessment.objects.get(name=assessmentName)
    sections = Section.objects.filter(assessment=assessment)
    if(TestReport.objects.filter(user=currentUser, assessment=assessment).exists()):
        print("Test Report already Exists")
        old = TestReport.objects.get(
            user=currentUser, assessment=assessment).time
        old = old.replace(tzinfo=None)
        now = datetime.datetime.now()
        difference = now - old
        Invitation.objects.filter(
            invitedTo=currentUser, assessment=assessment).update(isAttempted=True)
    else:
        tempTestReport = TestReport(user=currentUser, assessment=assessment)
        tempTestReport.save()
        for section in sections:
            tempSectionReport = SectionReport(
                testReport=tempTestReport, section=section)
            tempSectionReport.save()
        Invitation.objects.filter(
            invitedTo=currentUser, assessment=assessment).update(isAttempted=True)
    information = {}
    old = TestReport.objects.get(
        user=currentUser, assessment=assessment).time
    old = old.replace(tzinfo=None)
    now = datetime.datetime.now()
    difference = now - old
    totalTimePassedTillNow = difference.days*86400 + difference.seconds - 19800
    totalTimeAvailable = assessment.duration*60
    print(totalTimePassedTillNow, totalTimeAvailable)
    # {'section': {{'question': solved/unsolved},
    #              {'question': solved/unsolved}, {'question': solved/unsolved}}}
    user = request.user
    testReport = TestReport.objects.get(user=user, assessment=assessment)
    for section in sections:
        currentSectionReport = SectionReport.objects.get(
            testReport=testReport, section=section)
        attempts = currentSectionReport.attemptInformation.split(',')
        info = []
        for attempt in attempts:
            if attempt.split('-')[0] not in info:
                info.append(attempt.split('-')[0])
        questions = QuestionSet.objects.filter(section=section)
        information[section] = {}
        for question in questions:
            if str(question.id) in info:
                information[section][question] = 'Attempted'
            else:
                information[section][question] = 'UnAttempted'
    return render(request, 'takeTest2.html', {'information': information, 'totalTimePassedTillNow': totalTimePassedTillNow, 'totalTimeAvailable': totalTimeAvailable})


def testQues(request, pk):
    sectionId = pk
    section = Section.objects.get(id=sectionId)
    currentUser = request.user
    print(currentUser)
    assessment = section.assessment
    old = TestReport.objects.get(
        user=currentUser, assessment=assessment).time
    old = old.replace(tzinfo=None)
    now = datetime.datetime.now()
    difference = now - old
    totalTimePassedTillNow = difference.days*86400 + difference.seconds - 19800
    totalTimeAvailable = assessment.duration*60
    print(totalTimePassedTillNow, totalTimeAvailable)
    questions = QuestionSet.objects.filter(section=section)
    information = {}
    # for question in questions:
    #     information[question] = OptionSet.objects.filter(Question=question)
    # temp = {'question1':OptionSet, 'question2':OptionSet}
    # information = {'1': '1', '2': '2',
    #                '3': '3', '4': '4', '5': '5'}
    # This technique should work
    # We have the sectionID from here we can generate the sectionReport that Report will provide us with the required information then we can use that information to mark our unchecked input checkbox
    # info = {'question': {'option': 'attempted/unattempted',
    #                      'option': 'attempted/unattempted', 'option': 'attempted/unattempted'}, }
    user = request.user
    testReport = TestReport.objects.get(user=user, assessment=assessment)
    currentSectionReport = SectionReport.objects.get(testReport=testReport,
                                                     section=Section.objects.get(id=pk))
    data = currentSectionReport.attemptInformation.split(',')
    information = {}
    for question in questions:
        information[question] = {}
        for option in OptionSet.objects.filter(Question=question):
            if str(question.id) + '-' + str(option.id) in data:
                information[question][option] = True
            else:
                information[question][option] = False
    return render(request, 'testQues.html', {'information': information, "assessment": assessment, 'sectionId': sectionId, 'totalTimePassedTillNow': totalTimePassedTillNow, 'totalTimeAvailable': totalTimeAvailable})


'''

Not able to understand how we would be able to implement this feature 
We are using the emails of the user to invite him for the test

so we receive 2 things from frontend one is the email address of the user 
and the other one is assessment link
Generating the assessment link is easy
the difficult thing is genrating a password
lets just say we generate a 8 word password for that person
so we send two things to the person one is 1) link of test
the other thing we are providing is        2) generated password

'''
