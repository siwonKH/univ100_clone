from django import views
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from univ import utils


class Home(views.View):
    @staticmethod
    def get(request):
        return render(request, 'index.html')


class University(views.View):
    @staticmethod
    def get(request):
        return render(request, 'university.html')


class Question(views.View):
    @staticmethod
    def get(request):
        return render(request, 'question.html')


class Search(views.View):
    @staticmethod
    def get(request):
        query = request.GET.get('q')

        results = utils.search_university(query)

        return render(request, 'search.html', {'results': results})


class Post(views.View):
    @staticmethod
    def get(request):
        return render(request, 'post.html')


class QuestionDetail(views.View):
    @staticmethod
    def get(request, question_id):
        return render(request, 'question_detail.html')


class Likes(views.View):
    @staticmethod
    def get(request):
        return render(request, 'likes.html')


class Authenticate(views.View):
    @staticmethod
    def get(request):
        return render(request, 'authenticate.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'authenticate.html', {'error': 'Invalid username or password'})


class Register(views.View):
    @staticmethod
    def get(request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        User.objects.create_user(username=username, password=password)

        return redirect('/auth')
