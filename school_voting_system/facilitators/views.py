from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from voting.models import SchoolElection, Election

@login_required
def add_election(request):
    return HttpResponse('trial')