from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
	user =  models.OneToOneField(User, on_delete=models.CASCADE)
	s_fullname = models.CharField(max_length=200)
	s_email = models.CharField(max_length=200)
	s_rollno = models.IntegerField(blank=False, null=True)
	s_class = models.CharField(max_length=200,blank=True, null=True)
	s_bio = models.CharField(max_length=200,blank=True, null=True, default='No Bio')

	def __str__(self):
		return str(self.s_fullname) + ' - ' + str(self.s_rollno) + ' - ' + str(self.s_class)

@receiver(post_save, sender=User)

def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)	
    instance.profile.save()


class assignment_by_student(models.Model):
	user = models.CharField(max_length=200, default='User0')
	content = models.CharField(max_length=20000, default='User0')
	ass_title = models.CharField(max_length=1000,  default='ass. 0')

	def __str__(self):
		return self.user +' - '+ self.ass_title


class assignment_submitted(models.Model):
	s_name = models.CharField(max_length=200)
	ass_title = models.CharField(max_length=1000)
	submit_date = models.DateField()
	plag_ratio = models.IntegerField(default=0)
	s_class = models.CharField(max_length=50,default='None')

	def __str__(self):
		return self.s_name + ' - ' + str(self.plag_ratio)

class assignment_save(models.Model):
	s_name = models.CharField(max_length=200)
	ass_title = models.CharField(max_length=1000)
	content = models.CharField(max_length=20000, default='')

	def __str__(self):
		return self.s_name + ' - ' +  self.ass_title

