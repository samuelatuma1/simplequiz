from django.contrib import admin
from .models import Courses, QuizProfile, Quiz, QuizQuestion, QuestionChoice, Category, Leadership_board
# Register your models here.
admin.site.register(Courses)
admin.site.register(QuizProfile)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
admin.site.register(QuestionChoice)
admin.site.register(Category)
admin.site.register(Leadership_board)


