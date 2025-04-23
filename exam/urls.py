from django.urls import path
from . import views

urlpatterns = [
    path('conduct-exam/<int:exam_id>/<int:paper_id>/', views.conduct_exam, name='conduct_exam'),
    
    
]
