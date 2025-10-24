from django.urls import path
from core import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Students
    path('students/', views.student_list, name='students'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:id>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:id>/', views.student_delete, name='student_delete'),

    # Teachers
    path('teachers/', views.teacher_list, name='teachers'),
    path('teachers/add/', views.teacher_add, name='teacher_add'),
    path('teachers/edit/<int:id>/', views.teacher_edit, name='teacher_edit'),
    path('teachers/delete/<int:id>/', views.teacher_delete, name='teacher_delete'),

    # Courses
    path('courses/', views.course_list, name='courses'),
    path('courses/add/', views.course_add, name='course_add'),
    path('courses/edit/<int:id>/', views.course_edit, name='course_edit'),
    path('courses/delete/<int:id>/', views.course_delete, name='course_delete'),

    # Exams
    path('exams/', views.exam_list, name='exams'),
    path('exams/add/', views.exam_add, name='exam_add'),
    path('exams/edit/<int:id>/', views.exam_edit, name='exam_edit'),
    path('exams/delete/<int:id>/', views.exam_delete, name='exam_delete'),

    # Attendance
    path('attendance/', views.attendance_list, name='attendance'),
    path('attendance/add/', views.attendance_add, name='attendance_add'),
    path('attendance/edit/<int:id>/', views.attendance_edit, name='attendance_edit'),
    path('attendance/delete/<int:id>/', views.attendance_delete, name='attendance_delete'),

    # Marks
    path('marks/', views.marks_list, name='marks'),
    path('marks/add/', views.marks_add, name='marks_add'),
    path('marks/edit/<int:id>/', views.marks_edit, name='marks_edit'),
    path('marks/delete/<int:id>/', views.marks_delete, name='marks_delete'),
]
