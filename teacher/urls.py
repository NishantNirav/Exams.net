from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('',views.dashboard , name='dashboard'),   
    # Exam
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/create/', views.create_exam, name='create_exam'),
    path('exams/update/<int:exam_id>/', views.update_exam, name='update_exam'),
    path('exams/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),
    # Question Paper
    path('question-paper/', views.question_paper_list, name='question_paper_list'),
    path('question-paper/create/', views.create_question_paper, name='create_question_paper'),
    path('question-paper/update/<int:paper_id>/', views.update_question_paper, name='update_question_paper'),
    path('question-paper/delete/<int:paper_id>/', views.delete_question_paper, name='delete_question_paper'),
    # Question
    path('exam/<int:exam_id>/paper/<int:paper_id>/questions/', views.question_list, name='question_list'),
    path('exam/<int:exam_id>/paper/<int:paper_id>/questions/create/', views.create_question, name='create_question'),
    path('exam/<int:exam_id>/paper/<int:paper_id>/question/<int:question_id>/update/', views.update_question, name='update_question'),
    path('exam/<int:exam_id>/paper/<int:paper_id>/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    # Reports
    # path('save_all_responses/<int:student_id>/<int:exam_id>/<int:paper_id>/', views.save_all_responses, name='save_all_responses'),
    # path('view_exam_results/<int:exam_id>/', views.view_exam_results, name='view_exam_results'),
     path('reports/', views.report_summary, name='report_summary'),
    path('detailed_report/<int:exam_id>/<int:paper_id>/', views.detailed_report, name='detailed_report'),
    path('detailed-report/student-response/<int:exam_id>/<int:paper_id>/<int:student_id>/', views.detailed_student_reponse, name='attempted_questions'),       

 
]
