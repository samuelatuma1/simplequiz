from django.db import models
import datetime

from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from django.db.models import F, Q, Count, Sum, Case, When
from django.db.models.functions import Cast
from django.utils.translation import gettext as _

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 200)
    slug = models.SlugField(max_length=200 ,unique=True)

    ##VERSION 3 ADDITION, INCLUDE AN IMAGE FIELD
    image = models.ImageField(upload_to='category', max_length=60)
    def __str__(self):
        return self.name


class Courses(models.Model):
    category = models.ForeignKey(Category, related_name = 'courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=250,)
    body = models.TextField()
    slug=models.SlugField(max_length=250,unique=True)
    images = models.ImageField(upload_to='courses/', default='quiz\media\courses\image.jpg')
    
   
    
    def __str__(self):
        return self.name
    
# my code  

#quiz profiles for users
class QuizProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    total_score = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    
    def __str__(self):
        return f'{first_name} {last_name}'
    
    
# Quiz for instruction 
class Quiz(models.Model):
    course=models.ForeignKey(Courses ,on_delete=models.CASCADE)
    slug = models.SlugField()
    description=models.TextField(blank=True, null=True)

    ##VERSION 2 ADDITION
    # Added the ability to time a quiz here 
    duration = models.IntegerField()
    time_denotation = models.CharField(max_length=6, choices=[('min', 'min'), ('hour', 'hour')])


    def __str__(self):
        return self.course.name

# quiz questions
class QuizQuestion(models.Model):
    quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE)

    question = models.TextField()
    question_mark = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    slug = models.SlugField()

    ##VERSION 2 ADDITION
    #Deleted the questionAnswer model

    def __str__(self):
        return self.question

# question choice

    
ANSWER_CHOICES=[
    ('A','A'),
    ('B','B'),
    ('C','C'),
    ('D','D')
]

class QuestionChoice(models.Model):
    question =models.ForeignKey(QuizQuestion, related_name='options' ,on_delete=models.CASCADE)
    A = models.CharField(max_length=500, blank=False, null=False)
    B = models.CharField(max_length=500, blank=False, null=False)
    C = models.CharField(max_length=500, blank=False, null=False)
    D = models.CharField(max_length=500, blank=False, null=False)

    # Let the correct answer be related to the actual options
    correct_answer = models.CharField(default=False , null=False, max_length=30, choices=[('A', A), ('B', B), ('C', C), ('D', D)])
    
    

    def __str__(self):
        return self.question.question


##VERSION 2 ADDITION
class Leadership_board(models.Model):
    user = models.CharField(max_length=60, blank=True)
    score = models.CharField(max_length=10, blank=True)
    course = models.CharField(max_length=50, blank=True)
    date = models.DateField(blank=True)

    ##VERSION 3 ADDITION
    last_renewal = models.DateField()
    trials = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.course} - {self.score}"

    

