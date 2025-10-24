from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import (LoginForm, StudentForm, TeacherForm, CourseForm,
                        ExamForm, MarksForm, AttendanceForm)
from core.models import CustomUser, Student, Teacher, Course, Exam, Marks, Attendance

# -------- Authentication --------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
        else:
            messages.error(request, 'Form validation failed.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# -------- Dashboard --------
@login_required
def dashboard(request):
    role = request.user.role
    if role == 'admin':
        context = {
            'students_count': Student.objects.count(),
            'teachers_count': Teacher.objects.count(),
            'courses_count': Course.objects.count(),
            'exams_count': Exam.objects.count()
        }
        return render(request, 'core/admin_dashboard.html', context)
    elif role == 'teacher':
        teacher = get_object_or_404(Teacher, user=request.user)
        attendance = Attendance.objects.filter(course__in=teacher.courses.all())
        marks = Marks.objects.filter(exam__course__in=teacher.courses.all())
        return render(request, 'core/teacher_dashboard.html', {'attendance': attendance, 'marks': marks})
    elif role == 'parent':
        student = get_object_or_404(Student, user=request.user)
        marks = Marks.objects.filter(student=student)
        attendance_records = Attendance.objects.filter(student=student)
        present_count = attendance_records.filter(status=True).count()
        absent_count = attendance_records.filter(status=False).count()
        return render(request, 'core/parent_dashboard.html', {
            'student': student,
            'marks': marks,
            'present_count': present_count,
            'absent_count': absent_count
        })
    else:
        messages.error(request, 'Role not recognized.')
        return redirect('login')

# -------- CRUD Helpers --------
def role_check(user, allowed_roles):
    return user.role in allowed_roles

# -------- Students CRUD --------
@login_required
def student_list(request):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    students = Student.objects.all()
    return render(request, 'core/students.html', {'students': students})

@login_required
def student_add(request):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully.')
            return redirect('students')
    else:
        form = StudentForm()
    return render(request, 'core/student_form.html', {'form': form, 'form_title': 'Add Student'})

@login_required
def student_edit(request, id):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('students')
    else:
        form = StudentForm(instance=student)
    return render(request, 'core/student_form.html', {'form': form, 'form_title': 'Edit Student'})

@login_required
def student_delete(request, id):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, 'Student deleted successfully.')
    return redirect('students')

# -------- Teachers CRUD --------
@login_required
def teacher_list(request):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    teachers = Teacher.objects.all()
    return render(request, 'core/teachers.html', {'teachers': teachers})

@login_required
def teacher_add(request):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully.')
            return redirect('teachers')
    else:
        form = TeacherForm()
    return render(request, 'core/teacher_form.html', {'form': form, 'form_title': 'Add Teacher'})

@login_required
def teacher_edit(request, id):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher updated successfully.')
            return redirect('teachers')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'core/teacher_form.html', {'form': form, 'form_title': 'Edit Teacher'})

@login_required
def teacher_delete(request, id):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    teacher = get_object_or_404(Teacher, id=id)
    teacher.delete()
    messages.success(request, 'Teacher deleted successfully.')
    return redirect('teachers')

# -------- Courses CRUD --------
@login_required
def course_list(request):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    courses = Course.objects.all()
    return render(request, 'core/courses.html', {'courses': courses})

@login_required
def course_add(request):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully.')
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'core/course_form.html', {'form': form, 'form_title': 'Add Course'})

@login_required
def course_edit(request, id):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'core/course_form.html', {'form': form, 'form_title': 'Edit Course'})

@login_required
def course_delete(request, id):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    course = get_object_or_404(Course, id=id)
    course.delete()
    messages.success(request, 'Course deleted successfully.')
    return redirect('courses')

# -------- Exams CRUD --------
@login_required
def exam_list(request):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    exams = Exam.objects.all()
    return render(request, 'core/exams.html', {'exams': exams})

@login_required
def exam_add(request):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam added successfully.')
            return redirect('exams')
    else:
        form = ExamForm()
    return render(request, 'core/exam_form.html', {'form': form, 'form_title': 'Add Exam'})

@login_required
def exam_edit(request, id):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    exam = get_object_or_404(Exam, id=id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam updated successfully.')
            return redirect('exams')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'core/exam_form.html', {'form': form, 'form_title': 'Edit Exam'})

@login_required
def exam_delete(request, id):
    if not role_check(request.user, ['admin']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    exam = get_object_or_404(Exam, id=id)
    exam.delete()
    messages.success(request, 'Exam deleted successfully.')
    return redirect('exams')

# -------- Attendance CRUD (Teacher) --------
@login_required
def attendance_list(request):
    if not role_check(request.user, ['teacher']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    teacher = get_object_or_404(Teacher, user=request.user)
    attendance = Attendance.objects.filter(course__in=teacher.courses.all())
    return render(request, 'core/attendance.html', {'attendance': attendance})

@login_required
def attendance_add(request):
    if not role_check(request.user, ['teacher']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance added successfully.')
            return redirect('attendance')
    else:
        form = AttendanceForm()
    return render(request, 'core/attendance_form.html', {'form': form, 'form_title': 'Add Attendance'})

@login_required
def attendance_edit(request, id):
    if not role_check(request.user, ['teacher']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    attendance = get_object_or_404(Attendance, id=id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance updated successfully.')
            return redirect('attendance')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'core/attendance_form.html', {'form': form, 'form_title': 'Edit Attendance'})

@login_required
def attendance_delete(request, id):
    if not role_check(request.user, ['teacher']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    attendance = get_object_or_404(Attendance, id=id)
    attendance.delete()
    messages.success(request, 'Attendance deleted successfully.')
    return redirect('attendance')

# -------- Marks CRUD (Teacher) --------
@login_required
def marks_list(request):
    if not role_check(request.user, ['teacher']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    teacher = get_object_or_404(Teacher, user=request.user)
    marks = Marks.objects.filter(exam__course__in=teacher.courses.all())
    return render(request, 'core/marks.html', {'marks': marks})

@login_required
def marks_add(request):
    if not role_check(request.user, ['teacher']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marks added successfully.')
            return redirect('marks')
    else:
        form = MarksForm()
    return render(request, 'core/marks_form.html', {'form': form, 'form_title': 'Add Marks'})

@login_required
def marks_edit(request, id):
    if not role_check(request.user, ['teacher']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    mark = get_object_or_404(Marks, id=id)
    if request.method == 'POST':
        form = MarksForm(request.POST, instance=mark)
        if form.is_valid():
            form.save()
            messages.success(request, 'Marks updated successfully.')
            return redirect('marks')
    else:
        form = MarksForm(instance=mark)
    return render(request, 'core/marks_form.html', {'form': form, 'form_title': 'Edit Marks'})

@login_required
def marks_delete(request, id):
    if not role_check(request.user, ['teacher']):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    mark = get_object_or_404(Marks, id=id)
    mark.delete()
    messages.success(request, 'Marks deleted successfully.')
    return redirect('marks')
