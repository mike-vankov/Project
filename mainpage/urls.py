from django.conf.urls import url
import mainpage.views

urlpatterns = [
	url(r'^auth/login/$', mainpage.views.login),
    url(r'^auth/logout/$', mainpage.views.logout),
	url(r'^$', mainpage.views.showmainpage),
]