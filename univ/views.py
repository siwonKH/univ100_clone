from django import views
from django.shortcuts import render


class Home(views.View):
    @staticmethod
    def get(request):
        return render(request, 'index.html')


class University(views.View):
    @staticmethod
    def get(request):
        return render(request, 'university.html')
