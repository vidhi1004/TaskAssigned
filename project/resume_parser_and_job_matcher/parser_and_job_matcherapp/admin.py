from django.contrib import admin
from .models import *


@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'posted_by')
    search_fields = ('title', 'description')
    filter_horizontal = ('required_skills',)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ('skills',)
    readonly_fields = ('resume_file', 'resume_content')


@admin.register(MatchedJob)
class MatchedJobAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'match_percentage')
    search_fields = ('candidate__username', 'job__title')


admin.site.site_header = "Job Matcher Admin"
admin.site.site_title = "Job Matcher Portal"
admin.site.index_title = "Welcome to Job Matcher Dashboard"
