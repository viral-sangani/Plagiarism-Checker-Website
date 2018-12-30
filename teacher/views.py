from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from webpages.forms import student_signup
from webpages.models import Profile
from django.http import *
from django.template import RequestContext
from .models import assignments_by_teacher, teacher_in_class
from webpages.models import assignment_submitted, Profile, assignment_submitted, assignment_by_student
import datetime
from django.contrib.auth.decorators import login_required


username = password = ''

def login_teacher(request):

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
				return HttpResponseRedirect('/teacher/teacher_home')

	return render(request,'webpages/teacher_login.html')


# @login_required(login_url='/login/')
@login_required(login_url="/teacher/login/")
def teacher_home(request):
	ass_submitted_list = []
	ass_list = []
	if request.method == 'GET':
		current_user = request.session['username']
		print('Done')
		t_class_obj= assignments_by_teacher.objects.filter(teacher_name=current_user)
		for title in t_class_obj:
			ass_list.append(title)
			submitted_obj = assignment_submitted.objects.filter(ass_title=title.ass_title).order_by('ass_title')
			for obj in submitted_obj:
				ass_submitted_list.append(obj)

		print(ass_list)

		context = {
			'ass_submitted_list': ass_submitted_list,
			'ass_list':ass_list,
		}

	return render(request, 'webpages/teacher_home.html', context)
@login_required(login_url="/teacher/login/")
def add(request):

	if request.POST:
		now = datetime.datetime.now()
		ass_obj = assignments_by_teacher()
		ass_obj.teacher_name = request.session['username']
		ass_obj.ass_title = request.POST['title']
		ass_obj.ass_body = request.POST['body']
		ass_obj.ass_sub_date = request.POST['submission_date']
		ass_obj.ass_given_date = now.strftime("%Y-%m-%d")
		ass_obj.ass_extra = request.POST['extra']
		ass_obj.save()

	context = {
		'username' : username,
		}
	return render(request, 'webpages/teacher_ass_form.html', context)

@login_required(login_url="/teacher/login/")
def view(request, id):
	content = ""
	ass_submit_list = []
	ass_submit_obj = assignment_submitted.objects.filter(pk=id)
	for obj in ass_submit_obj:
		s_fullname = obj.s_name
		ass_title = obj.ass_title
		submit_date = obj.submit_date
		plag_ratio = obj.plag_ratio


		ass_content = assignment_by_student.objects.filter(user = s_fullname, ass_title = ass_title)

		for content_info in ass_content:
			content = content_info.content

	context = {
		's_name': s_fullname,
		'ass_title':ass_title,
		'submit_date':submit_date,
		'plag_ratio':plag_ratio,
		'content':content,
	}


	return render(request, 'webpages/view_ass.html', context)