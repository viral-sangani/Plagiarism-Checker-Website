from django.urls import include, path
from . import views
from django.contrib import admin

urlpatterns = [
    path('teacher_home/',views.teacher_home, name='teacher_home'),
    path('login/', views.login_teacher, name = 'teacher_login'),
    path('view_assignment/<int:id>', views.view, name = 'view_assignment'),
    path('add_assignment/', views.add, name = 'add_assignment'),

]
