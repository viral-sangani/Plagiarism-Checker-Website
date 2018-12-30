from django.urls import include, path
from . import views

urlpatterns = [
    path('',views.studnt_login, name = 'student_login'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('add_assignment/', views.add_assignment, name= 'add_assignment'),

    path('signup/', views.signup_student, name ='signup_student'),

    path('home/', views.home, name = 'student_home'),

    path('about/',views.about, name='about'),

    path('profile/<slug:s_username>', views.profile, name='profile'),

    path('assignment/<int:id>',views.assignment, name='write_assignment'),
    
    path('summary/', views.assignment_summary, name= 'assignment_summary'),

    path('list/' , views.ass_list, name = 'ass_list'),
]
