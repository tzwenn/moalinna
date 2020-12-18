from django.urls import path

from . import views

app_name = 'authorized_keys'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('delete/<int:key_id>/', views.delete, name='delete'),
]
