from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import *


app_name = "authentication"

urlpatterns = [
    path('student/register', RegisterStudentView.as_view(), name='student-register'),
    path('activate-user/<uidb64>/<token>', views.activate_account, name='activate'),
    path('student/profile/update/', EditStudentProfileView.as_view(), name='student-profile-update'),
    path('student/profile/changepassword/', views.student_change_password, name='student-change-password'),
    path('instructor/profile/changepassword/', views.instructor_change_password, name='instructor-change-password'),
    path('instructor/register', RegisterInstructorView.as_view(), name='instructor-register'),
    path('instructor/profile/update/', EditInstructorProfileView.as_view(), name='instructor-profile-update'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='authentication/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/password/password_reset_complete.html'), name='password_reset_complete'),
]
