from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from datetime import datetime, timedelta
import random

from current_semester_students.models import Student
from .forms import VoterLogin, Verification

def login_view(request):
    error = False
    if request.method == 'POST':
        voter_login = VoterLogin(request.POST)
        if voter_login.is_valid():
            student_id = voter_login.cleaned_data['student_id']
            email_or_phone = voter_login.cleaned_data['email_or_phone']
            if Student.objects.filter(student_id=student_id, email=email_or_phone).exists():
                student = Student.objects.get(student_id=student_id)
                user = authenticate(request, username=student_id, password=email_or_phone)
                if user is not None:
                    login(request, user)
                    code = random.randint(100000, 999999)
                    request.session['otp'] = str(code)
                    request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=2)).timestamp()
                    request.session['student_id'] = student_id
                    send_mail(
                        f'Hello, {student.first_name} {student.last_name}',
                        f"This is the verification code to login in School Voting System {code}",
                        'schoolvotingsystem@gmail.com',
                        [email_or_phone],
                        fail_silently=False
                    )
                    return redirect('verification')
        error = True
        
    template = loader.get_template('login.html')
    voter_login = VoterLogin()
    context = {
        'voter_login': voter_login,
        'error': error,
    }   
    return HttpResponse(template.render(context, request=request))

@login_required(login_url='/login/')
def verification(request):
    if request.method == 'POST':
        if 'resend' in request.POST:
            code = random.randint(100000, 999999)
            request.session['otp'] = str(code)
            request.session['otp_expiry'] = (datetime.now() + timedelta(minutes=2)).timestamp()
            send_mail(
                f'Your New Voting Verification Code',
                f"This is the verification code to login in School Voting System {code}",
                'schoolvotingsystem@gmail.com',
                [request.user.email],
                fail_silently=False
            )
            verification_form = Verification()
            return render(request, 'verification.html', {'verification_form': verification_form, 'resent': True})
        
        verification_form = Verification(request.POST)
        expiry = request.session.get('otp_expiry')

        if expiry and datetime.now().timestamp() > expiry:
            logout(request)
            request.session.flush()
            template = loader.get_template('login.html')
            voter_login = VoterLogin()
            context = {
                'voter_login': voter_login,
                'expired': True
            }   
            return HttpResponse(template.render(context, request=request))

        if verification_form.is_valid():
            user_otp = verification_form.cleaned_data['otp']
            session_otp = request.session.get('otp')
            print(session_otp)
            if user_otp == session_otp:
                request.session['verified'] = True
                return redirect('dashboard')
            else:
                return render(request, 'verification.html', {'verification_form': verification_form,'error': True})
    verification_form = Verification()
    return render(request, 'verification.html', {'verification_form': verification_form})

