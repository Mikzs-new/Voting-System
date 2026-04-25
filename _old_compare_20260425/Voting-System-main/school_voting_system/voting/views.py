from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from current_semester_students.models import Student

@login_required(login_url='/login/')
def dashboard(request):
    student = Student.objects.get(student_id=request.user.username)
    template = loader.get_template('dashboard.html')
    context = {
        'student': student,
    }
    return HttpResponse(template.render(context, request))