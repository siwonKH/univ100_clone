import time

from django import views
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from univ import utils


class Home(views.View):
    @staticmethod
    def get(request):

        # get random 20 universities
        universities = utils.get_random_20_universities()

        return render(request, 'index.html', {'universities': universities})


class Mypage(views.View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:

            return render(request, 'mypage.html', {'user': request.user})
        else:
            return redirect('/auth')


class Logout(views.View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('/')
        else:
            return redirect('/auth')


class University(views.View):
    @staticmethod
    def get(request, university_id):

        university = utils.get_university(university_id)

        questions = utils.get_10_questions_and_first_answer(university_id)

        return render(request, 'university.html', {'university': university, 'questions': questions})


class Question(views.View):
    @staticmethod
    def get(request, university_id):
        university = utils.get_university(university_id)

        questions = utils.get_all_questions_and_first_answer(university_id)

        return render(request, 'question.html', {'questions': questions, 'university': university, 'query': ''})


class Search(views.View):
    @staticmethod
    def get(request):
        query = request.GET.get('q')

        results = utils.search_university(query)

        return render(request, 'search.html', {'results': results})


class Post(views.View):
    @staticmethod
    def get(request, university_id):
        if request.user.is_authenticated:

            university = utils.get_university(university_id)

            return render(request, 'post.html', {'university': university})
        else:
            return redirect('/auth')

    def post(self, request, university_id):
        title = request.POST.get('title')
        content = request.POST.get('content')

        question = utils.add_question(university_id, title, content)

        return redirect(f'/univ/{university_id}/q/{question.id}')


class QuestionDetail(views.View):
    @staticmethod
    def get(request, university_id, question_id):
        university = utils.get_university(university_id)

        question = university.question_set.get(id=question_id)

        question.answers = question.answer_set.all()

        return render(request, 'question_detail.html', {'question': question, 'university': university})


class QuestionSearch(views.View):
    @staticmethod
    def get(request, university_id):
        # try:
        query = request.GET.get('q')

        if query == "":
            return redirect(f'/univ/{university_id}/q')

        start_time = time.time()
        questions = utils.search_questions(university_id, query)
        end_time = time.time()
        search_time = end_time - start_time
        print(f'search: {search_time:.6f} seconds')

        start_time = time.time()
        questions2 = utils.legacy_search_questions(university_id, query)
        end_time = time.time()
        search_time = end_time - start_time
        print(f'legacy search: {search_time:.6f} seconds')


        return render(request, 'question.html', {'questions': questions, 'university': utils.get_university(university_id), 'query': query})
        # except Exception as e:
        #     print(e)
        #     return render(request, 'question.html', {'questions': [], 'university': utils.get_university(university_id), 'query': query})


class Answer(views.View):
    @staticmethod
    def post(request, university_id, question_id):
        content = request.POST.get('content')

        university = utils.get_university(university_id)

        question = university.question_set.get(id=question_id)

        question.answer_set.create(content=content)

        return redirect(f'/univ/{university_id}/q/{question_id}')


class Likes(views.View):
    @staticmethod
    def get(request):
        return render(request, 'likes.html')

    @staticmethod
    def post(request):
        if request.user.is_authenticated:
            university_id = request.POST.get('university_id')
            question_id = request.POST.get('question_id')
            answer_id = request.POST.get('answer_id')

            if university_id:
                university = utils.get_university(university_id)

                university.likes.add(request.user)

                return JsonResponse({'likes': university.likes.count()})
            elif question_id:
                question = utils.get_university(question_id)

                question.likes.add(request.user)

                return JsonResponse({'likes': question.likes.count()})
            elif answer_id:
                answer = utils.get_university(answer_id)

                answer.likes.add(request.user)

                return JsonResponse({'likes': answer.likes.count()})
        else:
            return redirect('/auth')


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
