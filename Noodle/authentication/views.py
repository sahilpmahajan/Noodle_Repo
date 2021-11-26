from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages, auth
from django.contrib.auth import update_session_auth_hash, login
from django.core.mail.message import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.views.generic import CreateView, FormView, RedirectView, UpdateView
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .tokens import account_activation_token
from .forms import *
from .models import User

from django.urls import reverse_lazy
from .decorators import user_is_student, user_is_instructor
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.db.models.query_utils import Q

#ACTIVATE ACCOUNT
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activated successfully')
    else:
        return HttpResponse('Activation link is invalid!')


# STUDENT REGISTRATION VIEW
class RegisterStudentView(CreateView):
    model=User
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
            user.is_active = False # Deactivate account till it is confirmed
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to = [to_email])
            email.send()
            messages.success(request, ('Please Confirm your email to complete registration.'))
            #send email if valid registeration, recipient_list mein put email of the user who just registered
            #subject = 'Thank you for registering to our site'
            #message = ' It is a decent site.'
            #email_from = settings.EMAIL_HOST_USER
            #recipient_list = ['soumyasinghdahiya2001@gmail.com',]
            #send_mail( subject, message, email_from, recipient_list )       

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
            #added new
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            ##############################3
            htmly = get_template('authentication/instructor/email.html')
            d = { 'username': username }
            subject, from_email, to = 'welcome', 'aviuday03@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            ########################################
            messages.success(request, f'Your account has been created! You should now be able to log in.')
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

#PASSWORD RESET
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = get_user_model().objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "authentication/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Float Moodle',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'aviuday03@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')

					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect('authentication:password_reset_done')
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="authentication/password/password_reset.html", context={"password_reset_form":password_reset_form})


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
 
