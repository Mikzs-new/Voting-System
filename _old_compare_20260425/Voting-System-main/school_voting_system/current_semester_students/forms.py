from django import forms

class AddCurrentSemesterStudents(forms.Form):
    csv_file = forms.FileField(
        label="Select a .csv file",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": ".csv"
            }
        ),
        required=True
    )