from django import forms

class AddElectionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255, required=True)
    description = forms.CharField(label='Description', max_length=255)
    election_start = forms.DateTimeField(
        label='Election Start', 
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
    )
    election_end = forms.DateTimeField(
        label='Election End', 
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
    )

class AddSchoolYearElectionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255, required=True)
    academic_year = forms.CharField(label='Academic Year', max_length=255, required=True)
