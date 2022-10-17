from django.urls import path
from .views import home,assessments

urlpatterns = [
    path('', home , name="home"),
    path('assessments/', assessments , name="home"),
]
