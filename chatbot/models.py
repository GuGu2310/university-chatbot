
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    academic_level = models.CharField(max_length=50, blank=True)
    interests = models.TextField(blank=True)
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
    topic_category = models.CharField(max_length=50, blank=True)
    
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
    helpfulness_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."

# University Information Models for Admin Management
class UniversityProgram(models.Model):
    PROGRAM_LEVELS = [
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('doctorate', 'Doctorate'),
        ('certificate', 'Certificate')
    ]
    
    name = models.CharField(max_length=200)
    duration = models.CharField(max_length=50)
    description = models.TextField()
    entry_requirements = models.TextField()
    career_paths = models.TextField(default="Not specified", help_text="Comma-separated career options")
    subjects = models.TextField(default="Not specified", help_text="Comma-separated subject list")
    job_prospects = models.TextField(default="Not specified")
    salary_range = models.CharField(max_length=100)
    specializations = models.TextField(blank=True, help_text="Comma-separated specializations")
    industry_connections = models.TextField(blank=True, help_text="Comma-separated industry partners")
    level = models.CharField(max_length=20, choices=PROGRAM_LEVELS, default='undergraduate')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class CampusFacility(models.Model):
    FACILITY_TYPES = [
        ('library', 'Library'),
        ('laboratory', 'Laboratory'),
        ('hostel', 'Hostel'),
        ('sports', 'Sports Facility'),
        ('cafeteria', 'Cafeteria'),
        ('transport', 'Transportation'),
        ('other', 'Other')
    ]
    
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES)
    description = models.TextField()
    capacity = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    operating_hours = models.CharField(max_length=100, blank=True)
    contact_info = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_facility_type_display()})"

class AdmissionInfo(models.Model):
    academic_year = models.CharField(max_length=20)
    application_start_date = models.DateField()
    application_deadline = models.DateField()
    entrance_exam_date = models.DateField(null=True, blank=True)
    result_announcement_date = models.DateField(null=True, blank=True)
    admission_start_date = models.DateField(null=True, blank=True)
    application_fee = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField()
    documents_needed = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    office_hours = models.CharField(max_length=100)
    is_current = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Admission Information"
    
    def __str__(self):
        return f"Admission {self.academic_year}"

class Scholarship(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    eligibility_criteria = models.TextField()
    benefit_amount = models.CharField(max_length=100)
    benefit_type = models.CharField(max_length=50, choices=[
        ('tuition_reduction', 'Tuition Reduction'),
        ('full_tuition', 'Full Tuition Waiver'),
        ('stipend', 'Monthly Stipend'),
        ('other', 'Other Benefits')
    ])
    application_deadline = models.DateField(null=True, blank=True)
    application_process = models.TextField()
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UniversityFee(models.Model):
    FEE_TYPES = [
        ('tuition', 'Tuition Fee'),
        ('hostel', 'Hostel Fee'),
        ('application', 'Application Fee'),
        ('examination', 'Examination Fee'),
        ('library', 'Library Fee'),
        ('sports', 'Sports Fee'),
        ('other', 'Other Fees')
    ]
    
    fee_type = models.CharField(max_length=20, choices=FEE_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='MMK')
    academic_year = models.CharField(max_length=20)
    payment_schedule = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_fee_type_display()} - {self.amount} {self.currency}"

class StudentClub(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    club_type = models.CharField(max_length=50, choices=[
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('volunteer', 'Volunteer'),
        ('professional', 'Professional'),
        ('other', 'Other')
    ])
    advisor = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    meeting_schedule = models.CharField(max_length=200, blank=True)
    membership_requirements = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    established_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class UniversityEvent(models.Model):
    EVENT_TYPES = [
        ('academic', 'Academic'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('festival', 'Festival'),
        ('ceremony', 'Ceremony'),
        ('workshop', 'Workshop'),
        ('competition', 'Competition'),
        ('other', 'Other')
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.CharField(max_length=200, blank=True)
    registration_required = models.BooleanField(default=False)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    contact_info = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    max_participants = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.start_date.strftime('%Y-%m-%d')}"

class UniversityNews(models.Model):
    NEWS_CATEGORIES = [
        ('general', 'General'),
        ('academic', 'Academic'),
        ('events', 'Events'),
        ('facilities', 'Facilities'),
        ('achievements', 'Achievements'),
        ('announcements', 'Announcements'),
        ('entertainment', 'Entertainment')
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=NEWS_CATEGORIES)
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags")
    author = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)
    
    # Content policy fields
    content_approved = models.BooleanField(default=False)
    moderator_notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "University News"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class ContactInformation(models.Model):
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    office_location = models.CharField(max_length=200)
    office_hours = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.department} - {self.phone}"

class EngagementContent(models.Model):
    CONTENT_TYPES = [
        ('joke', 'Joke'),
        ('encouragement', 'Encouragement'),
        ('fun_fact', 'Fun Fact'),
        ('tip', 'Study Tip'),
        ('advice', 'Career Advice')
    ]
    
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    tone = models.CharField(max_length=50, blank=True)
    context = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_content_type_display()}: {self.content[:50]}..."
