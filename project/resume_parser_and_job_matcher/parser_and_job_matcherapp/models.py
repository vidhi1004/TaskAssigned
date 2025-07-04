from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date
from django.utils import timezone
# Create your models here.


class Skills(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Users(AbstractUser):
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    resume_content = models.TextField(null=True, blank=True)
    skills = models.ManyToManyField(Skills, null=True, blank=True)
    phone_number = models.CharField(max_length=10)


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    required_skills = models.ManyToManyField(Skills, null=True, blank=True)
    posted_by = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class MatchedJob(models.Model):
    candidate = models.ForeignKey(Users, on_delete=models.CASCADE)
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="job_match")
    match_percentage = models.IntegerField()

    class Meta:
        unique_together = ("candidate", "job")
