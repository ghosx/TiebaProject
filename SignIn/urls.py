from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'info/', views.info, name='info'),
    path(r'login/', views.login, name='login'),
    path(r'logout/', views.logout, name='logout'),
    path(r'about/',views.about,name='about'),
    path(r'bduss/',views.bduss,name="bduss"),
]