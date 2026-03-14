from django.urls import path

from . import views

urlpatterns = [
    path('add_election/', views.add_election, name='add_election'),
]