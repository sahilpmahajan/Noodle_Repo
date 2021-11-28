from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from authentication.decorators import user_is_instructor, user_is_student
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import statistics 
from django.utils import timezone


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
        foo = super(CourseCreateView, self).form_valid(form)
        course_name = form.cleaned_data['course_name']
        course = Course.objects.get(course_name = course_name)
        course.user = self.request.user
        course.save()
        return foo

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


# # VIEW FOR COURSE LIST
# class CourseView(ListView):
#     model = Course
#     template_name = 'core/instructor/courses.html'
#     context_object_name = 'course'

#     @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
#     # @method_decorator(user_is_instructor, user_is_student)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(self.request, *args, **kwargs)

#     def get_queryset(self):
#         return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')

def view_courselist(request):
    if(request.user.role=='student'):
        user = User.objects.get(id=request.user.id)
        student_list = []
        for student in user.student_set.all():
            student_list.append(student.course)
        return render(request, "core/instructor/courses.html", {'course': student_list})
    elif(request.user.role=='instructor'):
        #user = Course.objects.get(id=request.user.id).user
        return render(request, "core/instructor/courses.html", {'course': request.user.course_set.all()})


# SINGLE COURSE VIEW
def course_single(request, id):
    course = get_object_or_404(Course, id=id)
    id=id
    is_registered = 0
    submitted = []
    total = []
    complete = 0
    for user in course.student_set.all():
        if(request.user.email == user.user.email):
            is_registered = 1
    if is_registered == 1:
        assignment_list = Assignment.objects.filter(course = course)            
        for assignment in assignment_list:
            total.append(assignment)
            if request.user.assignmentsubmission_set.filter(assignment = assignment):
                    submitted.append(assignment)
        complete = len(submitted)/len(total) * 100
        complete = str(round(complete, 2))
    return render(request, "core/instructor/view_course.html", {
        'course': course , 
        'is_registered': is_registered,
        'complete' : complete
        })


# REGISTER COURSE
def course_single_register(request, id):
    course = get_object_or_404(Course, id=id)
    if(request.method == 'POST'):
        course_code = request.POST.get("course_code")
        if(str(course.course_description) == str(course_code)):
            new_student = Student(course = course, user = request.user)
            new_student.save() 
            return render(request, "core/instructor/view_course.html", {'course': course})
    
    return render(request, "core/instructor/register_course.html", {'course': course})


# ASSIGNMENT CREATE VIEW
# class AssignmentCreateView(CreateView):
#     template_name = 'core/instructor/assignment_create.html'
#     form_class = AssignmentCreateForm
#     extra_context = {
#         'title': 'New Course'
#     }
#     success_url = reverse_lazy('core:assignment-list')

#     @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return reverse_lazy('authentication:login')
#         if self.request.user.is_authenticated and self.request.user.role != 'instructor':
#             return reverse_lazy('authentication:login')
#         return super().dispatch(self.request, *args, **kwargs)

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         foo = super(AssignmentCreateView, self).form_valid(form)
#         form.instance.course = self.kwargs.get('id')
#         ass_name = form.cleaned_data['title']
#         ass = Assignment.objects.get(title = ass_name)
#         ass.save()
#         return foo

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

def assignment_create(request, id):
    #user = request.user
    course = get_object_or_404(Course, id=id)
    if(request.method == 'POST'):
        title = request.POST['title']
        content = request.POST['content']
        marks = request.POST['marks']
        duration = request.POST['duration']
        weight = request.POST['weight']
        due_date = request.POST['due_date']
        ass = Assignment.objects.create(course=course, title = title, content=content, marks=marks, duration=duration, weight=weight, due_date = due_date)
        ass.save()
        return redirect(f"http://127.0.0.1:8000/{id}/assignment")
    return render(request, "core/instructor/assignment_create.html")
# VIEW FOR ASSIGNMENT LIST
# class AssignmentView(ListView):
#     model = Assignment
#     template_name = 'core/instructor/assignments.html'
#     context_object_name = 'assignment'

#     @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
#     # @method_decorator(user_is_student, user_is_instructor)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(self.request, *args, **kwargs)

#     def get_queryset(self):
#         return self.model.objects.all()  # filter(user_id=self.request.user.id).order_by('-id')

def view_assignmentlist(request, id):
        # user = User.objects.get(id=request.user.id)
        course = get_object_or_404(Course, id=id)
        id=id
        assignment_list = Assignment.objects.filter(course = course)
        
        if(request.user.role == 'student'):
            submitted = []
            not_submitted = []
            for assignment in assignment_list:
                    if request.user.assignmentsubmission_set.filter(assignment = assignment):
                        submitted.append(assignment)
                    else:
                        not_submitted.append(assignment)
            return render(request, "core/instructor/assignments.html", {'not_submitted': not_submitted , 'id': id, 'submitted': submitted})
        elif(request.user.role == 'instructor'):
            return render(request, "core/instructor/assignments.html", {'assignment': assignment_list , 'id': id})

# # DELETE ASSIGNMENT VIEW
# class AssignmentDeleteView(DeleteView):
#     model = Assignment
#     success_url = reverse_lazy('core:assignment-list')

def delete_assignment(request,id):

    assign = Assignment.objects.filter(id=id)
    #c_id = assign.course_id
    assign.delete()
    return redirect(f"http://127.0.0.1:8000/course")

# ASSIGNMENT SUBMISSION VIEW
# class AssignmentSubmissionView(CreateView):
#     template_name = 'core/instructor/assignment_submission.html'
#     form_class = AssignmentSubmissionForm
#     extra_context = {
#         'title': 'New Exam'
#     }
#     success_url = reverse_lazy('core:home')

#     @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
#     def dispatch(self, request, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return reverse_lazy('authentication:login')
#         if self.request.user.is_authenticated and self.request.user.role != 'student':
#             return reverse_lazy('authentication:login')
#         return super().dispatch(self.request, *args, **kwargs)

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(AssignmentSubmissionView, self).form_valid(form)

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)

#put this instead of your assignment_submit
def assignment_submission_is_valid(due_date):
    now = timezone.localtime(timezone.now())
    print(now)
    print(due_date)
    if(now <= due_date):  # before submission deadline
        return True
    return False


def assignment_submit(request, id, pk):
    #user = request.user
    #course = get_object_or_404(Course, id=id)
    assignment = get_object_or_404(Assignment, pk=pk)
    # doubt number 1 : how to get date from assignment
    # doubt number 2 : do we need to add invalid submission in urls.py
    print(assignment.title)
    print('hello')
    if(assignment_submission_is_valid(assignment.due_date)):
        if(request.method == 'POST'):
            name = request.POST['name']
            university_id = request.POST['university_id']
            content = request.POST['content']
            file = request.FILES['file']
            ass_sub = AssignmentSubmission.objects.create(
                user=request.user, assignment=assignment, name=name, content=content, university_id=university_id, file=file)
            ass_sub.save()
            return redirect("http://127.0.0.1:8000/")
        return render(request, "core/instructor/assignment_submission.html")
    else:
        return redirect("http://127.0.0.1:8000/failed")


def invalid_submission(request):
    return render(request, "core/invalid_submission.html")

# VIEW FOR Assignment Submission List
# class AssignmentSubmissionListView(ListView):
#     model = AssignmentSubmission
#     template_name = 'core/instructor/submitted_assignment.html'
#     context_object_name = 'assignment_submission'

#     @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
#     # @method_decorator(user_is_instructor, user_is_student)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(self.request, *args, **kwargs)

#     def get_queryset(self):
#         return self.model.objects.all().order_by('-id')  # filter(user_id=self.request.user.id).order_by('-id')


# VIEW FOR Submitted Assignment
# class SubmittedAssignment(ListView):
#     model = AssignmentSubmission
#     template_name = 'core/instructor/submitted_assignment.html'
#     context_object_name = 'assignment_submission'

#     @method_decorator(login_required(login_url=reverse_lazy('authentication:login')))
#     @method_decorator(user_is_student)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(self.request, *args, **kwargs)

#     def get_queryset(self):
#         return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')

def view_assignmentsubmissionlist(request, id, pk):
        # user = User.objects.get(id=request.user.id)
        #course = get_object_or_404(Course, id=id)
        assignment = get_object_or_404(Assignment, pk=pk)
        id=id
        pk=pk
        if(request.user.role == 'student'):
            assignmentsub_list = AssignmentSubmission.objects.filter(assignment = assignment, user = request.user)
        else:
            assignmentsub_list = AssignmentSubmission.objects.filter(assignment = assignment)
        return render(request, "core/instructor/submitted_assignment.html", {'assignment_submission': assignmentsub_list , 'id': id, 'pk': pk})


# # ASSIGNMENT FEEDBACK VIEW
# class AssignmentFeedback(UpdateView):
#     template_name = 'core/instructor/assignment_feedback.html'
#     #form_class = FeedbackForm
#     model = AssignmentSubmission
#     fields = ['feedback','marks_obtained']

#     success_url = reverse_lazy('core:assignment-submission')

def assignment_feedback(request, id, pk, cd):
    #user = request.user
    #course = get_object_or_404(Course, id=id)
    #assignment = get_object_or_404(Assignment, cd=cd)
    if(request.method == 'POST'):
        feedback = request.POST['feedback']
        marks_obtained = request.POST['marks_obtained']
        ass_sub = get_object_or_404(AssignmentSubmission, id=cd)
        ass_sub.feedback = feedback
        ass_sub.marks_obtained = marks_obtained
        ass_sub.save()
        return redirect(f"http://127.0.0.1:8000/{id}/assignment/{pk}/submitted-assignment")
    return render(request, "core/instructor/assignment_feedback.html")



# ASSIGNMENT DELETE VIEW
# class AssignmentSubmissionDelete(DeleteView):
#     model = AssignmentSubmission
#     success_url = reverse_lazy('core:assignment-submission')

def delete_assignmentsubmission(request,pk):

    assignsub = AssignmentSubmission.objects.filter(pk=pk)
    assignsub.delete()
    return redirect(f"http://127.0.0.1:8000/course")

# COURSE DELETE VIEW
class CourseDelete(DeleteView):
    model = Course
    success_url = reverse_lazy('core:home')


#CSV upload view
def upload_csv(request,id,pk):
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            
            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)
            
            file_data = csv_file.read().decode("utf-8")
            csv_data = file_data.split("\n")
            assignment = get_object_or_404(Assignment, pk=pk)
            assignmentsub_list = AssignmentSubmission.objects.filter(assignment = assignment)
            # qs = AssignmentSubmission.objects.filter(id = pk)
            for item in assignmentsub_list:
                
                for x in csv_data:
                    fields = x.split(",")
                    if item.university_id == fields[0]:
                        
                        item.marks_obtained = fields[1]
                        item.feedback = fields[2]
                        item.save()
            

            return redirect(f"http://127.0.0.1:8000/{id}/assignment/{pk}/submitted-assignment")


        form = CsvImportForm()
        data = {"form": form}
        return render(request, "core/csv_upload.html", data)


#View for Chart.js

def assignment_chart(request,id,pk):
    labels = []
    data = []
    labelstudent = []
    datastudent = []
    assignment = get_object_or_404(Assignment, pk=pk)
    
    assignmentsub_list = AssignmentSubmission.objects.filter(assignment = assignment)
    for item in assignmentsub_list:
        labels.append(item.university_id)
        data.append(item.marks_obtained)
    average = sum(data)/len(data)
    labels.append("Average")
    data.append(average)
    var = statistics.variance(data)
    labels.append("Variance")
    data.append(var)
    assignmentStudent = AssignmentSubmission.objects.filter(assignment = assignment, user = request.user)
    for item in assignmentStudent:
        labelstudent.append("Your Marks")
        datastudent.append(item.marks_obtained)
        if(item.marks_obtained < average):
            warning = "Warning: Your Marks are below Average for this assignment"
        else:
            warning = "Congrats: Your Marks are above Average for this assignment"
    labelstudent.append("Average")
    labelstudent.append("Variance")
    datastudent.append(average)
    datastudent.append(var)

    if(request.user.role == "instructor"):
        return render(request, 'core/chart/assignment_submission_chart.html', {
            'labels' : labels,
            'data' : data,
        })

    else:
        return render(request, 'core/chart/assignment_submission_chart.html', {
            'labels' : labelstudent,
            'data' : datastudent,
            'warning' : warning
        }
    )

def assignment_course_average_chart(request,id):
        course = get_object_or_404(Course, id=id)
        id=id
        assignment_list = Assignment.objects.filter(course = course)
        labels = []
        data = []
        dataset = []
        if(request.user.role == 'instructor'):
            for assignment in assignment_list:
                    submissions = assignment.assignmentsubmission_set.all()
                    for submission in submissions:
                        dataset.append(submission.marks_obtained)
                    mean = sum(dataset)/len(dataset)
                    var = statistics.variance(dataset)
                    data.append(mean)
                    data.append(var)
                    labels.append("Average "+assignment.title)
                    labels.append("Variance "+assignment.title)
            return render(request, "core/chart/assignment_submission_chart.html", 
            {'labels': labels , 
            'data': data
            })

def course_total_chart(request,id):
    course = get_object_or_404(Course, id=id)
    id=id
    assignment_list = Assignment.objects.filter(course = course)
    labels = []
    data = []
    totalmarksweighted = 0
    totalobtainedweighted = 0
    for assignment in assignment_list:
        submission = assignment.assignmentsubmission_set.filter(user = request.user)
        w = float(assignment.weight)
        a = float(assignment.marks)
        for item in submission:
            s = float(item.marks_obtained)
        totalmarksweighted += a * w
        totalobtainedweighted += s * w
    labels.append("Course Total(Weighted)")
    labels.append("Your Marks(Weighted)")
    data.append(totalmarksweighted)
    data.append(totalobtainedweighted)
    return render(request, "core/chart/assignment_submission_chart.html", 
            {'labels': labels , 
            'data': data
            })

#TO-DO LIST VIEW

def student_to_do_list(request):
        assignment_list = Assignment.objects.filter()
        
        if(request.user.role == 'student'):
            submitted = []
            not_submitted = []
            for assignment in assignment_list:
                    if request.user.assignmentsubmission_set.filter(assignment = assignment):
                        submitted.append(assignment)
                    else:
                        not_submitted.append(assignment)
            return render(request, "core/student_todo_list.html", {'not_submitted': not_submitted , 'id': request.user.id, 'submitted': submitted})

        else:
            courses = Course.objects.filter(user = request.user)
            ass_sub_list = []
            for course in courses:
                course_ass = []
                assignments = Assignment.objects.filter(course = course)
                for assignment in assignments:
                    ass_subs = []
                    assignmentsubmissions = AssignmentSubmission.objects.filter(assignment=assignment)
                    for assignmentsubmission in assignmentsubmissions:
                        if(not assignmentsubmission.feedback):
                            ass_subs.append(assignmentsubmission)
                    course_ass.append(ass_subs)
            
                ass_sub_list.append(course_ass)

            return render(request, "core/student_todo_list.html", {'ass_sub_list': ass_sub_list})
            #ass_sub.assignment.course.course_name
            #ass_sub.assignment.title
            #ass_sub.name

def view_commentslist(request, id, pk):
                #course = get_object_or_404(Course, id=id)
                # time = timezone.localtime(timezone.now())
                post = get_object_or_404(Post, pk=pk)
                id = id
                pk = pk
                comments_list = Comment.objects.filter(post = post)
                # if(request.method == 'POST'):
                #         content = request.POST['content']
                #         com = Comment.objects.create(
                #             post = post, user=request.user, content=content, time = time)
                #         com.save()
                #         return redirect('core:home')
                return render(request, "core/comments.html", {'comments_list': comments_list, 'id': id, 'pk' : pk})

def comment_create(request, id, pk):
    post = get_object_or_404(Post, pk=pk)
    id = id
    pk = pk
    time = timezone.localtime(timezone.now())
    if(request.method == 'POST'):
            print('Avi in POST')
            content = request.POST.get('content', False)
            com = Comment.objects.create(
                post = post, user=request.user, content=content, time = time)
            com.save()
            return redirect(f"http://127.0.0.1:8000/{id}/discussion/{pk}/comments")
    return render(request, "core/create_comment.html", {'id':id, 'pk':pk})

def view_discussionlist(request, id):
    # user = User.objects.get(id=request.user.id)
    course = get_object_or_404(Course, id=id)
    id = id
    discussion_list = Post.objects.filter(course=course)
    return render(request, "core/discussions.html", {'discussion_list': discussion_list, 'id': id})

def discussion_create(request, id):
    course = get_object_or_404(Course, id=id)
    time = timezone.localtime(timezone.now())
    if(request.method == 'POST'):
        topic = request.POST['topic']
        post = Post.objects.create(course=course, topic=topic, time=time)
        post.save()
        return redirect(f"http://127.0.0.1:8000/{id}/discussion")
    return render(request, "core/instructor/discussion_create.html")