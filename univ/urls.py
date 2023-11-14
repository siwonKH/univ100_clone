from django.urls import path

from .views import Home, University, Question, Search, Post, QuestionDetail, Likes, Authenticate, Register, Answer, QuestionSearch, Mypage, Logout


urlpatterns = [
    path('', Home.as_view()),
    path('univ/<int:university_id>', University.as_view()),
    path('univ/<int:university_id>/q', Question.as_view()),
    path('search', Search.as_view()),
    path('univ/<int:university_id>/post', Post.as_view()),
    path('univ/<int:university_id>/q/<int:question_id>', QuestionDetail.as_view()),
    path('likes', Likes.as_view()),
    path('auth', Authenticate.as_view()),
    path('register', Register.as_view()),
    path('univ/<int:university_id>/q/<int:question_id>/answer', Answer.as_view()),
    path('univ/<int:university_id>/q/search', QuestionSearch.as_view()),
    path('mypage', Mypage.as_view()),
    path('logout', Logout.as_view()),
]
