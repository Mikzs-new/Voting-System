from django import forms

class VoterLogin(forms.Form):
    student_id = forms.CharField(label='Student ID', max_length=255, required=True)
    email_or_phone = forms.CharField(label='Email',max_length=255, required=True)

class Verification(forms.Form):
    otp = forms.CharField(label="Enter OTP Code", max_length=6, required=True)