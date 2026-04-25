from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User

import pandas as pd

from .forms import AddCurrentSemesterStudents
from .models import Student, Course

def add_students(request):
    add_student_form = AddCurrentSemesterStudents()
    missing_value = False
    if(request.method == 'POST'):
        add_student_form = AddCurrentSemesterStudents(request.POST, request.FILES)
        if(add_student_form.is_valid()):
            students_csv = add_student_form.cleaned_data['csv_file']
            students_df = pd.read_csv(students_csv)
            if(validate_csv(students_df)):
                missing_values = students_df[students_df.isnull().any(axis=1)]
                missing_value = not missing_values.empty
                students_df.dropna(inplace=True)
                students_to_create = []
                for _, row in students_df.iterrows():
                    if not Student.objects.filter(student_school_id=row['student_id']).exists():
                        if not Course.objects.filter(name=row['course']).exists():
                            Course.objects.create(name=row['course'])
                        students_to_create.append(Student(
                            student_school_id=row['student_id'],
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            course=Course.objects.get(name=row['course']),
                            year_level=row['year'],
                            email=row['email']
                        ))
                        User.objects.create_user(
                            username=row['student_id'],
                            email=row['email'],
                            password=row['email']
                        )

                Student.objects.bulk_create(students_to_create)
                return render(request, 'add_students.html', {'add_students_form': add_student_form, 'missing_values': missing_values, 'missing_value': missing_value})
            else:
                return render(request, 'add_students.html', {'add_students_form': add_student_form, 'error': True, 'missing_value': missing_value}) 
    return render(request, 'add_students.html', {'add_students_form': add_student_form, 'missing_value': missing_value})

def all_students(request):
    template = loader.get_template('all_students.html')
    students = Student.objects.all().values()
    context = {
        'students': students
    }
    return HttpResponse(template.render(context, request))

def validate_csv(students_df):
    required_columns = [
        'student_id',
        'first_name',
        'last_name',
        'course',
        'year',
        'email'
    ]
    return list(students_df.columns) == required_columns