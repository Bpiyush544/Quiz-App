from django.urls import path
from .views import home,assessments, optionDelete, questionDelete,viewAndEdit,questionView,deleteAssessment

urlpatterns = [
    path('', home , name="home"),
    path('assessments/', assessments , name="home"),
    path('assessments/view/<str:ass>/', viewAndEdit , name="edit"),
    path('assessments/delete/<int:pk>/', deleteAssessment , name="delete"),
    path('questionView/<int:pk>/', questionView , name="questionView"),
    path('questionDelete/<int:pk>/', questionDelete , name="questionDelete"),
    path('optionDelete/<int:pk>/', optionDelete, name="optionDelete")
]
