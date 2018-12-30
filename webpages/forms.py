from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import assignment_by_student
from teacher.models import assignments_by_teacher
from tinymce.widgets import TinyMCE
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'User name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class student_signup(UserCreationForm):
	s_fullname = forms.CharField()
	s_email = forms.CharField()
	s_class = forms.CharField()
	s_rollno = forms.CharField()
	
	class Meta:
		model = User
		fields = ('username','s_fullname','s_email','s_class','s_rollno','password1','password2',)

class add_assignment(forms.ModelForm):
	teacher_name = forms.CharField()
	ass_title = forms.CharField()
	ass_body = forms.CharField()
	ass_date = forms.DateField()
	ass_sub_date = forms.DateField()
	extra_note = forms.CharField()

	class Meta:
		model = assignments_by_teacher
		fields= ('teacher_name','ass_title','ass_body','ass_date','ass_sub_date','extra_note',)

class assignment_field(forms.ModelForm):
	user = forms.CharField(
		widget = forms.TextInput(
            attrs = {'type':'hidden','class': 'summernote'}
        ))
	content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

	class Meta:
		model = assignment_by_student
		fields = ('content','user',)
