from django.urls import path

from .views import Home, University


urlpatterns = [
    path('', Home.as_view()),
    path('university', University.as_view()),
]
