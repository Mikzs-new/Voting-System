from django.urls import path
from . import views

urlpatterns = [
    path('add_students/', views.add_students, name='add_students'),
    path('all_students/', views.all_students, name='all_students')
]