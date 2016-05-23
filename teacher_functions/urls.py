from django.conf.urls import url
import teacher_functions.views

urlpatterns = [
	url(r'^groups/$', teacher_functions.views.show_my_groups),
	url(r'^groups/(?P<group_id>\d+)/$', teacher_functions.views.show_group),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/$', teacher_functions.views.show_coursework_task),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/add/$', teacher_functions.views.show_add_coursework_task),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/add/update/$', teacher_functions.views.add_coursework_task),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<taskcoursework_id>\d+)/edit/$', teacher_functions.views.show_edit_coursework_task),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<taskcoursework_id>\d+)/edit/update/$', teacher_functions.views.edit_coursework_task),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<taskcoursework_id>\d+)/delete/$', teacher_functions.views.delete_coursework_task),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<taskcoursework_id>\d+)/$', teacher_functions.views.show_students_coursework),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<taskcoursework_id>\d+)/(?P<student_id>\d+)/$', teacher_functions.views.show_student_coursework),
	url(r'^groups/(?P<group_id>\d+)/courseworktask/(?P<subject_id>\d+)/(?P<course_id>\d+)/(?P<semester_id>\d+)/(?P<taskcoursework_id>\d+)/(?P<student_id>\d+)/(?P<commit_id>\d+)/$', teacher_functions.views.show_student_coursework_2),
	url(r'^', teacher_functions.views.show_teacher_page),
]