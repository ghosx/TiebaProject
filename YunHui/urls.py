from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path(r'api/del/user/<uuid>/',views.delUser,name="deluser"),
    path(r'add/',views.add,name="add"),
    path(r'test/',views.test,name="test"),
]