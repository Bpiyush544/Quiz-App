from django.urls import path
from .views import home, assessments, optionDelete, questionDelete, viewAndEdit, questionView, deleteAssessment, testAssessment, result, addQues, candidateSettings, invites, unused, attempted, testDetails, takeTest2, testQues

urlpatterns = [
    path('', home, name="home"),
    path('assessments/', assessments, name="assessments"),
    path('assessments/test/<int:pk>/', testAssessment, name="testAssessment"),
    path('assessments/view/<str:ass>/', viewAndEdit, name="edit"),
    path('assessments/delete/<int:pk>/', deleteAssessment, name="delete"),
    path('questionView/<int:pk>/', questionView, name="questionView"),
    path('questionDelete/<int:pk>/', questionDelete, name="questionDelete"),
    path('optionDelete/<int:pk>/', optionDelete, name="optionDelete"),
    path('result/', result, name="result"),
    path('addQues/<str:assgn>/', addQues, name="addQues"),
    path('candidateSettings/<str:assgn>/',
         candidateSettings, name="candidateSettings"),
    path('invites/', invites, name="invites"),
    path('unused/', unused, name="unused"),
    path('attempted/', attempted, name="attempted"),
    path('testDetails/<str:test>/', testDetails, name="testDetails"),
    path('takeTest/<str:details>/', takeTest2, name="takeTake2"),
    path('testQues/<int:pk>/', testQues, name="testQues"),
]
