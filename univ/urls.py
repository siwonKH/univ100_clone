from django.urls import path

from .views import Home, University, Question, Search, Post, QuestionDetail, Likes, Authenticate, Register


urlpatterns = [
    path('', Home.as_view()),
    path('university', University.as_view()),
    path('q', Question.as_view()),
    path('search', Search.as_view()),
    path('post', Post.as_view()),
    path('q/<int:question_id>', QuestionDetail.as_view()),
    path('likes', Likes.as_view()),
    path('auth', Authenticate.as_view()),
    path('register', Register.as_view()),
]
