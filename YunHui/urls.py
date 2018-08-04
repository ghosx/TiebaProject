from django.urls import path

from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('info/',views.info,name='info'),
    path('login/',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path(r'api/del/user/<uuid>/',views.delUser,name="deluser"),
    path(r'add/',views.add,name="add"),
    path(r'test/',views.test,name="test"),
]