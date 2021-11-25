from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authentication.decorators import user_is_instructor, user_is_student
from django.core.mail import send_mail
from django.conf import settings

from .forms import *
from .models import *


class HomeView(ListView):
    paginate_by = 6
    template_name = 'home.html'
    model = Course
    context_object_name = 'course'

    def get_queryset(self):
        return self.model.objects.all()


# COURSE CREATE VIEW
class CourseCreateView(CreateView):
    template_name = 'core/instructor/course_create.html'
    form_class = CourseCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('core:course')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'instructor':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CourseCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# VIEW FOR COURSE LIST
class CourseView(ListView):
    model = Course
    template_name = 'core/instructor/courses.html'
    context_object_name = 'course'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')


def course_single(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "core/instructor/view_course.html", {'course': course})


# REGISTER COURSE
def course_single_register(request, id):
    course = get_object_or_404(Course, id=id)
    if(request.method == 'POST'):
        course_code = request.POST.get("course_code")
        if(str(course.course_description) == str(course_code)):
            return render(request, "core/instructor/view_course.html", {'course': course})
    
    return render(request, "core/instructor/register_course.html", {'course': course})


# ASSIGNMENT CREATE VIEW
class AssignmentCreateView(CreateView):
    template_name = 'core/instructor/assignment_create.html'
    form_class = AssignmentCreateForm
    extra_context = {
        'title': 'New Course'
    }
    success_url = reverse_lazy('core:assignment-list')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'instructor':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# VIEW FOR ASSIGNMENT LIST
class AssignmentView(ListView):
    model = Assignment
    template_name = 'core/instructor/assignments.html'
    context_object_name = 'assignment'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # @method_decorator(user_is_student, user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()  # filter(user_id=self.request.user.id).order_by('-id')


# DELETE ASSIGNMENT VIEW
class AssignmentDeleteView(DeleteView):
    model = Assignment
    success_url = reverse_lazy('core:assignment-list')


# ASSIGNMENT SUBMISSION VIEW
class AssignmentSubmissionView(CreateView):
    template_name = 'core/instructor/assignment_submission.html'
    form_class = AssignmentSubmissionForm
    extra_context = {
        'title': 'New Exam'
    }
    success_url = reverse_lazy('core:home')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('authentication:login')
        if self.request.user.is_authenticated and self.request.user.role != 'student':
            return reverse_lazy('authentication:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssignmentSubmissionView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# VIEW FOR Assignment Submission List
class AssignmentSubmissionListView(ListView):
    model = AssignmentSubmission
    template_name = 'core/instructor/assignment_submission_list.html'
    context_object_name = 'assignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # @method_decorator(user_is_instructor, user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

# VIEW FOR Submitted Assignment
class SubmittedAssignment(ListView):
    model = AssignmentSubmission
    template_name = 'core/instructor/submitted_assignment.html'
    context_object_name = 'assignment_submission'

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    @method_decorator(user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')



# ASSIGNMENT FEEDBACK VIEW
class AssignmentFeedback(UpdateView):
    template_name = 'core/instructor/assignment_feedback.html'
    #form_class = FeedbackForm
    model = AssignmentSubmission
    fields = ['feedback']

    success_url = reverse_lazy('core:assignment-submission-list')

    # @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    # def dispatch(self, request, *args, **kwargs):
    #     if not self.request.user.is_authenticated:
    #         return reverse_lazy('authentication:login')
    #     if self.request.user.is_authenticated and self.request.user.role != 'instructor':
    #         return reverse_lazy('authentication:login')
    #     return super().dispatch(self.request, *args, **kwargs)

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super(AssignmentFeedback, self).form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     self.object = None
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)



# ASSIGNMENT DELETE VIEW
class AssignmentSubmissionDelete(DeleteView):
    model = AssignmentSubmission
    success_url = reverse_lazy('core:assignment-submission-list')


# COURSE DELETE VIEW
class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('core:home')






