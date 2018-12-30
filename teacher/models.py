from django.db import models
from django.contrib.auth.models import User

class teacher_subject(models.Model):
	user_name = models.CharField(max_length=200)
	subject = models.CharField(max_length=100)

	def __str__(self):
		return self.user_name + ' - ' + str(self.subject)

class teacher_in_class(models.Model):
	teacher_name = models.CharField(max_length=1000)
	class_name = models.CharField(max_length=500)

	def __str__(self):
		return self.class_name + ' - ' + self.teacher_name

class assignments_by_teacher(models.Model):
	teacher_name = models.CharField(max_length=200)
	ass_title = models.CharField(max_length=10000)
	ass_body = models.CharField(max_length=50000)
	ass_sub_date = models.DateField()
	ass_given_date = models.DateField()
	ass_extra = models.CharField(max_length=50000)

	def __str__(self):
		return str(self.ass_given_date) + ' - ' + str(self.teacher_name) + ' - ' + self.ass_title

class assignment_and_class(models.Model):
	ass_title = models.CharField(max_length=10000)
	ass_class = models.CharField(max_length=200)

	def __str__(self):	
		return self.ass_class



