from django.contrib import admin
from .models import Course, Assignment, AssignmentSubmission, Student, CourseAssignment

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(Student)
admin.site.register(CourseAssignment)



