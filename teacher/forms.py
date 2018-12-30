from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class teacher(UserCreationForm):
	fullname = forms.CharField()
	email = forms.CharField()
	subject = forms.CharField()
	
	class Meta:
		model = User
		fields = ('username','fullname','email','subject', 	'password1','password2',)