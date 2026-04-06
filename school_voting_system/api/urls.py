from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"students", views.StudentViewSet, basename="students")
router.register(r"elections", views.ElectionViewSet, basename="elections")
router.register(r"school_year_elections", views.SchoolYearElectionViewSet, basename="school_year_elections")

urlpatterns = [
    path('', include(router.urls)),
]
