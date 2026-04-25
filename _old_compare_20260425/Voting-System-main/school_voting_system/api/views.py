from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets

from current_semester_students.models import Student, Course
from running_candidates.models import Position, Candidate, Partylist
from voters.models import Vote
from voting.models import Election, SchoolYearElection
from .serializer import CourseSerializer, StudentSerializer, StudentCreateSerializer, PositionSerializer, PartylistSerializer, CandidateSerializer, ElectionSerializer, ElectionCreateSerializer, SYESerializer, VoteSerializer, SYECreateSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        return CourseSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentCreateSerializer
        return StudentSerializer

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()

    def get_serializer_class(self):
        return PositionSerializer
    
class PartylistViewSet(viewsets.ModelViewSet):
    queryset = Partylist.objects.all()

    def get_serializer_class(self):
        return PartylistSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()

    def get_serializer_class(self):
        return CandidateSerializer

class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ElectionCreateSerializer
        return ElectionSerializer

class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()

    def get_serializer_class(self):
        return VoteSerializer

class SchoolYearElectionViewSet(viewsets.ModelViewSet):
    queryset = SchoolYearElection.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SYECreateSerializer
        return SYESerializer

