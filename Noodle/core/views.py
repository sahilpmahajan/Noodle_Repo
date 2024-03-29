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
from django.template.loader import get_template
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import subprocess
import os
import argparse
import re
from shutil import copyfile

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
        course.teacher_name = self.request.user.first_name + " " + self.request.user.last_name
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
    student = Student.objects.filter(course=course, user=request.user)
    student_id = 0
    for item in student:
        student_id = item.id
    id=id
    is_registered = 0
    submitted = []
    total = []
    complete = 0
    is_ta = 0
    is_super_ta = 0
    students = Student.objects.filter(course = course, user=request.user)
    for item in students:
        is_ta = item.is_ta
        is_super_ta = item.is_super_ta
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
    
    if(request.user.role=='student' and is_ta == 0):
        role = "Student"
    elif(request.user.role=='student' and is_ta == 1 and is_super_ta == 0):
        role = "Standard TA"
    elif(request.user.role=='student' and is_ta == 1 and is_super_ta == 1):
        role = "Super TA"
    else:
        role = "Instructor"
    return render(request, "core/instructor/view_course.html", {
        'course': course , 
        'is_registered': is_registered,
        'complete' : complete,
        'is_ta': is_ta,
        'is_super_ta': is_super_ta,
        'role': role,
        'student_id': student_id
        })


# REGISTER COURSE
def course_single_register(request, id):
    course = get_object_or_404(Course, id=id)
    if(request.method == 'POST'):
        course_code = request.POST.get("course_code")
        if(str(course.student_code) == str(course_code)):
            new_student = Student(course = course, user = request.user, is_ta = 0, is_super_ta = 0)
            new_student.save() 
            return render(request, "core/instructor/view_course.html", {'course': course})
        elif(str(course.ta_code) == str(course_code)):
            new_student = Student(course = course, user = request.user, is_ta = 1 , is_super_ta = 0)
            new_student.save() 
            return render(request, "core/instructor/view_course.html", {'course': course})
        elif(str(course.super_ta_code) == str(course_code)):
            new_student = Student(course = course, user = request.user, is_ta = 1, is_super_ta = 1)
            new_student.save() 
            return render(request, "core/instructor/view_course.html", {'course': course})
    
    return render(request, "core/instructor/register_course.html", {'course': course})

def get_student_list(id):#returns email id of students having course id 'id'
    course = get_object_or_404(Course, id=id)
    student_list = Student.objects.filter(course=course)
    return student_list

# VIEW REGISTERED STUDENTS IN A COURSE
def view_registered_students(request, id):
    course = get_object_or_404(Course, id=id)
    student_list = Student.objects.filter(course=course)
    return render(request, "core/instructor/registered_students.html", {'course': course, 'student_list': student_list})

#DEREGISTER STUDENT FROM COURSE
def deregister_student(request,id,pk):

    student = Student.objects.filter(pk=pk)
    student.delete()
    return redirect(f"http://127.0.0.1:8000/{id}/course-view/")


# ASSIGNMENT CREATE VIEW
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
        student_list = get_student_list(id)
        for student in student_list:
            #send email through iteration
            email = student.user.email
            name = student.user.first_name
            htmly = get_template('core/instructor/assignment_emails.html')
            d = { 'name': name }
            subject, from_email, to = 'NEW ASSIGNMENT', 'sahilpmahajan@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        return redirect(f"http://127.0.0.1:8000/{id}/assignment")
    return render(request, "core/instructor/assignment_create.html")


# VIEW FOR ASSIGNMENT LIST
def view_assignmentlist(request, id):
        # user = User.objects.get(id=request.user.id)
        course = get_object_or_404(Course, id=id)
        id=id
        assignment_list = Assignment.objects.filter(course = course).order_by('due_date')
        is_ta = 0
        is_super_ta = 0
        students = Student.objects.filter(course = course, user=request.user)
        for item in students:
            is_ta = item.is_ta
            is_super_ta = item.is_super_ta
        if(request.user.role == 'student' and is_ta==0):
            submitted = []
            not_submitted = []
            for assignment in assignment_list:
                    if request.user.assignmentsubmission_set.filter(assignment = assignment):
                        submitted.append(assignment)
                    else:
                        not_submitted.append(assignment)
        
            return render(request, "core/instructor/assignments.html", {'not_submitted': not_submitted , 'id': id, 'submitted': submitted, 'is_ta': is_ta, 'is_super_ta': is_super_ta})
        elif(request.user.role == 'instructor' or is_ta==1):
            return render(request, "core/instructor/assignments.html", {'assignment': assignment_list , 'id': id, 'is_ta': is_ta, 'is_super_ta': is_super_ta})

# # DELETE ASSIGNMENT VIEW
def delete_assignment(request,id):

    assign = Assignment.objects.filter(id=id)
    assign.delete()
    return redirect(f"http://127.0.0.1:8000/course")


#put this instead of your assignment_submit
def assignment_submission_is_valid(due_date):
    now = timezone.localtime(timezone.now())
    if(now <= due_date):  # before submission deadline
        return True
    return False

# ASSIGNMENT SUBMISSION VIEW
def assignment_submit(request, id, pk):
    #user = request.user
    #course = get_object_or_404(Course, id=id)
    assignment = get_object_or_404(Assignment, pk=pk)
    # doubt number 1 : how to get date from assignment
    # doubt number 2 : do we need to add invalid submission in urls.py
    if(assignment_submission_is_valid(assignment.due_date)):
        if(request.method == 'POST'):
            name = request.user.first_name + ' ' + request.user.last_name
            content = request.POST['content']
            file = request.FILES['file']
            ass_sub = AssignmentSubmission.objects.create(
                user=request.user, assignment=assignment, name=name, content=content, file=file)
            ass_sub.save()
            email = request.user.email
            name = request.user.first_name
            htmly = get_template('core/email_submission.html')
            d = { 'name': name }
            subject, from_email, to = 'welcome', 'sahilpmahajan@gmail.com', email
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect("http://127.0.0.1:8000/")
        return render(request, "core/instructor/assignment_submission.html")
    else:
        return redirect("http://127.0.0.1:8000/failed")


def invalid_submission(request):
    return render(request, "core/invalid_submission.html")



def view_assignmentsubmissionlist(request, id, pk):
        # user = User.objects.get(id=request.user.id)
        #course = get_object_or_404(Course, id=id)
        assignment = get_object_or_404(Assignment, pk=pk)
        id=id
        pk=pk
        is_ta = 0
        students = Student.objects.filter(course = assignment.course, user=request.user)
        for item in students:
            is_ta = item.is_ta
        if(request.user.role == 'student' and is_ta == 0):
            assignmentsub_list = AssignmentSubmission.objects.filter(assignment = assignment, user = request.user)
        else:
            assignmentsub_list = AssignmentSubmission.objects.filter(assignment = assignment)
        return render(request, "core/instructor/submitted_assignment.html", {'assignment_submission': assignmentsub_list , 'id': id, 'pk': pk, 'is_ta': is_ta})





# # ASSIGNMENT FEEDBACK VIEW
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
                    if item.user.roll_number == fields[0]:
                        
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
    is_ta = 0
    students = Student.objects.filter(course = assignment.course, user=request.user)
    for item in students:
        is_ta = item.is_ta
    assignmentsub_list = AssignmentSubmission.objects.filter(assignment = assignment)
    if(len(assignmentsub_list)!=0):
        for item in assignmentsub_list:
            labels.append(item.user.roll_number)
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

    if(request.user.role == "instructor" or is_ta ):
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
                    if(len(submissions)!=0):
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
        assignment_list = Assignment.objects.filter().order_by('due_date')
        is_ta = 0
        now = timezone.localtime(timezone.now())
        students = Student.objects.filter(course = assignment_list[0].course, user=request.user)
        for item in students:
            is_ta = item.is_ta
        if(request.user.role == 'student' and is_ta == 0):
            submitted = []
            not_submitted = []
            for assignment in assignment_list:
                is_registered = 0
                for user in assignment.course.student_set.all():
                    if(request.user.email == user.user.email):
                        is_registered = 1
                if(is_registered == 1):
                    if request.user.assignmentsubmission_set.filter(assignment = assignment):
                        submitted.append(assignment)
                    elif(now <= assignment.due_date):
                        not_submitted.append(assignment)
            return render(request, "core/student_todo_list.html", {'not_submitted': not_submitted , 'id': request.user.id, 'submitted': submitted, 'is_ta': is_ta})

        elif(request.user.role == 'instructor' or is_ta == 1):
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

            return render(request, "core/student_todo_list.html", {'ass_sub_list': ass_sub_list, 'is_ta': is_ta})
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

def append_notifs(email, id, pk):
    course = get_object_or_404(Course, id=id)
    discussion = get_object_or_404(Post, pk=pk) #something else
    str_notif = str(discussion.notifs_students) + ';' + str(email) 
    discussion.notifs_students = str_notif
    discussion.save()

def remove_notifs(email, id, pk):
    course = get_object_or_404(Course, id=id)
    discussion = get_object_or_404(Post, pk=pk) #something else
    str_notif = str(discussion.notifs_students) 
    str_notif = str_notif.replace(';'+email, '', 100)
    discussion.notifs_students = str_notif
    discussion.save()

def getnotifs_email(str_notifs):
    l = []
    i = 0
    for j in range(len(str_notifs)):
        if(str_notifs[j]==';'):
            l.append(str_notifs[i:j])
            i=j+1
    l.append(str_notifs[i:])
    l[0]=l[0][4:]
    return l    

def getnotifs(request, id, pk):
    if(request.method == 'POST'):
        value = request.POST['value']
        if((value == 'y' or value == 'yes') or (value == 'YES' or value == 'Yes')):
            email = request.user.email  
            append_notifs(email, id, pk)         
        elif((value == 'n' or value == 'no') or (value == 'NO' or value == 'No')):
            email = request.user.email
            remove_notifs(email,id,pk)
        return redirect(f"http://127.0.0.1:8000/{id}/discussion")
    return render(request, "core/notifs_yesno.html")

@user_is_instructor
def change_course_code(request, id):
    course = get_object_or_404(Course, id=id)
    if(request.method == 'POST'):
        newcode = request.POST["new_code"]
        course.student_code = newcode
        course.save()
        return render(request, "core/instructor/view_course.html", {'course': course})
    return render(request, "core/instructor/change_course_code.html", {'course' : course, 'id' : id})

def comment_create(request, id, pk):
    post = get_object_or_404(Post, pk=pk)
    id = id
    pk = pk
    time = timezone.localtime(timezone.now())
    if(request.method == 'POST'):
            content = request.POST.get('content', False)
            com = Comment.objects.create(
                post = post, user=request.user, content=content, time = time)
            com.save()
            ###############################################
            discussion_name = post.topic
            email_list = getnotifs_email(post.notifs_students)
            for email in email_list:
                htmly = get_template('core/discussion_notif_email.html')
                d = { 'email':email, 'discussion_name': discussion_name }
                subject, from_email, to = 'welcome', 'yashdahiya2002@gmail.com', email
                html_content = htmly.render(d)
                msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            ###############################################
            return redirect(f"http://127.0.0.1:8000/{id}/discussion/{pk}/comments")
    return render(request, "core/create_comment.html", {'id':id, 'pk':pk})

@user_is_instructor
def removefromcourse(request, id):    
    course = get_object_or_404(Course, id=id)
    students = Student.objects.filter(course=course)
    if(request.method == 'POST'):
        roll_number = request.POST['roll_number']
        for e in students:
            if(e.user.roll_number == roll_number):
                e.delete()
                break
        return render(request, "core/instructor/view_course.html", {'course': course})
    return render(request, "core/instructor/email_student_enter.html", {'course' : course, 'id' : id})

@user_is_instructor
def addtocourse(request, id):    
    User = get_user_model()
    users = User.objects.all()
    course = get_object_or_404(Course, id=id)
    if(request.method == 'POST'):
        roll_number = request.POST['roll_number']
        for e in users:
            if(e.roll_number == roll_number and e.role == 'student'):
                new_student = Student(course=course, user = e, is_ta = 0, is_super_ta=0)
                new_student.save()
                break
        return render(request, "core/instructor/view_course.html", {'course': course})
    return render(request, "core/instructor/email_student_enter.html", {'course' : course, 'id' : id})

def get_email_id(id):#returns email id of students having course id 'id'
    course = get_object_or_404(Course, id=id)
    student_list = Student.objects.filter(course=course)
    email_list = []
    for e in student_list:
        email_list.append(e.user.email)
    return email_list

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



############################## AUTOGRADER SCRIPT #########################################

def compile(code):
    try:
        proc = subprocess.run(['g++', '-w', f'{code}', '-o', 'myexec'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=5)
    except subprocess.TimeoutExpired:
        print("compile time exceeded")
        exit(1)
    output = proc.stdout.decode()
    errors = proc.stderr.decode()
    assert output == '', "compilation error"
    assert errors == '', "compilation error"


def run_compiled(input_file, tle):
    copyfile(input_file, 'input.txt')
    out_file = open(f'out.out', 'w+')
    try:
        subprocess.run(['./myexec'], stdout=out_file, stderr=out_file, timeout=tle)
    except subprocess.TimeoutExpired:
        print("Time limit Exceeded")
        exit(1)
    out_file.close()


def diff_checker(output_file):
    out_file = open(f'out.out')
    test_output = out_file.read()
    expected_output = open(f'{output_file}').read()

    test_output = re.sub(r'\s+', ' ', test_output).strip()
    expected_output = re.sub(r'\s+', ' ', expected_output).strip()
    # considers just spaces between everything while comparing

    if test_output == expected_output:
        print("All test passed")
    else:
        print("failed")
    try:
        os.remove('input.txt')
        os.remove('out.out')
        os.remove('myexec')
    except:
        pass


def autograder(request,id,pk):
    if request.method == "POST":
        input_file = request.FILES["input_upload"]
        output_file = request.FILES["output_upload"]
        #code: assignment submission file 
        assignment = get_object_or_404(Assignment, pk=pk)
        assignmentsub_list = AssignmentSubmission.objects.filter(assignment = assignment)
        for item in assignmentsub_list:
            code = item.file.name
        tle = 10
        assert os.path.splitext(code)[1] == '.cpp', 'not a .cpp file'
        assert os.path.isfile(code), 'invalid code path/directory'
        assert os.path.isfile(input_file), 'invalid input path/directory'
        assert os.path.isfile(output_file), 'invalid output path/directory'

        compile(code)
        run_compiled(input_file, tle)
        diff_checker(output_file)
        return redirect(f"http://127.0.0.1:8000/{id}/assignment/{pk}/submitted-assignment")

    form = AutograderImportForm()
    data = {"form": form}
    return render(request, "core/autograder_upload.html", data)

