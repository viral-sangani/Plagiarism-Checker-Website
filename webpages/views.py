from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, assignment_by_student, assignment_submitted, assignment_save
from teacher.models import teacher_in_class, assignments_by_teacher
from .forms import assignment_field, student_signup, add_assignment
from django.views.generic import TemplateView
from .plagiarism import init
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import datetime


def studnt_login(request):
	context = []
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		request.session['username'] = username
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if request.GET.get('next', None):
					return HttpResponseRedirect(request.GET['next'])
				return HttpResponseRedirect('/home')

		else:
			content = {
			'error': "Provide Valid Credentials !!"
			}
			return render(request, "registration/login.html",content)

	return render(request,'registration/login.html')

def signup_student(request):
	if request.method == 'POST':
		form = student_signup(request.POST)
		if form.is_valid():
			user = form.save()

			user.refresh_from_db()

			user.profile.s_fullname = form.cleaned_data.get('s_fullname')
			user.profile.s_email = form.cleaned_data.get('s_email')
			user.profile.s_class = form.cleaned_data.get('s_class')
			user.profile.s_rollno = form.cleaned_data.get('s_rollno')
			user.save()

			for user in User.objects.all():
				Profile.objects.get_or_create(user=user)

			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')

			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/home')

	else:
		form = student_signup()
	return render(request, 'webpages/signup_student.html',{'form' : form})
	

@login_required(login_url="/")
def home(request):
	teacher_list = []
	assignment_list = []
	ass_obj_list = []
	username = request.user.get_username()
	user_obj = Profile.objects.filter(user__username=username)
	
	for obj in user_obj:
		s_fullname = obj.s_fullname
		student_class = obj.s_class

		teacher_class_obj = teacher_in_class.objects.filter(class_name__exact=student_class)

	for obj in teacher_class_obj:
		teacher_list.append(obj.teacher_name)

	for teacher in teacher_list:
		assignment_obj = assignments_by_teacher.objects.filter(teacher_name__exact=teacher)
		# ass_obj_list.append(assignment_obj)
		for obj in assignment_obj:
			if (assignment_submitted.objects.filter(s_name = s_fullname, ass_title = obj.ass_title).exists()):
				pass
			else:
				ass_obj_list.append(obj)

	content = {
		'teacher_list':teacher_list,
		'ass_obj_list':ass_obj_list,
		'username':request.user.get_username(),
		'fullname': s_fullname,
		'today':datetime.date.today(),
		 }

	return render(request,'webpages/home.html', content)

@login_required(login_url="/")
def about(request):
	username = request.user.get_username()
	user_obj = Profile.objects.filter(user__username=username)

	for obj in user_obj:
		s_fullname = obj.s_fullname

	content = {
		'fullname':s_fullname,
	}
	return render(request,'webpages/about.html', content)

@login_required(login_url="/")
def profile(request, s_username):
	user_obj = Profile.objects.filter(user__username=s_username)
	for obj in user_obj:
		s_fullname = obj.s_fullname
		s_rollno = obj.s_rollno
		s_class = obj.s_class
		s_email = obj.s_email
		s_bio = obj.s_bio

	content = {
		's_username':s_username,
		's_fullname':s_fullname,
		's_rollno':s_rollno,
		's_class':s_class,
		's_email':s_email,
		's_bio': s_bio,
	}
	return render(request,'webpages/profile.html', content)

@login_required(login_url="/")
def assignment_summary(request):
	teacher_list = []
	assignment_list = []
	ass_submitted_obj_list = []
	ass_submitted_ratio_obj_list = []
	ass_saved_obj_list  =[]
	username = request.user.get_username()
	user_obj = Profile.objects.filter(user__username=username)


	for obj in user_obj:
		s_fullname = obj.s_fullname
		student_class = obj.s_class

		teacher_class_obj = teacher_in_class.objects.filter(class_name__exact=student_class)

	for obj in teacher_class_obj:
		teacher_list.append(obj.teacher_name)

	for teacher in teacher_list:
		assignment_obj = assignments_by_teacher.objects.filter(teacher_name__exact=teacher)
		for obj in assignment_obj:
			temp_obj = assignment_save.objects.filter(s_name = s_fullname, ass_title = obj.ass_title)
			for temp in temp_obj:
				if(obj.ass_title == temp.ass_title):
					ass_saved_obj_list.append(obj)		

	for teacher in teacher_list:
		assignment_obj = assignments_by_teacher.objects.filter(teacher_name__exact=teacher)
		for obj in assignment_obj:
			if (assignment_submitted.objects.filter(s_name = s_fullname, ass_title = obj.ass_title)):
				ratio_objs = assignment_submitted.objects.filter(s_name = s_fullname, ass_title = obj.ass_title)
				for ratio_obj in ratio_objs:
					ass_submitted_ratio_obj_list.append(ratio_obj)
				ass_submitted_obj_list.append(obj)	

	content = {
		'teacher_list':teacher_list,
		'ass_submitted_obj_list':ass_submitted_obj_list,
		'username':request.user.get_username(),
		'fullname': s_fullname,
		'ass_saved_obj_list':ass_saved_obj_list,
		'ass_submitted_ratio_obj_list':ass_submitted_ratio_obj_list,
		'today':datetime.date.today(),
		 }
	
	return render(request, 'webpages/assignment_list.html', content)


@login_required(login_url="/")
def assignment(request, id):
	s_class_obj = Profile.objects.filter(user__username=request.user.get_username())
	for c_obj in s_class_obj:
		s_fullname = c_obj.s_fullname
	if request.method == "POST":
		context = {
		'form': assignment_field()
		}
		if 'save' in request.POST:
			obj = assignments_by_teacher.objects.filter(pk=id)
			for o in obj:
				o_title = o.ass_title
				
			if (assignment_save.objects.filter(ass_title=o_title, s_name = s_fullname)):
				assignment_save.objects.filter(ass_title=o_title, s_name = s_fullname).update(content = request.POST['content'])
				print(request.POST['content'])
				return HttpResponseRedirect('/summary')

			else:
				save_object = assignment_save()
				save_object.s_name = s_fullname
				save_object.ass_title = o_title
				save_object.content = request.POST['content']
				save_object.save()

				return HttpResponseRedirect('/summary')

		if 'submit' in request.POST:
			form = assignment_by_student()			

			form.content = request.POST['content']
			form.user = s_fullname
			form.ass_title = request.POST['post_title']
			print(form.user)
			form.save()

			if(assignment_save.objects.filter(s_name = s_fullname, ass_title = request.POST['post_title'])):
				assignment_save.objects.filter(s_name = s_fullname, ass_title = request.POST['post_title']).delete()


			obj = assignments_by_teacher.objects.filter(pk=id)

			for o in obj:
				title = o.ass_title

			assignment_list = assignment_by_student.objects.filter(ass_title = request.POST['post_title'])
			last_assignment = assignment_by_student.objects.last()
			init(assignment_list,last_assignment, request.user.get_username() , title)

			return HttpResponseRedirect('/summary')

	else:
		init_content = ""
		obj = assignments_by_teacher.objects.filter(pk=id)
		for o in obj:
			o_title = o.ass_title
		if (assignment_save.objects.filter(ass_title=o_title, s_name = s_fullname).exists()):
			content_obj = assignment_save.objects.filter(ass_title=o_title, s_name = s_fullname)
			for obj in content_obj:
				init_content = obj.content

		form = assignment_field(initial={'content':init_content})
		user = request.user.get_username()
		obj = assignments_by_teacher.objects.filter(pk=id)
		context = {
			'form':form,
			'obj':obj,
			'user':user
				}

		return render(request,'webpages/write_ass.html',context)

@login_required(login_url="/")
def ass_list(request):
	teacher_list = []
	assignment_list = []
	ass_obj_list = []
	username = request.user.get_username()
	user_obj = Profile.objects.filter(user__username=username)
	
	for obj in user_obj:
		s_fullname = obj.s_fullname
		student_class = obj.s_class

		teacher_class_obj = teacher_in_class.objects.filter(class_name__exact=student_class)

	for obj in teacher_class_obj:
		teacher_list.append(obj.teacher_name)

	for teacher in teacher_list:
		assignment_obj = assignments_by_teacher.objects.filter(teacher_name__exact=teacher)
		for obj in assignment_obj:
			if (assignment_submitted.objects.filter(s_name = s_fullname, ass_title = obj.ass_title).exists()):
				pass
			else:
				ass_obj_list.append(obj)


	content = {
		'teacher_list':teacher_list,
		'ass_obj_list':ass_obj_list,
		'username':request.user.get_username(),
		'fullname': s_fullname,
		'today':datetime.date.today(),
		 }

	return render(request,'webpages/all_assignment.html', content)
