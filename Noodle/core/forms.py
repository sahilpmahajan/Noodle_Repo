from django import forms
from .models import *


# FORM FOR CREATE A COURSE
class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'teacher_name', 'teacher_details', 'course_description', 'end_date']

    def __init__(self, *args, **kwargs):
        super(CourseCreateForm, self).__init__(*args, **kwargs)
        self.fields['course_name'].label = "Course Name"
        #self.fields['course_image'].label = "Image"
        self.fields['teacher_name'].label = "Teacher Name"
        self.fields['teacher_details'].label = "Teacher Details"
        self.fields['course_description'].label = "Description"
        self.fields['end_date'].label = "End Date"

        self.fields['course_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Course Name',
            }
        )

        # self.fields['course_image'].widget.attrs.update(
        #     {
        #         'placeholder': 'Image',
        #     }
        # )

        self.fields['teacher_name'].widget.attrs.update(
            {
                'placeholder': 'Teacher Name',
            }
        )

        self.fields['teacher_details'].widget.attrs.update(
            {
                'placeholder': 'Teacher Details',
            }
        )

        self.fields['course_description'].widget.attrs.update(
            {
                'placeholder': 'Description',
            }
        )

    def is_valid(self):
        valid = super(CourseCreateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(CourseCreateForm, self).save(commit=False)
        if commit:
            course.save()
        return course



# ASSIGNMENT CREATE FORM
class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'content', 'marks', 'duration']

    def __init__(self, *args, **kwargs):
        super(AssignmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Assignment Name"
        self.fields['content'].label = "Content"
        self.fields['marks'].label = "Marks"
        self.fields['duration'].label = "Duration"

        self.fields['title'].widget.attrs.update(
            {
                'placeholder': 'Enter A Name',
            }
        )

        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Content',
            }
        )

        self.fields['marks'].widget.attrs.update(
            {
                'placeholder': 'Enter Marks',
            }
        )

        self.fields['duration'].widget.attrs.update(
            {
                'placeholder': '3 hour, 2 hour etc ...',
            }
        )

    def is_valid(self):
        valid = super(AssignmentCreateForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(AssignmentCreateForm, self).save(commit=False)
        if commit:
            course.save()
        return course

# ASSIGNMENT SUBMISSION FORM

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['name', 'university_id', 'content', 'file']

    def __init__(self, *args, **kwargs):
        super(AssignmentSubmissionForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = " Name"
        self.fields['university_id'].label = "University Id"
        self.fields['content'].label = "Answer"
        self.fields['file'].label = "Or Upload File"

        self.fields['name'].widget.attrs.update(
            {
                'placeholder': 'Write Your Name',
            }
        )

        self.fields['university_id'].widget.attrs.update(
            {
                'placeholder': 'Write Your Id',
            }
        )

        self.fields['content'].widget.attrs.update(
            {
                'placeholder': 'Write Your Answer Here',
            }
        )

        self.fields['file'].widget.attrs.update(
            {
                'placeholder': 'Upload Your FILE Here',
            }
        )

    def is_valid(self):
        valid = super(AssignmentSubmissionForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        course = super(AssignmentSubmissionForm, self).save(commit=False)
        if commit:
            course.save()
        return course


