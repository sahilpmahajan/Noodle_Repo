from django.db import models
from authentication.models import User
from django.utils import timezone


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    #course_image = models.ImageField(upload_to='media')
    teacher_name = models.CharField(max_length=50)
    teacher_details = models.TextField()
    student_code = models.CharField(max_length=6)
    ta_code =models.CharField(max_length=6)
    created_at = models.DateField(default=timezone.now)
    end_date = models.CharField(max_length=20)
    # end_date = models.DateField(max_length=20)


    def __str__(self):
        return self.course_name


class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    marks = models.CharField(max_length=20)
    duration = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now())
    weight = models.DecimalField(
                         max_digits = 3,
                         decimal_places = 2)
    due_date = models.DateTimeField(default = timezone.now())
    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    university_id = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    feedback = models.TextField(default='')
    file = models.FileField(null=True, blank=True)
    marks_obtained = models.IntegerField(default = 0)

    def __str__(self):
        return self.university_id

class Student(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ta = models.BooleanField()

class CourseAssignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)


class Post(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.TextField(null=True, blank=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    time = models.DateTimeField(default=timezone.localtime(timezone.now()))