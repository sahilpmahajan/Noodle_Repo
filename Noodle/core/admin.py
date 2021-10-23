from django.contrib import admin
from .models import Course, Assignment, AssignmentSubmission

admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)

