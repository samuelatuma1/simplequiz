from django.shortcuts import render

from django.http import HttpResponse
import datetime
from monthdelta import monthdelta

# Create your views here.

from .models import Courses, QuizProfile, Quiz, QuizQuestion, QuestionChoice, Category, Leadership_board

## VERSION 3 ADDITION
def home(request):
    #Get all categories
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'quizTest/home.html', context)


############################################################################
#Index routes a user to a particular quiz if such a quiz exists.
# It takes in the course name as an argument.
#The model(s) here should provide
    # - The questions for a course
    # - The options for each question
    # - The right answer to each question
    # - The duration of the quiz in "hour" or 'min'
############################################################################

def index(request, quiz):

    ##VERSION 3.2  ADDITION. This is necessary to prevent users from using the back button to retake the quiz, and from accesing quiz from the header (url)
    if request.method == 'POST':

        user = request.POST['user']
    
        #if a person decides to write a quiz on a particular course

        #Assuming you have a course called quiz
        quizName = str(quiz)

        #Get all the questions relating to the course
        get_questions = QuizQuestion.objects.filter(quiz__course__name=quizName).all()

        #If no such quiz, return an error message
        if len(get_questions) <= 0:
            return render(request, 'quizTest/error.html', {'error_msg': f"It is not your fault, it is ours. We couldn't find {quizName}"})


        ## VERSION 2 MODIFICATION

        # The previous version worked, but for this one, you will access all questions in a course at once




        ##VERSION 3 MODIFICATION
        # Allow for  a certain number of trials. 3 in this case
        #################################################################################
        # Get the last performance from this particular user
        try:
            
            recent = Leadership_board.objects.filter(user=user).filter(course=quizName).last()

            #Get last renewal from recent, and determine when next access should be renewed
            renew_access = recent.last_renewal + monthdelta(6)  #Add 6 months to last_renewal to determine next renewal

            #Get date test is to be written
            submission_date = datetime.date.today()
            #Check if last_renewal is upto 6 months away from today
            get_time_difference = renew_access - submission_date

            #convert get_time_difference to integer
            time_left_before_renew = get_time_difference.days

            #If there is still time before next renewal
            if time_left_before_renew > 0:

                have_trial= False

                #Check if user has used up his trials 2 trials in this case
                if recent.trials > 1:

                    have_trial = False

                else:
                    #if user haven't used up his trials
                    have_trial = True
                    

            #If it is more than 6 months ago, set his last performance's trial to 0, and renew_date to the day of submission
            else:
            
                recent.last_renewal=submission_date
                recent.trials=0
                recent.save()
                have_trial = True
            
        #If the user have not taken the test before 
        except:
            have_trial = True



        

        if have_trial == True:
            get_questions = QuizQuestion.objects.filter(quiz__course__name=quizName).all()
            
            #Check if any such course exists in the first place
            if len(get_questions) > 0:
                
                questionSet = []
            
                for question in get_questions:
                
                    #Create an array which we can more easily work with in javascript
                    quest = question.question

                    #Get options for each question uas well as the right answer related_name = options
                    choices = question.options.first()

                    ##VERSION 3 INCLUSION
                    # Needed because the question model is represented in two different models, the question and choice
                    # The idea is that, sometimes, there might be question without choices, which if not handled, can
                    #lead to errors
                    ## END
                    # If question has options
                    try:
                        answer = choices.correct_answer

                        #Convert the makeup of each question to a python dictionary to allow it being passed as a json in javascript more easily
                        questionSet.append({
                            'question': quest,

                            'A': choices.A,
                            'B': choices.B,
                            'C': choices.C,
                            'D': choices.D,

                            'answer': answer
                        })
                    #If no option available for the question
                    except:
                        answer = 'None'

                        #Convert the makeup of each question to a python dictionary to allow it being passed as a json in javascript more easily
                        questionSet.append({
                            'question': quest,

                            'A': 'None',
                            'B': 'None',
                            'C': 'None',
                            'D': 'None',

                            'answer': answer
                        })





                #Pass in questionSet as context. 
                # (having options (QuestionChoice( and the right answer(QuestionChoice.correct_answer))
                #Also, pass in the name of the course

                # duration of each quiz. Should be in the/a model. This will allow for different quiz to have different duration
                # The idea is a table should hold the duration as well as time_denotation whether in min or hour

                ## VERSION 2 
                #################################################################################
                # Get quiz duration from the Quiz Model
                # However there is a possibility the quiz might not be attached to a Course model;
                # If this is the case, the code will use a default 30 minutes

                ###########################################################################

                # This attempts to populate say nav bar with other courses in the same category
                # Get the course name
                course_name = Courses.objects.filter(name=quizName).first()

                # Get the category the course falls under 
                course_category = course_name.category.name

                # Get other quiz that falls under the same category
                related_quiz = Quiz.objects.filter(course__category__name=course_category).all()
                # Convert querySet to a more easily iterable list
                listit = list(related_quiz)

                #Get other quizes from the same category apart from the current quiz
                related_quizzes = []

                for i in listit:
                    #If it is the current quiz, ignore
                    if i.course.name == quizName:
                        pass
                    #Else if it is not the current quiz, add to related_quizes
                    else:
                        related_quizzes.append(i.course.name)

                #Pass in the related_quizzes in context


                ###########################################################################
                #################################################################################
                quiz_duration = Quiz.objects.filter(course__name=quizName).first()

                #Try getting the duration from the course model
                try:
                    duration = quiz_duration.duration
                    time_denotation = quiz_duration.time_denotation 

                #If a course does not exist for the particular quiz, use a default 30 minutes
                except:
                    duration = 30
                    time_denotation = 'min'

                ## VERSION 2 COMMENT END

                context = {
                    'questionSet': questionSet, 
                    'course': quizName, 

                    ## MODEL 2 Changes
                    'related_quizzes': related_quizzes,
                    'duration': duration, 
                    'time_denotation':  time_denotation

                    }

                return render(request, 'quizTest/quiz.html', context)


            #If no such course, return an error message
            else:
                if len(get_questions) < 1:
                    return HttpResponse('Error no existing question')
        
        else:
            return render(request, 'quizTest/error.html', {'error_msg': f'You have used up your trials for {quizName}', 'extra_info': f'Course accessible from {renew_access}'})
            #return HttpResponse('Resource not available')

    #If request is any other thana a post request
    else:
        return render(request, 'quizTest/error.html', {'error_msg': f' Wrong turn, it seems you attempted to access this page from the wrong point'})



###############################################################################
# quiz_performance shows the performance of a user in a test she just took
# It is usually a post request and the data from the post request should include
    # - score
    # - user
    # - and course
# This function should also store user's performance alongside others, 
# so another function say (leadership_board), will be able to rank users
# Unfortunately, I didn't create any login method to keep it simple
# I will try to make this easily modifiable
###############################################################################

def quiz_performance(request):
    if request.method == 'POST':
        #Get all the passed in data
        score = request.POST['score']
        user = request.POST['user']
        course = request.POST['course']

        ## VERSION 2 INCLUSION
        day = int(request.POST['day'])
        month = int(request.POST['month'])
        year = int(request.POST['year'])

        # Store performance in session
        request.session['user'] = user
        request.session['total'] = score
        request.session['course'] = course

        ###############################################################
            #If there is a table e.g Leaderboard, add data to table
            #This will be used for ranking performance, etc
            #This is commented out, because I didn't create such table
        ###############################################################

        ## VERSION 2 MODIFICATION
        ######################################################
        #Save user performance in leadership_board
        #Query for user performance in all courses too
        #Get and save date from javascript
        ######################################################

        
        
        #Create date from javascript input
        submission_date = datetime.date(year, month, day)

        ##VERSION 3 MODIFICATION
        ###Save last_renewal and trials field with "calculated" obtained result
        #################################################################################
        try:
            # Get the last performance from this particular user
            recent = Leadership_board.objects.filter(user=user).filter(course=course).last()

            #Get last renewal from recent, and determine when next access should be renewed
            renew_access = recent.last_renewal + monthdelta(6)  #Add 6 months to last_renewal to determine next renewal

            #Check if last_renewal is upto 6 months away from today
            get_time_difference = renew_access - submission_date

            #convert get_time_difference to integer
            time_left_before_renew = get_time_difference.days

            #If there is still time before next renewal
            if time_left_before_renew > 0:

                #Check if user has used up his trials
                if recent.trials > 1:

                    #If this is the case, add 1 to trials
                    # Do not change last renewal
                    new_performance = Leadership_board(user=user, course=course, score=score, date=submission_date, last_renewal=recent.last_renewal, trials=recent.trials+1)
                    new_performance.save()

                else:
                    #also if user haven't used up his trials still add to trials
                    new_performance = Leadership_board(user=user, course=course, score=score, date=submission_date, last_renewal=recent.last_renewal, trials=recent.trials+1)
                    new_performance.save()

            #If it is more than 6 months ago, set his trial to 0, and renew_date to the day of submission
            #This will hardly be the case because it will be taken care of in the quiz-index section, but for the sake of completeness, lets implement this
            else:
                new_performance = Leadership_board(user=user, course=course, score=score, date=submission_date, last_renewal=submission_date, trials=0)
                new_performance.save()

        except:
            new_performance = Leadership_board(user=user, course=course, score=score, date=submission_date, last_renewal=submission_date, trials=0)
            new_performance.save()

        #################################################################################

        ##END OF VERSION 3 ADDITION
        

        #Order the user's perfomance list from most recent to oldest
        user_performances = Leadership_board.objects.filter(user=request.session['user']).all().order_by('-pk')

    
        #Get users score, etc from session
        context = {
            'user': request.session['user'],
            'course': request.session['course'],
            'score':  request.session['total'],
            'submission_date': submission_date,
            ##VERSION 2 MODIFICATION
            'user_performances': user_performances
        }

        return render(request, 'quizTest/quiz_performance.html', context)

    #Order the user's performance list from most recent to oldest
    user_performances = Leadership_board.objects.filter(user=request.session['user']).all().order_by('-pk')

    return render(request, 'quizTest/quiz_performance.html', {'user_performances': user_performances})


### Leadership_board shows the ranked performance For all test takers for a particular course
def leadership_board(request, quiz):
    #Assuming you have a course called quiz
    quizName = str(quiz)    

    # This attempts to populate say nav bar with other courses in the same category
    # Get the course name
    course_name = Courses.objects.filter(name=quizName).first()

    # Get the category the course falls under 
    course_category = course_name.category.name

    # Get other quiz that falls under the same category
    related_quiz = Quiz.objects.filter(course__category__name=course_category).all()
    # Convert querySet to a more easily iterable list
    listit = list(related_quiz)

    #Get other quizes from the same category apart from the current quiz
    related_quizzes = []

    for i in listit:
        #If it is the current quiz, ignore
        if i.course.name == quizName:
            pass
        #Else if it is not the current quiz, add to related_quizes
        else:
            related_quizzes.append(i.course.name)

        #Pass in the related_quizzes in context


        ###########################################################################
        #################################################################################
    ## Rank score performance in a descending order
    ranked_performance = Leadership_board.objects.all().filter(course=quizName).order_by('-score')

    return render(request, 'quizTest/ranked_performance.html', {'user_performances': ranked_performance, 'related_quizzes': related_quizzes})    

## VERSION 3 ADDITION
####################################################################################################
# course_main allows users to access all courses in a particular category
# Ideally, it should return the course material and quiz of every course in the category if there is
# Else, it returns a message like No course here yet
####################################################################################################
def course_main(request, category):

    #Get the category name
    category = str(category)

    #Get all courses in the category
    category = Category.objects.filter(name=category).all()

    #If there is at least a course in the category
    try:
        course_category = category[0].name

        # Get all the courses in the same category
        related_courses = Courses.objects.filter(category__name=course_category).all()

        # Now, if there is at least one course in the category
        try:
            #Return coure.html, passing all the courses as context
            listit = list(related_courses)
            #return HttpResponse(f'{listit[1]}')  
            
            return render(request, 'quizTest/course.html', {'related_courses': listit})
        except:
             return HttpResponse('No course yet') 
    
    #If there is no course in the category
    except:
        return HttpResponse('Nothing here yet')


## VERSION 3
## On click of a particular course
## This is where the actual course content should be hosted
def course_details(request, category):

    course = str(category)
    #Get the quiz associated with the course
    quizName = Quiz.objects.filter(course__name=course).all()
    
    ##################################################################################################
    #Also. attempt to get the Course material associated with the course
    #Since we dont have a course material model yet we will skip this step, but it should be something like this
    #course_material = Course_material.objects.filter(course__name=category).all()
    # Some table data methods the Course_material model should have include a TextField, an optional image field etc

    # Also, the solution set to a particular quiz may be included here
    # A possible way to handle the answer set, is to include a TextField named something like 
        #Question_Solution in the QuestionChoice, or QuizQuestion section, and 
        #then create its own view and template. This will be implemented later
    #########################################################################################
    
    #Pass in the context
    context = {
        'quizName': quizName,
        #'course_materal': course_material,
        'quiz_solution': quizName
    }
    return render(request, 'quizTest/course_details.html', context)
    


##  funtion that handles quiz details and ultimately leads to the quiz
def quiz_instructions(request, category):

    course = str(category)
    #Get the quiz associated with the course
    quizName = Quiz.objects.filter(course__name=course).all()
    
    
    #Pass in the context
    context = {
        'quizName': quizName,
       
    }
    return render(request, 'quizTest/quiz_details.html', context)