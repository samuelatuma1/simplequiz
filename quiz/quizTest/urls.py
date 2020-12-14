# These are the urls for our quizTest
from django.urls import path
from . import views

urlpatterns = [
    path('quiz/<str:quiz>/', views.index, name='index'),

    # Quiz performance. On submit of quiz
    path('quiz_performance/', views.quiz_performance, name='quiz_performance'),

    # Leadership board. For all test takers
    path('leaderboard/<str:quiz>/', views.leadership_board, name='leadership_board'),
   
    # A funny home page. 
    path('home/', views.home, name='home'),

    # Path for each course
    path('course/<str:category>/', views.course_main, name='course_main'),

    #Path for details of each course
    path('details/<str:category>/', views.course_details, name='course_details'),

    #Path for the details of each quiz
    
    path('quizinstructions/<str:category>/', views.quiz_instructions, name='quiz_instructions'),
]