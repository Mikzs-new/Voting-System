from django.urls import path

from . import views

urlpatterns = [
    path('add_election/', views.add_election, name='add_election'),
    path('add_school_year/', views.add_school_year_election, name='add_school_year_election'),
]