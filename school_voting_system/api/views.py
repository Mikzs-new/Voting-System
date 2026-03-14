from rest_framework.response import Response
from rest_framework.decorators import api_view

from current_semester_students.models import Student

@api_view(['GET'])
def getData(request):
    data = Student.objects.all().values()
    return Response(data)