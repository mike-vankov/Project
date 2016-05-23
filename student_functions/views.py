# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template.context_processors import csrf

from academic_plan.models import AcademicPlan
from course_work.models import CourseWork
from forms import CourseWorkAddForm
# Create your views here.
def is_student(user):
	if hasattr(user, 'person'):
		user = user.person
		if hasattr(user, 'student'):
			return True
	return False

@user_passes_test(is_student)
def show_student_page(request):
	return redirect(settings.LOGIN_REDIRECT_URL)

@user_passes_test(is_student)
def show_my_courseworks(request):
	student = auth.get_user(request).person.student

	param = student.studentgroup.academicplan.get_current_courseworks()

	if param['current_semester'] is not None:
		page = 'my_courseworks.html'
		args = {
			'username' : student.name,
			'studentgroup' : student.studentgroup,
			'semester' : param['current_semester'],
			'subjects' : param['subjects'],
		}
	else:
		page = 'fail_student.html'
		args = {
			'username' : student.name,
			'studentgroup' : student.studentgroup,
		}

	return render_to_response(page, args)

@user_passes_test(is_student)
def show_coursework(request, subject_id, course_id, semester_id):
	student = auth.get_user(request).person.student
	semester = student.studentgroup.academicplan.get_current_semester()

	if student.studentgroup.academicplan.exists_coursework2(subject_id, course_id, semester_id):
		cw = student.studentgroup.academicplan.get_coursework_task(subject_id, course_id, semester_id)

		page = 'show_coursework.html'
		args = {
			'username' : student.name,
			'studentgroup' : student.studentgroup,
			'semester' : semester,
			'subject_title' : cw['subject_title'],
			'coursework_task' : cw['taskcoursework'],
			'teacher' : cw['teacher'],
			'subject_id' : subject_id,
			'course_id' : course_id, 
			'semester_id' : semester_id,
		}
		args.update(csrf(request))
		return render_to_response(page, args)
	else:
		return redirect('/')

@user_passes_test(is_student)
def show_coursework_rep(request, subject_id, course_id, semester_id, task_id):
	student = auth.get_user(request).person.student
	semester = student.studentgroup.academicplan.get_current_semester()

	if student.studentgroup.academicplan.exists_coursework2(subject_id, course_id, semester_id):
		if student.studentgroup.academicplan.exists_coursework_task(subject_id, course_id, semester_id, task_id):
			cw = student.studentgroup.academicplan.get_coursework_task(subject_id, course_id, semester_id)

			commits = CourseWork.objects.getCommitsByUserAndTask(student, cw['taskcoursework'])

			page = 'show_coursework_rep.html'
			args = {
				'username' : student.name,
				'studentgroup' : student.studentgroup,
				'semester' : semester,
				'subject_title' : cw['subject_title'],
				'coursework_task' : cw['taskcoursework'],
				'subject_id' : subject_id,
				'course_id' : course_id, 
				'semester_id' : semester_id,
				'task_id' : task_id,
				'commits' : commits,
			}
			args.update(csrf(request))
			return render_to_response(page, args)

	return redirect('/')

@user_passes_test(is_student)
def show_add_coursework_rep(request, subject_id, course_id, semester_id, task_id):
	if request.POST:
		student = auth.get_user(request).person.student
		semester = student.studentgroup.academicplan.get_current_semester()

		if student.studentgroup.academicplan.exists_coursework2(subject_id, course_id, semester_id):
			if student.studentgroup.academicplan.exists_coursework_task(subject_id, course_id, semester_id, task_id):
				subject_title = student.studentgroup.academicplan.get_subject_title(subject_id)

				page = 'show_add_coursework_rep.html'
				args = {
					'username' : student.name,
					'studentgroup' : student.studentgroup,
					'semester' : semester,
					'subject_id' : subject_id,
					'subject_title' : subject_title,
					'course_id' : course_id, 
					'semester_id' : semester_id,
					'task_id' : task_id,
					'form' : CourseWorkAddForm(),
				}
				args.update(csrf(request))
				return render_to_response(page, args)
	
	return redirect('/')

@user_passes_test(is_student)
def add_coursework_rep(request, subject_id, course_id, semester_id, task_id):
	if request.POST:
		form = CourseWorkAddForm(request.POST)
		if form.is_valid():
			student = auth.get_user(request).person.student

			if student.studentgroup.academicplan.exists_coursework2(subject_id, course_id, semester_id):
				if student.studentgroup.academicplan.exists_coursework_task(subject_id, course_id, semester_id, task_id):
					
					cwt = student.studentgroup.academicplan.get_coursework_task2(semester_id)
					cw = CourseWork.objects.getByUserAndTask(student, cwt)

					courseworkcommit = form.save(commit = False)

					if not cw:
						cw = CourseWork(taskcoursework=cwt, student=student)
						cw.save()

					courseworkcommit.coursework = cw
					courseworkcommit.save()
					cw.save()

	return redirect('/student/mycourseworks/%s/%s/%s/%s/' % (subject_id, course_id, semester_id, task_id))