from django.urls import path
from .views import home,assessments,viewAndEdit

urlpatterns = [
    path('', home , name="home"),
    path('assessments/', assessments , name="home"),
    path('assessments/view/<str:ass>/', viewAndEdit , name="edit"),
]
