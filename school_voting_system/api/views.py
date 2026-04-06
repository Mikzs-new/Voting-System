from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets

from current_semester_students.models import Student
from voting.models import Election, SchoolYearElection
from .serializer import StudentSerializer, StudentCreateSerializer, ElectionSerializer, ElectionCreateSerializer, SYESerializer, SYECreateSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentCreateSerializer
        return StudentSerializer

class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ElectionCreateSerializer
        return ElectionSerializer

class SchoolYearElectionViewSet(viewsets.ModelViewSet):
    queryset = SchoolYearElection.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SYECreateSerializer
        return SYESerializer