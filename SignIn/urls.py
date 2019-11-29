from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name="index"),
    path(r'bduss/', views.new, name="new"),
    path(r'image/', views.get_img, name='image'),
    path(r'status/', views.status, name='status')
]