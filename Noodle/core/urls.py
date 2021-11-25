from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
                  path('application/', HomeView.as_view(), name='home'),
                  path('', HomeView.as_view(), name='home'),
                  path('course/', CourseView.as_view(), name='course'),
                  path('course-create/', CourseCreateView.as_view(), name='course-create'),
                  path('assignment-create/', AssignmentCreateView.as_view(), name='assignment-create'),
                  path('assignment/', AssignmentView.as_view(), name='assignment-list'),
                  path('<pk>/delete/', AssignmentDeleteView.as_view(), name='delete-assignment'),
                  path('<int:id>/course-view/', course_single, name='course-view'),
                  path('<int:id>/course-register', course_single_register, name='course-register'),
                  path('assignment-submission/', AssignmentSubmissionView.as_view(), name='assignment-submission'),
                  path('assignment-submission-list/', AssignmentSubmissionListView.as_view(), name='assignment-submission-list'),
                  path('submitted-assignment/', SubmittedAssignment.as_view(), name='submitted-assignment'),
                  path('<pk>/assignment-feedback/', AssignmentFeedback.as_view(), name='assignment-feedback'),
                  path('<pk>/submission-delete/', AssignmentSubmissionDelete.as_view(), name='submission-delete'),
                  path('<pk>/delete-course/', CourseDelete.as_view(), name='delete-course')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
