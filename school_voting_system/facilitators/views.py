from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import json

from .forms import AddElectionForm, AddSchoolYearElectionForm

from voting.models import SchoolYearElection, Election, YearLevelValidItem, CoursesValidItem
from current_semester_students.models import Course
from running_candidates.models import Position

def add_election(request):
    if request.method == 'POST':
        add_election_form = AddElectionForm(request.POST)
        if add_election_form.is_valid():
            title = add_election_form.cleaned_data['title']
            description = add_election_form.cleaned_data['description']
            election_start = add_election_form.cleaned_data['election_start']
            election_end = add_election_form.cleaned_data['election_end']
            positions = json.loads(request.POST.get('positions', '[]'))
            qualified_courses = json.loads(request.POST.get('courses', '[]'))
            qualified_levels = json.loads(request.POST.get('year_levels', '[]'))
            
            Election.objects.create(
                title=title, 
                description=description, 
                start_voting_date=election_start, 
                end_voting_date=election_end,
                school_election=SchoolYearElection.objects.order_by('-id').first(),
            )

            election = Election.objects.order_by('-id').first()

            for title,count in positions:
                Position.objects.create(
                    title=title,
                    seat_count=count,
                    election=election
                )
                
            for course in qualified_courses:
                CoursesValidItem.objects.create(
                    course=Course.objects.get(id=course),
                    election_id=election
                )

            for level in qualified_levels:
                YearLevelValidItem.objects.create(
                    year_level=level,
                    election_id=election
                )


    add_election_form = AddElectionForm()
    courses = Course.objects.all().values()
    context = {
        'election_form': add_election_form,
        'courses': courses,
    }

    return render(request, 'add_election.html', context)

def add_school_year_election(request):
    if request.method == 'POST':
        school_year_form = AddSchoolYearElectionForm(request.POST)
        if school_year_form.is_valid():
            title = school_year_form.cleaned_data['title']
            academic_year = school_year_form.cleaned_data['academic_year']
            SchoolYearElection.objects.create(title=title, academic_year=academic_year)
            return HttpResponse('TURE')
        
    school_year_form = AddSchoolYearElectionForm()
    school_elections = SchoolYearElection.objects.all().values()
    context = {
        'add_school_election': school_year_form,
        'school_election': school_elections
    }
    return render(request, 'add_school_election.html', context)