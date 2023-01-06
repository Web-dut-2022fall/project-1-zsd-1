from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("wiki/<slug:title>", views.view_entry, name="view_entry"), 
	path("entry/create", views.create_entry, name="create_entry"),  
	path("entry/edit/<slug:title>", views.edit_entry, name="edit_entry"), 
	path("random", views.random, name="random"),   
]
