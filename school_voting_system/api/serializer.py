from rest_framework import serializers

from current_semester_students.views import Student, Course
from facilitators.models import Facilitator
from voters.models import Vote, VoteItem
from voting.models import SchoolYearElection, Election, CoursesValidItem, YearLevelValidItem

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['id']

    def validate_student_school_id(self, value):
        if Student.objects.filter(student_school_id=value).exists():
            raise serializers.ValidationError('Student Already Exists')
        return value
    
class FacilitatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilitator
        fields = '__all__'

class FacilitatorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilitator
        exclude = ['id']
    
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

class ElectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['title','school_election']

class SYESerializer(serializers.ModelSerializer):
    elections = ElectionSerializer(source='election_set',many=True)
    class Meta:
        model = SchoolYearElection
        fields = ['title','academic_year','elections']

class SYECreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYearElection
        fields = ['title','academic_year']

        


