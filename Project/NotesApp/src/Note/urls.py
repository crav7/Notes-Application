from django.conf.urls import url
from django.contrib import admin

#from . import views
from .views import(
	note_list,
	note_create,
	note_detail,
	note_update,
	note_delete,
	)
urlpatterns = [
		
		url(r'^$',note_list,name='list'),
		url(r'^create/$',note_create,name='create'),
		url(r'^(?P<slug>[\w-]+)/$',note_detail,name='detail'),
		url(r'^(?P<slug>[\w-]+)/edit/$',note_update,name='update'),
		url(r'^(?P<slug>[\w-]+)/delete/$',note_delete,name='delete'),

]