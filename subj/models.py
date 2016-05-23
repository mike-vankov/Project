# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import datetime

YEAR_CHOICES = []
for r in range(datetime.datetime.now().year-7, (datetime.datetime.now().year+2)):
	YEAR_CHOICES.append((r,r))

# Create your models here.
class Faculty(models.Model):
	title_full = models.CharField(max_length=50, verbose_name='Полное название факультета')
	title_short = models.CharField(max_length=10, verbose_name='Краткое название факультета')

	def __unicode__(self):
		return unicode(self.title_short)

	class Meta:
		verbose_name = "Факультет"
		verbose_name_plural = "Факультеты"

class Department(models.Model):
	title_full = models.CharField(max_length=100, verbose_name='Полное название кафедры')
	title_short = models.CharField(max_length=10, verbose_name='Краткое название кафедры')

	faculty = models.ForeignKey(Faculty, verbose_name='Факультет', null=True)

	class Meta:
		verbose_name = "Кафедра"
		verbose_name_plural = "Кафедры"

	def __unicode__(self):
		return unicode(self.title_short)

class StudentGroup(models.Model):
	title = models.CharField(max_length=10, verbose_name='Название группы')
	year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year, verbose_name='Год поступления')

	department = models.ForeignKey(Department, verbose_name='Кафедра', null=True)

	academicplan = models.OneToOneField('academic_plan.AcademicPlan', verbose_name='Учебный план', blank=True, null=True)

	def __unicode__(self):
		return unicode(self.title)

	class Meta:
		verbose_name = "Группа"
		verbose_name_plural = "Группы"