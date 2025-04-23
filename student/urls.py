from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard , name='dashboard'),    
    path('exams/',views.exams_today , name='today_exams'),    
    path('upcomming-exams/',views.upcoming_exams , name='upcomming_exams'),    
    path('past-exams/',views.past_exams , name='past_exams'),    
    path('reports/',views.student_report , name='student_reports'), 
    path('attempted-questions/<int:exam_id>/<int:paper_id>/', views.attempted_questions, name='attempted_questions'),       
]
