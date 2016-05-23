# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserChangeForm

from .models import Person, Student, Teacher

# Register your forms here.
class PersonCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение', widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return password2

    def save(self, commit=True):
        user = super(PersonCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = Person
        fields = ['username', 'last_name', 'first_name', 'middle_name', 'birthday']

    def __init__(self, *args, **kwargs):
	    super(PersonCreationForm, self).__init__(*args, **kwargs)
	    self.fields['last_name'].required=True
	    self.fields['first_name'].required=True
	    self.fields['middle_name'].required=True

class PersonChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField(label='Пароль', help_text= ("Пароли хранятся в защищённом виде, так что у нас нет способа узнать пароль этого пользователя. Однако вы можете сменить его/её пароль, используя "
                    "<a href=\"../password/\">эту форму</a>."))

	def clean_password(self):
		return self.initial['password']

	class Meta:
		fields = ['username', 'password', 'last_name', 'first_name', 'middle_name', 'birthday']

	def __init__(self, *args, **kwargs):
	    super(PersonChangeForm, self).__init__(*args, **kwargs)
	    self.fields['last_name'].required=True
	    self.fields['first_name'].required=True
	    self.fields['middle_name'].required=True

# Register your models here.
class NewUserAdmin(UserAdmin):
    list_display = [
        'username',
        'is_staff',
        'last_login',
        'date_joined',
    ]

    list_filter = ['is_staff',]

class PersonAdmin(NewUserAdmin):
	form = PersonChangeForm
	add_form = PersonCreationForm

	list_display = [
        'username',
        'name',
    ]

	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'birthday')}),
	)

	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2'
            )}
         ),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'birthday')}),
    )

class StudentAdmin(PersonAdmin):
	list_filter = ['studentgroup']

	list_display = [
		'username',
		'last_name',
		'first_name',
		'middle_name',
		'studentgroup',
	]

	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'birthday')}),
		('Данные студента', {'fields': ('number', 'studentgroup')}),
	)

	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2'
            )}
         ),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'birthday')}),
        ('Данные студента', {'fields': ('number', 'studentgroup')}),
    )

class TeacherAdmin(PersonAdmin):
	list_filter = ['isGeneral']

	list_display = [
		'username',
		'last_name',
		'first_name',
		'middle_name',
		'rank',
		'academic_degree',
		'isGeneral',
	]

	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'birthday')}),
		('Данные преподавателя', {'fields': ('rank', 'academic_degree', 'isGeneral')}),
	)

	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'password1',
                'password2'
            )}
         ),
        ('Личные данные', {'fields': ('last_name', 'first_name', 'middle_name', 'birthday')}),
        ('Данные преподавателя', {'fields': ('rank', 'academic_degree', 'isGeneral')}),
    )
	
admin.site.register(Person, PersonAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)