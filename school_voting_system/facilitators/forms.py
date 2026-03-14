from django import forms

class AddElectionForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255, required=True)
    election_start = forms.DateTimeField(label='Election Start', required=True)
    election_end = forms.DateTimeField(label='Election End', required=True)
