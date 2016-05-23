from django.conf.urls import url
import student_functions.views

urlpatterns = [
	url(r'^mycourseworks/$', student_functions.views.show_my_courseworks),
	url(r'^mycourseworks/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/$', student_functions.views.show_coursework),
	url(r'^mycourseworks/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<task_id>\d+)/$', student_functions.views.show_coursework_rep),
	url(r'^mycourseworks/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<task_id>\d+)/add/$', student_functions.views.show_add_coursework_rep),
	url(r'^mycourseworks/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<task_id>\d+)/add/update/$', student_functions.views.add_coursework_rep),
	url(r'^', student_functions.views.show_student_page),
]