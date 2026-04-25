from rest_framework import serializers

from current_semester_students.views import Student, Course
from facilitators.models import Facilitator
from running_candidates.models import Position, Partylist, Candidate
from voters.models import Vote, VoteItem
from voting.models import SchoolYearElection, Election, CoursesValidItem, YearLevelValidItem

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_name(self, value):
        if Course.objects.filter(name=value).exists():
            raise serializers.ValidationError('Course Already Exists')
        return value

class StudentSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'student_school_id', 'course', 'year_level', 'email']

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

#FIX THIS POST
class FacilitatorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilitator
        exclude = '__all__'

class PartylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partylist
        fields = '__all__'

#FIX THIS POST
class PartylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partylist
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

#FIX THIS POST
class PositionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

#FIX THIS POST
class CandidateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class ElectionSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    year_levels = serializers.SerializerMethodField()
    positions = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = ['id', 'title', 'courses', 'year_levels', 'positions']

    def get_positions(self, obj):
        positions = obj.position_set.all()
        return PositionSerializer(positions,many=True).data

    def get_courses(self, obj):
        courses = [item.course for item in obj.coursesvaliditem_set.all()]
        return CourseSerializer(courses,many=True).data

    def get_year_levels(self, obj):
        return [item.year_level for item in obj.yearlevelvaliditem_set.all()]

class ElectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Election
        fields = ['title','school_election']

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

#FIX THIS POST
class VoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class SYESerializer(serializers.ModelSerializer):
    elections = ElectionSerializer(source='election_set',many=True)
    class Meta:
        model = SchoolYearElection
        fields = ['title','academic_year','elections']

class SYECreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYearElection
        fields = ['title','academic_year']

        


