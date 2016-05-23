# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import AcademicPlan, Subject, Course, Semester, Special, SpecialCourse, SpecialSemester#, TypeOfControl#, WorkTime#, ASTT
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin

# Register your models here.
class SemesterInline(NestedStackedInline):
	model = Semester
	extra = 1
	fk_name = 'course'
	exclude = ['taskcoursework']

class CourseInline(NestedStackedInline):
	model = Course
	extra = 1
	fk_name = 'subject'
	inlines = [SemesterInline]

class SpecialSemesterInline(NestedTabularInline):
	model = SpecialSemester
	extra = 1
	fk_name = 'specialcourse'

class SubjectInline(NestedStackedInline):
	model = Subject
	extra = 1
	fk_name = 'academicplan'
	inlines = [CourseInline]

class SpecialCourseInline(NestedStackedInline):
	model = SpecialCourse
	extra = 1
	fk_name = 'special'
	inlines = [SpecialSemesterInline]

class AcademicPlanAdmin(NestedModelAdmin):
	model = AcademicPlan
	inlines = [SubjectInline]

	exclude = ['date']

	list_filter = [
		'department',
		'faculty',
		'special',
	]

	list_display = [
		'title',
		'date',
		'special',
	]

class SpecialAdmin(NestedModelAdmin):
	model = Special
	inlines = [SpecialCourseInline]

admin.site.register(AcademicPlan, AcademicPlanAdmin)
admin.site.register(Special, SpecialAdmin)