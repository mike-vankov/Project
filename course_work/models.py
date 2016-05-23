# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models import Manager

from cwcs.models import Student

# Create your models here.
class TaskCourseWork(models.Model):
	title = models.CharField(max_length=100, verbose_name='Название курсовой работы')
	text = models.TextField(verbose_name='Описание', default="")
	date_create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата создания', null=True)
	date_update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования', null=True)
	#file = ...

	class Meta:
		verbose_name = "Задание на курсовую работу"
		verbose_name_plural = "Задания на курсовые работы"

	def __unicode__(self):
		return unicode(self.title)

class CourseWorkManager(models.Manager):
	def getByUserAndTask(self, student, task):
		try:
			result = CourseWork.objects.get(student=student, taskcoursework=task)
		except:
			result = None
		return result

	def getCommitsByUserAndTask(self, student, task):
		try:
			result = self.getByUserAndTask(student, task).getCommits().order_by('-date_create')
		except:
			result = None
		return result
		

class CourseWork(models.Model):
	date_create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата создания', null=True)
	date_update = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования', null=True)
	#file = ...

	taskcoursework = models.ForeignKey(TaskCourseWork, verbose_name='Задание на курсовую работу')
	student = models.ForeignKey(Student, verbose_name='Студент')

	editable = models.BooleanField(default=True, verbose_name='Редактируемый')

	objects = CourseWorkManager()

	def getCommits(self):
		return CourseWorkCommit.objects.filter(coursework=self)

	class Meta:
		verbose_name = "Отчет по курсовой работе"
		verbose_name_plural = "Отчеты по курсовой работе"

	def __unicode__(self):
		return unicode("Отчет по курсовой работе")

class CourseWorkCommit(models.Model):
	title = models.CharField(max_length=100, verbose_name='Заголовок')
	text = models.TextField(verbose_name='Описание', default="", blank=True)
	date_create = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата создания', null=True)
	#file = ...

	coursework = models.ForeignKey(CourseWork, verbose_name='Отчет по курсовой работе', null=True)

	class Meta:
		verbose_name = "Отправленная работа"
		verbose_name_plural = "Отправленные работы"

	def __unicode__(self):
		return unicode('%s (%s)' % (self.title, str(self.date_create)))
