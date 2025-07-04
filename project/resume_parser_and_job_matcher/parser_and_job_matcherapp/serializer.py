from rest_framework import serializers
from .models import *


class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'name']

class UserRegisterationSerializer(serializers.ModelSerializer):
    password_conformation = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password', 'phone_number', 'password_conformation']

    def validate(self, data):
        password = data.get('password')
        if not password:
            raise serializers.ValidationError(
                {"password": "Password is required."})

        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."})

        if data['password'] != data['password_conformation']:
            raise serializers.ValidationError("Passwords must match")
        return data


class UserSerializer(serializers.ModelSerializer):
    skills = SkillsSerializer(many=True)

    class Meta:
        model = Users
        fields = ['id', 'username', 'email', 'first_name', 'skills',
                  'resume_file', 'resume_content', 'phone_number']


class JobManagementSerializer(serializers.ModelSerializer):
    required_skills = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skills.objects.all()
    )

    class Meta:
        model = Job
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def create(self, validated_data):
        job = Job.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            posted_by=validated_data['posted_by']
        )
        job.required_skills.set(validated_data['required_skills'])
        return job


class JobSerializer(serializers.ModelSerializer):
    required_skills = SkillsSerializer(many=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'required_skills']
        depth = 1


class JobMatchSerializer(serializers.ModelSerializer):
    candidate = UserSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = MatchedJob
        fields = ['candidate', 'job', 'match_percentage']
