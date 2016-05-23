# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from cwcs.models import Student, Teacher, Person

# Create your views here.
def is_member(user):
	if hasattr(user, 'person'):
		user = user.person
		if hasattr(user, 'student'):
			return True
		elif hasattr(user, 'teacher'):
			return True

	return False

@login_required
def showmainpage(request):
	obj = auth.get_user(request)
	name = obj.username
	page = 'main_page.html'
	args = {}

	if hasattr(obj, 'person'):
		obj = obj.person
		if hasattr(obj, 'student'):
			name = obj.student.name
			page = 'main_page_student.html'
			args = {
				'username' : name,
				'studentgroup' : obj.student.studentgroup,
			}

		elif hasattr(obj, 'teacher'):
			name = obj.teacher.name
			page = 'main_page_teacher.html'
			args = {
				'username' : name,
			}

	return render_to_response(page, args)
		
def login(request):
	if request.user.is_authenticated():
		return redirect('/')

	args = {}
	args.update(csrf(request))
	loginpage = 'login.html'

	if request.POST:
		username = request.POST.get('login', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				if is_member(user):
					auth.login(request, user)

					if not request.POST.has_key('remember'):               
						settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
					else:
						settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

					return redirect(settings.LOGIN_REDIRECT_URL)
				else:
					args['login_error'] = "Вы не являетесь студентом или преподавателем!"
			else:
				args['login_error'] = "Аккаунт выключен!"
		else:
			args['login_error'] = "Указан неверный логин или пароль!"
			
	return render_to_response(loginpage, args)

def logout(request):
	auth.logout(request)
	return redirect(settings.LOGOUT_REDIRECT_URL)