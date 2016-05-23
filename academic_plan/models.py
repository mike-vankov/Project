# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError
import datetime
from django.db import models
from django.db.models import Manager

from subj.models import Department, Faculty, StudentGroup
from cwcs.models import Teacher
from course_work.models import TaskCourseWork, CourseWork

# Create your models here.
COURSE_CHOICES = []
for r in range(1, 8):
	COURSE_CHOICES.append((r,r))

SEMESTER_CHOICES = []
for r in range(1, 12):
	SEMESTER_CHOICES.append((r,r))

CONTROL_CHOICES_Z = 1
CONTROL_CHOICES_DZ = 2
CONTROL_CHOICES_EX = 3

CONTROL_CHOICES = [
	(CONTROL_CHOICES_Z, 'Зачет'),
	(CONTROL_CHOICES_DZ, 'Диф. зачет'),
	(CONTROL_CHOICES_EX, 'Экзамен'),
]

COURSEWORK_NONE = 'Задание на курсовую работу отсутствует!'
COURSEWORK_CHOICES_NONE = 0
COURSEWORK_CHOICES_CW = 1
COURSEWORK_CHOICES_CP = 2

COURSEWORK_CHOICES = [
	(COURSEWORK_CHOICES_NONE, 'Нет'),
	(COURSEWORK_CHOICES_CW, 'Курсовая работа'),
	(COURSEWORK_CHOICES_CP, 'Курсовой проект'),
]

DAY_CHOICES = []
for r in range(1, 32):
	DAY_CHOICES.append((r,r))

MONTH_CHOICES = [
	(1, 'Январь'),
	(2, 'Февраль'),
	(3, 'Март'),
	(4, 'Апрель'),
	(5, 'Май'),
	(6, 'Июнь'),
	(7, 'Июль'),
	(8, 'Август'),
	(9, 'Сентябрь'),
	(10, 'Октябрь'),
	(11, 'Ноябрь'),
	(12, 'Декабрь'),
]

class Special(models.Model):
	title = models.CharField(max_length=100, verbose_name='Название')

	class Meta:
		verbose_name = "Тип"
		verbose_name_plural = "Типы"

	def __unicode__(self):
		return unicode(self.title)

class SpecialCourse(models.Model):
	number = models.PositiveIntegerField(choices=COURSE_CHOICES, verbose_name='Курс')

	special = models.ForeignKey(Special, verbose_name='Курс')

	class Meta:
		verbose_name = "Курс"
		verbose_name_plural = "Курсы"

	def __unicode__(self):
		return unicode('Курс ' + str(self.number))

class SpecialSemester(models.Model):
	number = models.PositiveIntegerField(choices=SEMESTER_CHOICES, verbose_name='Семестр')

	startday = models.PositiveIntegerField(choices=DAY_CHOICES, verbose_name='Начало семестра, день', default=1)
	startmonth = models.PositiveIntegerField(choices=MONTH_CHOICES, verbose_name='Начало семестра, месяц', default=1)
	endday = models.PositiveIntegerField(choices=DAY_CHOICES, verbose_name='Конец семестра, день', default=1)
	endmonth = models.PositiveIntegerField(choices=MONTH_CHOICES, verbose_name='Конец семестра, месяц', default=1)

	specialcourse = models.ForeignKey(SpecialCourse, verbose_name='Курс')

	def clean(self):
		try:
			d1 = datetime.date(2000, self.startmonth, self.startday)
			d2 = datetime.date(2000, self.endmonth, self.endday)
		except:
			raise ValidationError(message='Проверьте правильность ввода даты!', code='dateerror')

	class Meta:
		verbose_name = "Семестр"
		verbose_name_plural = "Семестры"

	def __unicode__(self):
		return unicode('Семестр ' + str(self.number))

#TOP
class AcademicPlan(models.Model):
	date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
	title = models.CharField(max_length=100, verbose_name='Название плана')

	faculty = models.ForeignKey(Faculty, verbose_name='Факультет')
	department = models.ForeignKey(Department, verbose_name='Кафедра')

	special = models.ForeignKey(Special, verbose_name='Тип', null=True)

	def get_courses(self):
		d = {}
		year_start = StudentGroup.objects.get(academicplan=self).year
		year_end = year_start

		courses = SpecialCourse.objects.filter(special=self.special)
		for course in courses:
			semesters = SpecialSemester.objects.filter(specialcourse=course)
			for semester in semesters:
				if (semester.endmonth < semester.startmonth) or ((semester.endmonth == semester.startmonth) and (semester.endday < semester.startday)):
					year_end = year_start + 1
			d[course] = [semesters, year_start, year_end]
			year_start = year_end

		return d

	def get_current_semester(self):
		try:
			for key, value in self.get_courses().items():
				for semester in value[0]:
					d1 = datetime.date(value[1], semester.startmonth, semester.startday)
					d2 = datetime.date(value[2], semester.endmonth, semester.endday)
					if d1 < datetime.datetime.now().date() < d2:
						return semester.number
		except:
			return None

	def get_current_courseworks(self):
		current_semester = self.get_current_semester()
		if current_semester is None:
			return None

		param = {}
		param['current_semester'] = current_semester
		text = ''
		subjects = Subject.objects.filter(academicplan=self)

		p = {}
		for subject in subjects:
			courses = Course.objects.filter(subject=subject)
			cc = {}
			for course in courses:
				semesters = Semester.objects.filter(course=course)
				ss = []
				for semester in semesters:
					if (int(semester.number) == int(current_semester)) and (semester.coursework != COURSEWORK_CHOICES_NONE):
						ss.append(semester)
				if ss != []:
					cc[course] = ss
			if cc != {}:
				p[subject] = cc

		param['subjects'] = p

		return param

	def exists_coursework2(self, subject_id, course_id, semester_id):
		try:
			current_semester = self.get_current_semester()

			subjects = Subject.objects.filter(academicplan=self, id=subject_id)
			courses = Course.objects.filter(subject__in=subjects, id=course_id)
			semesters = Semester.objects.filter(course__in=courses, id=semester_id, number=current_semester)

			if subjects.exists() and courses.exists() and semesters.exists():
				return True
		except:
			pass
		return False

	def exists_coursework(self, subject_id, course_id, semester_id, taskcoursework_id):
		try:
			cw = TaskCourseWork.objects.get(id=taskcoursework_id)

			if self.exists_coursework2(subject_id, course_id, semester_id) and cw:
				return True
		except:
			pass
		return False

	def get_coursework_task(self, subject_id, course_id, semester_id):
		param = {}

		param['subject_title'] = Subject.objects.get(id=subject_id).title
		semester = Semester.objects.get(id=semester_id)

		param['taskcoursework'] = semester.taskcoursework
		param['teacher'] = semester.teacher

		return param

	def get_coursework_task2(self, semester_id):
		semester = Semester.objects.get(id=semester_id)
		return semester.taskcoursework

	def exists_coursework_task(self, subject_id, course_id, semester_id, task_id):
		if self.exists_coursework2(subject_id, course_id, semester_id):
			semesters = Semester.objects.filter(taskcoursework=task_id)
			if semesters.exists():
				return True
		return False

	def get_subject_title(self, subject_id):
		return Subject.objects.get(id=subject_id).title

	class Meta:
		verbose_name = "Учебный план"
		verbose_name_plural = "Учебные планы"

	def __unicode__(self):
		return unicode(self.title)

#ONE
class Subject(models.Model):
	department = models.CharField(max_length=50, verbose_name='Кафедра')
	index = models.CharField(max_length=10, verbose_name='Индекс дисциплины')
	title = models.CharField(max_length=100, verbose_name='Название дисциплины')

	academicplan = models.ForeignKey(AcademicPlan, verbose_name='Учебный план')

	class Meta:
		verbose_name = "Предмет"
		verbose_name_plural = "Предметы"

	def __unicode__(self):
		return unicode(self.title)
#TWO
class Course(models.Model):
	number = models.PositiveIntegerField(choices=COURSE_CHOICES, verbose_name='Курс')

	subject = models.ForeignKey(Subject, verbose_name='Курс')

	class Meta:
		verbose_name = "Курс"
		verbose_name_plural = "Курсы"

	def __unicode__(self):
		return unicode('Курс ' + str(self.number))
#THREE
class Semester(models.Model):
	number = models.PositiveIntegerField(choices=SEMESTER_CHOICES, verbose_name='Семестр')

	lec = models.PositiveIntegerField(verbose_name='Лекции', default=0)
	lab = models.PositiveIntegerField(verbose_name='Лабораторные', default=0)
	prc = models.PositiveIntegerField(verbose_name='Практические', default=0)
	ksr = models.PositiveIntegerField(verbose_name='КСР', default=0)
	srs = models.PositiveIntegerField(verbose_name='СРС', default=0)

	course = models.ForeignKey(Course, verbose_name='Курс')

	control = models.PositiveIntegerField(choices=CONTROL_CHOICES, verbose_name='Вид контроля', default=CONTROL_CHOICES_Z)
	coursework = models.PositiveIntegerField(choices=COURSEWORK_CHOICES, verbose_name='Курсовая работа', default=COURSEWORK_CHOICES_NONE)

	teacher = models.ForeignKey(Teacher, verbose_name='Преподаватель', null=True, blank=True)
	taskcoursework = models.ForeignKey(TaskCourseWork, verbose_name='Задание на курсовую работу', blank=True, null=True)

	class Meta:
		verbose_name = "Семестр"
		verbose_name_plural = "Семестры"

	def __unicode__(self):
		return unicode('Семестр ' + str(self.number))