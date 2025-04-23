from django.http import HttpResponse
from django.utils.timezone import now, make_aware, localtime
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required   
from django.shortcuts import render, redirect, get_object_or_404
from teacher.models import Exam,QuestionPaper, Question, Response
from django.contrib import messages


@login_required
def conduct_exam(request, exam_id, paper_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    paper = get_object_or_404(QuestionPaper, pk=paper_id, exam_id=exam)
    
    # Check if the user has already attempted the exam
    if Response.objects.filter(student_id=request.user, exam_id=exam, paper_id=paper).exists():
        messages.error(request, "You have already attempted this exam.")
        return redirect('/student/')  # Redirect to the student portal


    # Convert exam times to timezone-aware datetimes
    exam_start_time = make_aware(datetime.combine(exam.exam_date, exam.exam_time))
    exam_end_time = exam_start_time + exam.exam_duration

    # Get current time in the local timezone
    current_time = localtime(now())  # Localized to TIME_ZONE in settings.py

    print(f"Current Time (Local): {current_time}")
    print(f"Exam Start Time (Local): {localtime(exam_start_time)}")
    print(f"Exam End Time (Local): {localtime(exam_end_time)}")

    # Adjust start and end times to local timezone for comparison
    exam_start_time = localtime(exam_start_time)
    exam_end_time = localtime(exam_end_time)

    if not (exam_start_time < current_time  or exam_end_time<current_time):
        return redirect('/student/')

    # Fetch questions for the paper
    questions = Question.objects.filter(exam_id=exam, paper_id=paper)

    # If form is submitted
    if request.method == 'POST':
        for question in questions:
            selected_option = request.POST.get(f'question_{question.question_id}')
            if selected_option:
                Response.objects.update_or_create(
                    student_id=request.user,
                    exam_id=exam,
                    paper_id=paper,
                    question_id=question,
                    defaults={
                        'selection': int(selected_option),
                        'total_marks': question.marks,
                    }
                )
        return redirect('/student/')

    # Calculate remaining time
    remaining_time = (exam_end_time - current_time).total_seconds()

    # Render the exam page
    return render(request, 'exam/conduct_exam.html', {
        'exam': exam,
        'paper': paper,
        'questions': questions,
        'remaining_time': remaining_time,
    })
