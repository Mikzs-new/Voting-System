from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
router.register(r"courses", views.CourseViewSet, basename="courses")
router.register(r"students", views.StudentViewSet, basename="students")
router.register(r"elections", views.ElectionViewSet, basename="elections")
router.register(r"positions", views.PositionViewSet, basename="positions")
router.register(r"candidates", views.CandidateViewSet, basename="candidates")
router.register(r"partylists", views.PartylistViewSet, basename="partylist")
router.register(r"votes", views.VoteViewSet, basename="votes")
router.register(r"school_year_elections", views.SchoolYearElectionViewSet, basename="school_year_elections")

urlpatterns = [
    path('', include(router.urls)),
]
