from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import AddElectionForm

from voting.models import SchoolElection, Election, YearLevelValidItem, CoursesValidItem
from current_semester_students.models import Course

def add_election(request):

    if request.method == 'POST':
        return 0

    add_election_form = AddElectionForm()
    courses = Course.objects.all().values()
    context = {
        'election_form': add_election_form,
        'courses': courses,
    }

    return render(request, 'add_election.html', context)