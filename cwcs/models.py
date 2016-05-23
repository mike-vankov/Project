# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from subj.models import StudentGroup
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your models here.
class Person(User):
	birthday = models.DateField(verbose_name='Дата рождения')
	middle_name = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
	name = models.CharField(max_length=50, verbose_name='ФИО')

	def clean(self):
		self.first_name = self.first_name.capitalize()
		self.last_name = self.last_name.capitalize()
		self.middle_name = self.middle_name.capitalize()
		self.name = self.last_name + " " + self.first_name + " " + self.middle_name

	class Meta:
		verbose_name = "Локальный пользователь"
		verbose_name_plural = "Локальные пользователи"

class Student(Person):
	number = models.CharField(max_length=10, verbose_name='Номер зачетной книжки', blank=False)

	studentgroup = models.ForeignKey(StudentGroup, verbose_name='Группа', blank=False, null=True)

	def __unicode__(self):
		return unicode(self.name)

	class Meta:
		verbose_name = "Студент"
		verbose_name_plural = "Студенты"

class Teacher(Person):
	rank = models.CharField(max_length=100, verbose_name='Учёное завание') #доцент кафдеры, профессор...
	academic_degree = models.CharField(max_length=100, verbose_name='Учёная степень', default='') #кандидат наук, доктор

	isGeneral = models.BooleanField(default=False, verbose_name='Просмотр всех')

	def __unicode__(self):
		return unicode(self.name)

	class Meta:
		verbose_name = "Преподаватель"
		verbose_name_plural = "Преподаватели"