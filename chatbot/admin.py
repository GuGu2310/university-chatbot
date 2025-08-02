
from django.contrib import admin
from .models import (
    UserProfile, Conversation, Message, UniversityProgram, 
    CareerPath, AdmissionResource, StudentCampaign
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'academic_level', 'consent_given', 'created_at']
    list_filter = ['consent_given', 'privacy_accepted', 'academic_level', 'created_at']
    search_fields = ['user__username', 'user__email', 'interests']

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'topic_category', 'started_at', 'is_active']
    list_filter = ['is_active', 'topic_category', 'started_at']
    search_fields = ['session_id', 'user__username']
    readonly_fields = ['session_id']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'message_type', 'content_preview', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content']
    readonly_fields = ['timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(UniversityProgram)
class UniversityProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'level', 'duration', 'created_at']
    list_filter = ['level', 'university', 'created_at']
    search_fields = ['name', 'university', 'description']

@admin.register(CareerPath)
class CareerPathAdmin(admin.ModelAdmin):
    list_display = ['title', 'salary_range', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'skills_needed']
    filter_horizontal = ['related_programs']

@admin.register(AdmissionResource)
class AdmissionResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'deadline_date', 'is_priority', 'created_at']
    list_filter = ['resource_type', 'is_priority', 'deadline_date', 'created_at']
    search_fields = ['title', 'description']

@admin.register(StudentCampaign)
class StudentCampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'campaign_type', 'university', 'deadline', 'is_active', 'created_at']
    list_filter = ['campaign_type', 'is_active', 'university', 'deadline', 'created_at']
    search_fields = ['title', 'description', 'university']
