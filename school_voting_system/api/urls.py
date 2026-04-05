from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    path('students/', views.student_list),
    path('student/<int:pk>/', views.student_details),
    path('election/<int:pk>/', views.election_details),
    path('school_year_elections/', views.school_year_election_list)
]

urlpatterns = format_suffix_patterns(urlpatterns)