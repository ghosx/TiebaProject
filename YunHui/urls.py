from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('info/',views.info,name='info'),
    path('login/',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path(r'del/<str:id>/',views.delete,name="delete"),
    path(r'about/',views.about,name='about'),
    path(r'add/',views.add,name="add"),
    path(r'switch/<str:id>/',views.switch,name="switch"),
    path(r'do/',views.do,name="do"),
]