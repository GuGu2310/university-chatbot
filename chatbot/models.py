
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    academic_level = models.CharField(max_length=50, blank=True)  # High School, Undergraduate, Graduate
    interests = models.TextField(blank=True)  # Academic interests
    consent_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    privacy_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'}'s Profile"

class Conversation(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    topic_category = models.CharField(max_length=50, blank=True)  # admissions, careers, programs, etc.
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Conversation {str(self.session_id)[:8]}"

class Message(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System')
    ]
    
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    helpfulness_score = models.FloatField(null=True, blank=True)  # User feedback on response quality
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."

class UniversityProgram(models.Model):
    PROGRAM_LEVELS = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('doctorate', 'Doctorate'),
        ('certificate', 'Certificate')
    ]
    
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=PROGRAM_LEVELS)
    description = models.TextField()
    requirements = models.TextField()
    duration = models.CharField(max_length=50)
    tuition_range = models.CharField(max_length=100, blank=True)
    career_prospects = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.university}"

class CareerPath(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_education = models.TextField()
    skills_needed = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True)
    job_outlook = models.TextField(blank=True)
    related_programs = models.ManyToManyField(UniversityProgram, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class AdmissionResource(models.Model):
    RESOURCE_TYPES = [
        ('application_tips', 'Application Tips'),
        ('scholarship', 'Scholarship'),
        ('financial_aid', 'Financial Aid'),
        ('test_prep', 'Test Preparation'),
        ('essay_help', 'Essay Help'),
        ('deadline', 'Important Deadline')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    url = models.URLField(blank=True)
    deadline_date = models.DateField(null=True, blank=True)
    is_priority = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class StudentCampaign(models.Model):
    CAMPAIGN_TYPES = [
        ('scholarship', 'Scholarship'),
        ('internship', 'Internship'),
        ('study_abroad', 'Study Abroad'),
        ('research', 'Research Opportunity'),
        ('club', 'Student Club/Organization'),
        ('event', 'Campus Event')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES)
    university = models.CharField(max_length=200, blank=True)
    deadline = models.DateField(null=True, blank=True)
    requirements = models.TextField(blank=True)
    benefits = models.TextField(blank=True)
    application_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
