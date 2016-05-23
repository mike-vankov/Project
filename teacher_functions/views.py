# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect

from django.template.context_processors import csrf

from academic_plan.models import AcademicPlan, Course, Semester, Subject
from subj.models import StudentGroup
from cwcs.models import Student
from forms import CourseworkTaskAddForm, CourseworkTaskEditForm
from course_work.models import TaskCourseWork, CourseWork, CourseWorkCommit

# Create your views here.
def is_teacher(user):
	if hasattr(user, 'person'):
		user = user.person
		if hasattr(user, 'teacher'):
			return True
	return False

def get_my_current_groups(teacher):
	param = {}

	groups = StudentGroup.objects.all()

	for group in groups:
		subjects = Subject.objects.filter(academicplan=group.academicplan)

		p = {}
		for subject in subjects:
			courses = Course.objects.filter(subject=subject)
			cc = {}
			for course in courses:
				semesters = Semester.objects.filter(course=course, number=group.academicplan.get_current_semester())
				ss = []
				for semester in semesters:
					if semester.teacher == teacher:
						ss.append(semester)
				if ss != []:
					cc[course] = ss
			if cc != {}:
				p[subject] = cc

		param[group] = p

	return param

def get_my_current_group(teacher, group_id):
	try:
		param = {}

		group = StudentGroup.objects.get(id=group_id)

		subjects = Subject.objects.filter(academicplan=group.academicplan)

		p = {}
		for subject in subjects:
			courses = Course.objects.filter(subject=subject)
			cc = {}
			for course in courses:
				semesters = Semester.objects.filter(course=course, number=group.academicplan.get_current_semester())
				ss = []
				for semester in semesters:
					if semester.teacher == teacher:
						ss.append(semester)
				if ss != []:
					cc[course] = ss
			if cc != {}:
				p[subject] = cc

		param['group'] = group
		param['subjects'] = p

		return param
	except:
		return None

def exists_group(teacher, group_id):
	if get_my_current_group(teacher, group_id) != None:
		return True
	return False

def get_students_from_group(group_id, taskcoursework_id):
	p = {}
	students = Student.objects.filter(studentgroup=StudentGroup.objects.get(id=group_id))
	for student in students:
		p[student] = CourseWork.objects.get(student=student, taskcoursework=TaskCourseWork.objects.get(id=taskcoursework_id))

	return p

def get_students_from_group2(group_id):
	return Student.objects.filter(studentgroup=StudentGroup.objects.get(id=group_id))

def existStudent(student_id, taskcoursework_id):
	try:
		student = Student.objects.get(id=student_id)
		taskcoursework = TaskCourseWork.objects.get(id=taskcoursework_id)
		cw = CourseWork.objects.get(taskcoursework=taskcoursework, student=student)
		if cw:
			return True
	except Exception, e:
		pass
	return False

def existsCommit(student_id, taskcoursework_id, commit_id):
	try:
		student = Student.objects.get(id=student_id)
		taskcoursework = TaskCourseWork.objects.get(id=taskcoursework_id)
		cw = CourseWork.objects.get(taskcoursework=taskcoursework, student=student)
		commit = CourseWorkCommit.objects.get(id=commit_id, coursework=cw)
		if commit:
			return True
	except Exception, e:
		pass
	return False

@user_passes_test(is_teacher)
def show_student_coursework_2(request, group_id, subject_id, course_id, semester_id, taskcoursework_id, student_id, commit_id):
	teacher = auth.get_user(request).person.teacher

	if exists_group(teacher, group_id):
		group = StudentGroup.objects.get(id=group_id)
		if group.academicplan.exists_coursework(subject_id, course_id, semester_id, taskcoursework_id):
			semester = group.academicplan.get_current_semester()
			if existStudent(student_id, taskcoursework_id):
				coursework_task = group.academicplan.get_coursework_task2(semester_id)
				if existsCommit(student_id, coursework_task.id, commit_id):
					student = Student.objects.get(id=student_id)
					commit = CourseWorkCommit.objects.get(id=commit_id)

					page = 'show_student_course_work_2.html'
					args = {
						'username' : teacher.name,
						'semester' : semester,
						'subject_title' : Subject.objects.get(id=subject_id).title,
						'student' : student,
						'group_id' : group_id,
						'subject_id' : subject_id,
						'course_id' : course_id,
						'semester_id' : semester_id,
						'taskcoursework_id' : taskcoursework_id,
						'commit' : commit,
					}
					args.update(csrf(request))
					return render_to_response(page, args)
	
	return redirect('/')

@user_passes_test(is_teacher)
def show_student_coursework(request, group_id, subject_id, course_id, semester_id, taskcoursework_id, student_id):
	teacher = auth.get_user(request).person.teacher

	if exists_group(teacher, group_id):
		group = StudentGroup.objects.get(id=group_id)

		if group.academicplan.exists_coursework(subject_id, course_id, semester_id, taskcoursework_id):
			semester = group.academicplan.get_current_semester()
			if existStudent(student_id, taskcoursework_id):
				student = Student.objects.get(id=student_id)
				coursework_task = group.academicplan.get_coursework_task2(semester_id)
				commits = CourseWork.objects.getCommitsByUserAndTask(student, coursework_task)

				page = 'show_student_course_work.html'
				args = {
					'username' : teacher.name,
					'semester' : semester,
					'subject_title' : Subject.objects.get(id=subject_id).title,
					'student' : student,
					'group_id' : group_id,
					'subject_id' : subject_id,
					'course_id' : course_id,
					'semester_id' : semester_id,
					'taskcoursework_id' : taskcoursework_id,
					'commits' : commits,
				}
				args.update(csrf(request))
				return render_to_response(page, args)
	
	return redirect('/')

@user_passes_test(is_teacher)
def show_students_coursework(request, group_id, subject_id, course_id, semester_id, taskcoursework_id):
	teacher = auth.get_user(request).person.teacher

	if exists_group(teacher, group_id):
		group = StudentGroup.objects.get(id=group_id)

		if group.academicplan.exists_coursework(subject_id, course_id, semester_id, taskcoursework_id):
			semester = group.academicplan.get_current_semester()

			coursework_task = group.academicplan.get_coursework_task2(semester_id)

			group = get_my_current_group(teacher, group_id)
			students = get_students_from_group(group_id, taskcoursework_id)

			page = 'show_students_course_work.html'
			args = {
				'username' : teacher.name,
				'semester' : semester,
				'subject_title' : Subject.objects.get(id=subject_id).title,
				'group' : group['group'],
				'coursework_task' : coursework_task,
				'students' : students,
				'subject_id' : subject_id,
				'course_id' : course_id,
				'semester_id' : semester_id,
			}
			args.update(csrf(request))
			return render_to_response(page, args)
	
	return redirect('/')

@user_passes_test(is_teacher)
def delete_coursework_task(request, group_id, subject_id, course_id, semester_id, taskcoursework_id):
	if request.POST:
		teacher = auth.get_user(request).person.teacher

		if exists_group(teacher, group_id):
			group = StudentGroup.objects.get(id=group_id)

			if group.academicplan.exists_coursework(subject_id, course_id, semester_id, taskcoursework_id):
				semester = Semester.objects.get(id=semester_id)
				semester.taskcoursework = None
				semester.save()

				TaskCourseWork.objects.get(id=taskcoursework_id).delete()

	return redirect('/teacher/groups/' + str(group_id) + '/courseworktask/' + str(subject_id) + '/' + str(course_id) + '/' + str(semester_id) + '/')

@user_passes_test(is_teacher)
def edit_coursework_task(request, group_id, subject_id, course_id, semester_id, taskcoursework_id):
	if request.POST:
		teacher = auth.get_user(request).person.teacher

		if exists_group(teacher, group_id):
			group = StudentGroup.objects.get(id=group_id)

			if group.academicplan.exists_coursework(subject_id, course_id, semester_id, taskcoursework_id):

				taskcoursework = TaskCourseWork.objects.get(id=taskcoursework_id)
				form = CourseworkTaskEditForm(request.POST, instance = taskcoursework)
				if form.is_valid():
					form.save(commit = True)

	return redirect('/teacher/groups/' + str(group_id) + '/courseworktask/' + str(subject_id) + '/' + str(course_id) + '/' + str(semester_id) + '/')

@user_passes_test(is_teacher)
def show_edit_coursework_task(request, group_id, subject_id, course_id, semester_id, taskcoursework_id):
	if request.POST:
		teacher = auth.get_user(request).person.teacher

		if exists_group(teacher, group_id):
			group = StudentGroup.objects.get(id=group_id)

			if group.academicplan.exists_coursework(subject_id, course_id, semester_id, taskcoursework_id):
				semester = group.academicplan.get_current_semester()
				current_semester = Semester.objects.get(id=semester_id)

				if current_semester.taskcoursework != None:
					page = 'edit_task_course_work.html'
					args = {
						'username' : teacher.name,
						'semester' : semester,
						'subject_title' : Subject.objects.get(id=subject_id).title,
						'group_id' : group_id,
						'subject_id' : subject_id,
						'course_id' : course_id,
						'semester_id' : semester_id,
						'form' : CourseworkTaskEditForm(instance = current_semester.taskcoursework),
						'taskcoursework_id' : taskcoursework_id,
					}
					args.update(csrf(request))
					return render_to_response(page, args)
	
	return redirect('/')

@user_passes_test(is_teacher)
def add_coursework_task(request, group_id, subject_id, course_id, semester_id):
	if request.POST:
		form = CourseworkTaskAddForm(request.POST)
		if form.is_valid():
			teacher = auth.get_user(request).person.teacher

			if exists_group(teacher, group_id):
				group = StudentGroup.objects.get(id=group_id)

				if group.academicplan.exists_coursework(subject_id, course_id, semester_id, taskcoursework_id):
					taskcoursework = form.save(commit = True)
					semester = Semester.objects.get(id=semester_id)
					#semester.taskcoursework_id = taskcoursework.id
					semester.taskcoursework = taskcoursework
					semester.save()

	return redirect('/teacher/groups/' + str(group_id) + '/courseworktask/' + str(subject_id) + '/' + str(course_id) + '/' + str(semester_id) + '/')

@user_passes_test(is_teacher)
def show_add_coursework_task(request, group_id, subject_id, course_id, semester_id):
	if request.POST:
		teacher = auth.get_user(request).person.teacher

		if exists_group(teacher, group_id):
			group = StudentGroup.objects.get(id=group_id)

			if group.academicplan.exists_coursework(subject_id, course_id, semester_id, taskcoursework_id):
				semester = group.academicplan.get_current_semester()

				page = 'add_task_course_work.html'
				args = {
					'username' : teacher.name,
					'semester' : semester,
					'subject_title' : Subject.objects.get(id=subject_id).title,
					'group_id' : group_id,
					'subject_id' : subject_id,
					'course_id' : course_id,
					'semester_id' : semester_id,
					'form' : CourseworkTaskAddForm(),
				}
				args.update(csrf(request))
				return render_to_response(page, args)
	
	return redirect('/')

@user_passes_test(is_teacher)
def show_coursework_task(request, group_id, subject_id, course_id, semester_id):
	teacher = auth.get_user(request).person.teacher

	if exists_group(teacher, group_id):
		group = StudentGroup.objects.get(id=group_id)

		if group.academicplan.exists_coursework2(subject_id, course_id, semester_id):
			cw = group.academicplan.get_coursework_task(subject_id, course_id, semester_id)
			semester = group.academicplan.get_current_semester()

			page = 'show_task_course_work.html'
			args = {
				'username' : teacher.name,
				'semester' : semester,
				'subject_title' : Subject.objects.get(id=subject_id).title,
				'coursework_task' : cw['taskcoursework'],
				'group_id' : group_id,
				'subject_id' : subject_id,
				'course_id' : course_id,
				'semester_id' : semester_id,
			}
			args.update(csrf(request))
			return render_to_response(page, args)
	
	return redirect('/')

@user_passes_test(is_teacher)
def show_teacher_page(request):
	return redirect(settings.LOGIN_REDIRECT_URL)

@user_passes_test(is_teacher)
def show_my_groups(request):
	teacher = auth.get_user(request).person.teacher

	groups = get_my_current_groups(teacher)

	page = 'show_my_groups.html'
	args = {
		'username' : teacher.name,
		'groups' : groups,
	}
	return render_to_response(page, args)

@user_passes_test(is_teacher)
def show_group(request, group_id):
	teacher = auth.get_user(request).person.teacher

	group = get_my_current_group(teacher, group_id)

	if group is not None:
		students = get_students_from_group2(group_id)

		page = 'show_group.html'
		args = {
			'username' : teacher.name,
			'group' : group['group'],
			'subjects' : group['subjects'],
			'students' : students,
			'group_id' : group_id,
		}
		return render_to_response(page, args)
	else:
		return redirect('/')