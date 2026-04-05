from rest_framework import serializers

from current_semester_students.views import Student, Course
from voters.models import Vote, VoteItem
from voting.models import SchoolYearElection, Election, CoursesValidItem, YearLevelValidItem

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'student_school_id', 'course', 'year_level', 'email']

class ElectionSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    year_levels = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = ['id', 'title', 'courses', 'year_levels']

    def get_courses(self, obj):
        return [item.course.id for item in obj.coursesvaliditem_set.all()]

    def get_year_levels(self, obj):
        return [item.year_level for item in obj.yearlevelvaliditem_set.all()]

class SYESerializer(serializers.ModelSerializer):
    elections = ElectionSerializer(many=True)
    class Meta:
        model = SchoolYearElection
        fields = ['title','academic_year','elections']

        


