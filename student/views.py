from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from functools import wraps
from django.utils import timezone
from teacher.models import Exam, Question, QuestionPaper, Response
from django.db.models import Q 

def validate_user_role(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if the user is logged in
        if not request.user.is_authenticated:
            return redirect('/auth/login')

        # Check if the user is staff
        if request.user.is_staff:
            context = {
                'error_message': "This is the Student Portal. Please login to the Teacher Portal.",
                'link_text': "Go to the Teacher Portal",
                'link': "/teacher"
            }
            return render(request, 'common/error.html', context)

        # Check if the user is admin
        elif request.user.is_superuser:
            context = {
                'error_message': "This is the Student Portal. Please login to the Admin Portal.",
                'link_text': "Go to the Admin Portal",
                'link': "/admin"
            }
            return render(request, 'common/error.html', context)

        # If user is a student, proceed to the view
        return view_func(request, *args, **kwargs)

    return wrapper

@validate_user_role
def dashboard(request):
    if request.method=="GET":
        return render(request,'student/index.html')
@validate_user_role  
def exams_today(request):
    now = timezone.now()
    # Get QuestionPaper that belongs to exams happening today (exam_date is today and exam_time is after now)
    question_papers_today = QuestionPaper.objects.filter(
        exam_id__exam_date=now.date(), exam_id__exam_time__gt=now.time()
    ).order_by('exam_id__exam_time')

    return render(request, 'student/today_exams.html', {'papers': question_papers_today})
  
@validate_user_role
def upcoming_exams(request):
    now = timezone.now()    
    # Get exams that are scheduled for the future (exam_date is after today)
    upcoming_exams = Exam.objects.filter(exam_date__gt=now.date()).order_by('exam_date', 'exam_time')
    # Alternatively, if you also want to show exams happening today but not yet started
    upcoming_exams_today = Exam.objects.filter(exam_date=now.date(), exam_time__gt=now.time()).order_by('exam_time')    
    # Merge both queries
    upcoming_exams = upcoming_exams | upcoming_exams_today
    return render(request, 'student/upcomming_exam.html', {'exams': upcoming_exams})

@validate_user_role
def past_exams(request):
    now = timezone.now()
    # Get exams that have passed (exam_date is before today OR if exam_date is today and exam_time is before now)
    past_exams = Exam.objects.filter(
        Q(exam_date__lt=now.date()) | Q(exam_date=now.date(), exam_time__lt=now.time())
    ).order_by('-exam_date', '-exam_time')
    return render(request, 'student/past_exams.html', {'exams': past_exams})

@validate_user_role
def student_report(request):
    student = request.user    
    # Get all responses by this student, filtering by student_id
    responses = Response.objects.filter(student_id=student).select_related('exam_id', 'paper_id', 'question_id')
    # Prepare data for the report
    report_data = []
    # Loop through the responses and aggregate data
    for response in responses:
        # Extracting exam, paper, and question details
        exam = response.exam_id
        paper = response.paper_id
        question = response.question_id
        # Check if this paper has already been added to the report data for this student
        paper_data = next((item for item in report_data if item['paper'] == paper), None)
        if not paper_data:
            # If paper data is not yet added, create a new entry
            paper_data = {
                'paper': paper,
                'exam': exam,
                'total_score': sum(q.marks for q in Question.objects.filter(paper_id=paper)),  # Sum of marks in the paper
                'marks_scored': 0,  # Initialize scored marks
                'questions': []
            }
            report_data.append(paper_data)
        # Add the response data to the paper's marks scored
        paper_data['marks_scored'] += response.marks_awarded
        paper_data['questions'].append({
            'question_text': question.question_text,
            'marks': question.marks,
            'selected_option': response.selection,
            'correct_option': question.correct_option,
            'marks_awarded': response.marks_awarded,
        })
    # Render the report template
    return render(request, 'student/student_report.html', {'student': student, 'report_data': report_data})
@validate_user_role
def attempted_questions(request, exam_id, paper_id):
    # Get the logged-in student (user)
    student = request.user
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
    return render(request, 'student/attempted_questions.html', {'student': student, 'question_data': question_data})
