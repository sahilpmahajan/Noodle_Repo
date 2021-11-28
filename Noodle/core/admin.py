from django.contrib import admin
from .models import Course, Assignment, AssignmentSubmission, Student, CourseAssignment, Post, Comment

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(Student)
admin.site.register(CourseAssignment)
admin.site.register(Post)
admin.site.register(Comment)


