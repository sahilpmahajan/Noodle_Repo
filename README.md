# Noodle_Repo
Github repository for CS251 Project, by:
Team Noodle:
Avi Uday
Sahil Mahajan
Shubham Bakare
Yash Singh 

Project Description:
Assignment Submission and Evaluation system, CodeName- Float Moodle
Frameworks used:
Django:
	AddOns:
Django_Rest_Framework (Used for Chat facility)
Widget_Tweaks
Crispy_Forms
Bootstrap4
Bootstrapform
For Styling:
CSS
JavaScript
Database used:
Sqlite

User Roles:
Instructor:
	Can create course, assignment, discussion, grade assignments, add specific students to course, deregister students/TAs, disable chat facility during exams

Student:
	Depending on course, Student can have sub-roles:
	Course Taking Student:
		Can submit assignments and see the feedback given
	Normal TA:
		Can grade assignment submissions
	Super TA:
		Can grade assignment submissions as well as create assignments

Features:

Registration Email
After registration, the registered email gets a confirmation link, and the account can be activated only after visiting that link (To ensure one can only register with his/her mail). 

Course Registration:
During creation of course, instructor will create 3 separate registration codes, 1 each for Course Taking student, Normal TA and Super TA, which instructor may communicate to students after which they may register to the course, thus instructor has the power to register a TA and also control the power of TA

Forgot Password:
Incase user forgets his password, he/she can click on this button and they will be sent a link on their registered email clicking which they can put the new credentials

Assignments:
Whenever the instructor/Super TA creates a new assignment, every student registered in the course gets an email to let him know that a new assignment is added. 
When the student submits any assignment, he gets an email that he has submitted the assignment. 

Course/Assignment Statistics:
Once the submissions are graded, student can see average of the assignment and his standing, and will be warned upon low score
Teacher can see Assignment/Course statistics, which includes facility of giving weights to Assignments
Student can see how much course is completed based on number of assignments he submitted in the form of a progress bar, also his total marks obtained for a course

Chat /Discussion Forums Facility:.
Instructor can create discussion on some topic and students can comment on it.
Students can decide if they want to receive E-mail notifications of every new comment on the discussion forum.
Chat feature for private messaging between users of the website.
Chat can be disabled by the instructor in the event of an exam.

Deadlines/To-Do lists
Assignments can be submitted only before deadline, and all assignments to be submitted will be visible in a To-Do list to the student, All assignment submissions to be graded will be visible in the To-Do list to the instructor


