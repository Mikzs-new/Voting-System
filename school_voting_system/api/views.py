from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from current_semester_students.models import Student
from voting.models import Election, SchoolYearElection
from .serializer import StudentSerializer, ElectionSerializer, SYESerializer

@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PUT','DELETE'])
def student_details(request, pk):
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','DELETE'])
def election_details(request, pk):
    election = Election.objects.get(id=pk)
    serializer = ElectionSerializer(election)
    return Response(serializer.data)

@api_view(['GET','POST'])
def school_year_election_list(request):
    if request.method == 'GET':
        school_year_election = SchoolYearElection.objects.all()
        serializer = SYESerializer(school_year_election, many=True)
        return Response(serializer.data)
    return