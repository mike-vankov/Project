# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import StudentGroup, Department, Faculty

# Register your models here.
class StudentGroupAdmin(admin.ModelAdmin):
	list_display = [
		'title',
		'year',
		'department',
	]

	list_filter = ['department', 'year']

class DepartmentAdmin(admin.ModelAdmin):
	list_display = [
		'title_short',
		'title_full',
		'faculty',
	]

	list_filter = ['faculty']

class FacultyAdmin(admin.ModelAdmin):
	list_display = [
		'title_short',
		'title_full',
	]

admin.site.register(StudentGroup, StudentGroupAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Faculty, FacultyAdmin)