from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import CreateView, FormView, RedirectView, UpdateView
from django.http import Http404

from .forms import *
from .models import User

from django.urls import reverse_lazy
from .decorators import user_is_student, user_is_instructor
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# STUDENT REGISTRATION VIEW
class RegisterStudentView(CreateView):
    model = User
    form_class = StudentRegistrationForm
    template_name = 'authentication/student/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('authentication:login')
        else:
            return render(request, 'authentication/student/register.html', {'form': form})


# STUDENT PROFILE EDIT VIEW
class EditStudentProfileView(UpdateView):
    model = User
    form_class = StudentProfileUpdateForm
    context_object_name = 'student'
    template_name = 'authentication/student/edit-profile.html'
    success_url = reverse_lazy('authentication:student-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_student)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("Invalid Username or Password")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Patient doesn't exists")
        return obj


# REGISTER INSTRUCTOR VIEW
class RegisterInstructorView(CreateView):
    model = User
    form_class = InstructorRegistrationForm
    template_name = 'authentication/instructor/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(data=request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('authentication:login')
        else:
            return render(request, 'authentication/instructor/register.html', {'form': form})


# INSTRUCTOR PROFILE EDIT VIEW
class EditInstructorProfileView(UpdateView):
    model = User
    form_class = InstructorProfileUpdateForm
    context_object_name = 'instructor'
    template_name = 'authentication/instructor/edit-profile.html'
    success_url = reverse_lazy('authentication:instructor-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
    @method_decorator(user_is_instructor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("Invalid username or Password")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Patient doesn't exists")
        return obj


# LOGIN VIEW FOR BOTH USER
class LoginView(FormView):
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'authentication/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


# LOGOUT VIEW
class LogoutView(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)

#CHANGE STUDENT PASSWORD

def student_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authentication/student/student-change-password.html', {
        'form': form
    })

#CHANGE INSTRUCTOR PASSWORD
def instructor_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'authentication/instructor/instructor-change-password.html', {
        'form': form
    })
 
