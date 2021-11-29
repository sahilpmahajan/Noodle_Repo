from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
                  path('application/', HomeView.as_view(), name='home'),
                  path('', HomeView.as_view(), name='home'),
                  path('course/', view_courselist, name='course'),
                  path('course-create/', CourseCreateView.as_view(), name='course-create'),
                  path('<int:id>/assignment/assignment-create/', assignment_create, name='assignment-create'),
                  path('<int:id>/assignment/', view_assignmentlist, name='assignment-list'),
                  path('<int:id>/course-view/registered-students/', view_registered_students, name='registered-students'),
                  path('<int:id>/delete/', delete_assignment, name='delete-assignment'),
                  path('<int:id>/course-view/registered-students/deregister_student/<int:pk>', deregister_student, name='deregister_student'),
                  path('<int:id>/course-view/', course_single, name='course-view'),
                  path('<int:id>/course-register', course_single_register, name='course-register'),
                  path('<int:id>/assignment/<int:pk>/assignment-submission', assignment_submit, name='assignment-submission'),
                  #path('<int:id>/assignment/assignment-submission-list/<int:pk>', AssignmentSubmissionListView.as_view(), name='assignment-submission-list'),
                  path('<int:id>/assignment/<int:pk>/submitted-assignment', view_assignmentsubmissionlist, name='submitted-assignment'),
                  path('<int:id>/assignment/<int:pk>/submitted-assignment/<int:cd>/assignment-feedback',assignment_feedback, name='assignment-feedback'),
                  path('<pk>/submission-delete/', delete_assignmentsubmission, name='submission-delete'),
                  path('<pk>/delete-course/', CourseDelete.as_view(), name='delete-course'),
                  path('<int:id>/assignment/<int:pk>/submitted-assignment/upload-csv', upload_csv, name='upload-csv'),
                  path('<int:id>/assignment/<int:pk>/submitted-assignment/upload-autograder', autograder, name='upload-autograder'),
                  path('<int:id>/assignment/<int:pk>/submitted-assignment/assignment-chart', assignment_chart, name='assignment-chart'),
                  path('<int:id>/assignment/assignment-course-chart', assignment_course_average_chart, name='assignment-course-chart'),
                  path('<int:id>/assignment/course-total', course_total_chart, name='course-total'),
                  path('todo-list/', student_to_do_list, name='student-todo-list'),
                  path('<int:id>/discussion/', view_discussionlist, name='discussion-list'),
                  path('<int:id>/discussion/<int:pk>/comments', view_commentslist, name='comments-list'),
                  path('<int:id>/discussion/<int:pk>/comment-create/', comment_create, name='comments-create'),
                  path('<int:id>/discussion/discussion-create/', discussion_create, name='discussion-create'),
                  path('failed/', invalid_submission, name='invalid-submission'),
                  path('<int:id>/course/change-course-code/', change_course_code, name='change-course-code'),
                  path('<int:id>/course/remove-course-student/', removefromcourse, name='remove-student-course'),
                  path('<int:id>/course/add-course-student/', addtocourse, name='add-student-course'),
                  path('<int:id>/course/<int:pk>/discussion-notif', getnotifs,name = 'discussion-notif'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
