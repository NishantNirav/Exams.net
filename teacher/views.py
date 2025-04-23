from datetime import timedelta
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, Question, QuestionPaper, Response
from django.shortcuts import render, redirect
from functools import wraps
from django.http import HttpResponse
from django.db.models import Count, Sum

def validate_user_role(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            return redirect('/auth/login')

        # Check if the user is Admin
        if request.user.is_superuser:
            context = {
                'error_message': "This is the Teachers Portal. Please login to the Admin Portal.",
                'link_text': "Go to the Admin Portal",
                'link': "/admin"
            }
            return render(request, 'common/teacher/error.html', context)

        # Check if the user is admin
        elif not request.user.is_staff:
            context = {
                'error_message': "This is the Teacher Portal. Please login to the Student Portal.",
                'link_text': "Go to the Student Portal",
                'link': "/student"
            }
            return render(request, 'common/teacher/error.html', context)

        # If user is a student, proceed to the view
        return view_func(request, *args, **kwargs)
    return wrapper

@validate_user_role
def dashboard(request):
    if request.method=="GET":
        context={
            "User":request.user,
        }
        return render(request,'teacher/index.html',context)

@validate_user_role
def create_exam(request):
    if request.method == "POST":
        exam_name = request.POST.get('exam_name')
        exam_date = request.POST.get('exam_date')
        exam_time = request.POST.get('exam_time')
        exam_duration = request.POST.get('exam_duration')
        hours, minutes, seconds = map(int, exam_duration.split(':'))
        exam_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        Exam.objects.create(
            exam_name=exam_name,
            exam_date=exam_date,
            exam_time=exam_time,
            exam_duration=exam_duration,
        )
        # exam.save()
        return redirect('exam_list')
    return render(request, 'teacher/create_exam.html')

@validate_user_role
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'teacher/exam_list.html', {'exams': exams})

@validate_user_role
def update_exam(request, exam_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    if request.method == "POST":
        exam.exam_name = request.POST.get('exam_name')
        exam.exam_date = request.POST.get('exam_date')
        exam.exam_time = request.POST.get('exam_time')
        # exam.exam_duration = request.POST.get('exam_duration')
        exam_duration = request.POST.get('exam_duration')
        hours, minutes, seconds = map(int, exam_duration.split(':'))
        exam_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        exam.exam_duration=exam_duration
       
        exam.save()
        return redirect('exam_list')
    return render(request, 'teacher/update_exam.html', {'exam': exam})

@validate_user_role
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    if request.method == "POST":
        exam.delete()
        return redirect('exam_list')
    return render(request, 'teacher/delete_exam.html', {'exam': exam})

# Create a question paper
@validate_user_role
def create_question_paper(request):
    if request.method == "POST":
        exam_id = request.POST.get('exam_id')
        paper_name = request.POST.get('paper_name')
        exam = get_object_or_404(Exam, exam_id=exam_id)
        QuestionPaper.objects.create(
            paper_name=paper_name,
            exam_id=exam
        )
        return redirect('question_paper_list')
    exams = Exam.objects.all()
    return render(request, 'teacher/create_question_paper.html', {'exams': exams})

# List all question papers
@validate_user_role
def question_paper_list(request):
    papers = QuestionPaper.objects.all()
    return render(request, 'teacher/question_paper_list.html', {'papers': papers})

# Update question paper
@validate_user_role
def update_question_paper(request, paper_id):
    paper = get_object_or_404(QuestionPaper, paper_id=paper_id)
    if request.method == "POST":
        paper.paper_name = request.POST.get('paper_name')
        exam_id = request.POST.get('exam_id')
        exam = get_object_or_404(Exam, exam_id=exam_id)
        paper.exam_id = exam
        paper.save()
        return redirect('question_paper_list')
    exams = Exam.objects.all()
    return render(request, 'teacher/update_question_paper.html', {'paper': paper, 'exams': exams})

# Delete question paper
@validate_user_role
def delete_question_paper(request, paper_id):
    paper = get_object_or_404(QuestionPaper, paper_id=paper_id)
    if request.method == "POST":
        paper.delete()
        return redirect('question_paper_list')
    return render(request, 'teacher/delete_question_paper.html', {'paper': paper})
# List of questions for a specific exam and paper
# @login_required
@validate_user_role
def question_list(request, exam_id, paper_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    paper = get_object_or_404(QuestionPaper, paper_id=paper_id, exam_id=exam)
    questions = Question.objects.filter(exam_id=exam, paper_id=paper)
    
    return render(request, 'teacher/question_list.html', {
        'exam': exam,
        'paper': paper,
        'questions': questions
    })

# Create a new question for a specific exam and paper
# @login_required
@validate_user_role
def create_question(request, exam_id, paper_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    paper = get_object_or_404(QuestionPaper, paper_id=paper_id, exam_id=exam)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_option = int(request.POST.get('correct_option'))
        marks = int(request.POST.get('marks'))
        
        Question.objects.create(
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            marks=marks,
            exam_id=exam,
            paper_id=paper
        )
        return redirect('question_list', exam_id=exam_id, paper_id=paper_id)

    return render(request, 'teacher/create_question.html', {
        'exam': exam,
        'paper': paper
    })

# Update a specific question for a given exam and paper
# @login_required
@validate_user_role
def update_question(request, exam_id, paper_id, question_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    paper = get_object_or_404(QuestionPaper, paper_id=paper_id, exam_id=exam)
    question = get_object_or_404(Question, question_id=question_id, exam_id=exam, paper_id=paper)
    
    if request.method == 'POST':
        question.question_text = request.POST.get('question_text')
        question.option1 = request.POST.get('option1')
        question.option2 = request.POST.get('option2')
        question.option3 = request.POST.get('option3')
        question.option4 = request.POST.get('option4')
        question.correct_option = int(request.POST.get('correct_option'))
        question.marks = int(request.POST.get('marks'))
        question.save()
        return redirect('question_list', exam_id=exam_id, paper_id=paper_id)

    return render(request, 'teacher/update_question.html', {
        'exam': exam,
        'paper': paper,
        'question': question
    })

# Delete a question for a specific exam and paper
# @login_required
@validate_user_role
def delete_question(request, exam_id, paper_id, question_id):
    exam = get_object_or_404(Exam, exam_id=exam_id)
    paper = get_object_or_404(QuestionPaper, paper_id=paper_id, exam_id=exam)
    question = get_object_or_404(Question, question_id=question_id, exam_id=exam, paper_id=paper)
    
    if request.method == 'POST':
        question.delete()
        return redirect('question_list', exam_id=exam_id, paper_id=paper_id)

    return render(request, 'teacher/delete_question.html', {
        'exam': exam,
        'paper': paper,
        'question': question
    })
    
# def detailed_report(request, exam_id, paper_id):
#     """
#     View to display the detailed report for a specific exam and question paper.
#     Includes:
#     - Exam name, paper name, date, time, and duration
#     - List of students with marks scored and total marks
#     """
#     exam = get_object_or_404(Exam, pk=exam_id)
#     paper = get_object_or_404(QuestionPaper, pk=paper_id)

#     student_responses = Response.objects.filter(exam_id=exam, paper_id=paper).values(
#         'student_id__username'
#     ).annotate(
#         total_marks=Sum('marks_awarded')
#     )

#     total_marks = Response.objects.filter(exam_id=exam, paper_id=paper).aggregate(
#         total_marks=Sum('total_marks')
#     )['total_marks'] or 0

#     return render(request, 'teacher/detailed_report.html', {
#         'exam': exam,
#         'paper': paper,
#         'student_responses': student_responses,
#         'total_marks': total_marks,
#     })
def report_summary(request):
    """
    View to display the exam report summary in descending order of exam date, including:
    - Exam name
    - Question paper name
    - Exam date, time, and duration
    - Number of students who attended the exam
    """
    exams = Exam.objects.all().order_by('-exam_date').annotate(
        students_attended=Count('response__student_id', distinct=True)
    )

    report_data = []
    for exam in exams:
        papers = QuestionPaper.objects.filter(exam_id=exam)
        for paper in papers:
            attended_students = Response.objects.filter(exam_id=exam, paper_id=paper).values('student_id').distinct().count()
            report_data.append({
                'exam_name': exam.exam_name,
                'paper_name': paper.paper_name,
                'exam_date': exam.exam_date,
                'exam_time': exam.exam_time,
                'exam_duration': exam.exam_duration,
                'students_attended': attended_students,
                'exam_id': exam.exam_id,
                'paper_id': paper.paper_id,
            })

    return render(request, 'teacher/report_summary.html', {'report_data': report_data})

def detailed_report(request, exam_id, paper_id):
    # Fetch exam and paper details
    exam = get_object_or_404(Exam, exam_id=exam_id)
    paper = get_object_or_404(QuestionPaper, paper_id=paper_id)

    # Get all responses for the exam and paper, grouped by student
    student_results = (
        Response.objects.filter(exam_id=exam_id, paper_id=paper_id)
        .values('student_id', 'student_id__username')  # Get student details
        .annotate(total_scored=Sum('marks_awarded'), total_marks=Sum('total_marks'))  # Aggregate marks
        .order_by('student_id')  # Optional: Order by student
    )

    # Pass data to the template
    return render(request, 'teacher/detailed_report.html', {
        'exam': exam,
        'paper': paper,
        'student_results': student_results,
    })
    
def detailed_student_reponse(request, exam_id, paper_id,student_id):
    # Get the logged-in student (user)
    student = get_object_or_404(User, id=student_id)
    # Get all responses for the logged-in student for the specific exam and paper
    responses = Response.objects.filter(
        student_id=student, 
        exam_id=exam_id, 
        paper_id=paper_id
    ).select_related('exam_id', 'paper_id', 'question_id')
    # Prepare data for the attempted questions
    question_data = []
    for response in responses:
        # Extracting exam, paper, and question details
        exam = response.exam_id
        paper = response.paper_id
        question = response.question_id
        question_data.append({
            'exam': exam,
            'paper': paper,
            'question':question,
            # 'question_text': question.question_text,
            'marks': question.marks,
            'selected_option': response.selection,
            'correct_option': question.correct_option,
            'marks_awarded': response.marks_awarded,
        })    
    return render(request, 'teacher/detailed_report_student_reponse.html', {'student': student, 'question_data': question_data})

