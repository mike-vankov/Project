# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from course_work.models import CourseWorkCommit

class SomeBaseForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ModelForm, self).__init__(*args, **kwargs)
		for _, field in self.fields.items():
			if field.widget.is_required:
				field.widget.attrs['required'] = 'required'

class CourseWorkAddForm(SomeBaseForm):
	class Meta:
		model = CourseWorkCommit
		fields = '__all__'
		exclude = ['date_create', 'coursework']
