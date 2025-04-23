from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_name = models.CharField(max_length=255)
    exam_date = models.DateField()
    exam_time = models.TimeField()
    exam_duration = models.DurationField()


    def __str__(self):
        return self.exam_name

class QuestionPaper(models.Model):
    paper_id = models.AutoField(primary_key=True)
    paper_name = models.CharField(max_length=255)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)

    def __str__(self):
        return self.paper_name

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField()
    option1 = models.TextField()
    option2 = models.TextField()
    option3 = models.TextField()
    option4 = models.TextField()
    correct_option = models.IntegerField()
    marks = models.IntegerField()
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
    paper_id=models.ForeignKey(QuestionPaper,on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

# class Response(models.Model):
#     student_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE)
#     question_paper_id = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)
#     question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
#     selection = models.IntegerField()

#     def __str__(self):
#         return f"Response by {self.student_id} for {self.exam_id}"

class Response(models.Model):
    response_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming User model for students
    exam_id = models.ForeignKey('Exam', on_delete=models.CASCADE)
    paper_id = models.ForeignKey('QuestionPaper', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    selection = models.IntegerField()  # The student's selected option
    marks_awarded = models.IntegerField(default=0)  # Marks awarded for this question
    total_marks = models.IntegerField()  # Marks this question is worth

    def __str__(self):
        return f"Response by {self.student_id} for Paper {self.paper_id} (Question {self.question_id})"

    def check_correctness(self):
        """
        Method to check if the student's selection is correct.
        Returns True if correct, False if incorrect.
        """
        return self.selection == self.question_id.correct_option
    
    def save(self, *args, **kwargs):
        """
        Overriding the save method to assign marks based on correctness.
        """
        if self.check_correctness():
            self.marks_awarded = self.total_marks  # Full marks if correct
        else:
            self.marks_awarded = 0  # No marks if incorrect
        super().save(*args, **kwargs)  # Save the Response instance
