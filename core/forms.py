from django import forms
from django.contrib.auth.forms import AuthenticationForm
from core.models import CustomUser, Student, Teacher, Course, Exam, Marks, Attendance
from django.core.validators import RegexValidator

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        validators=[RegexValidator(r'^[\w.@+-]+$', 'Enter a valid username.')]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        min_length=6
    )

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'roll_number', 'courses']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'courses']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'course', 'date']

class MarksForm(forms.ModelForm):
    class Meta:
        model = Marks
        fields = ['student', 'exam', 'marks_obtained']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status']
