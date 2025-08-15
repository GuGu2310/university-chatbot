
from django.contrib import admin
from .models import (
    UserProfile, Conversation, Message, UniversityProgram, 
    CampusFacility, AdmissionInfo, Scholarship, UniversityFee,
    StudentClub, UniversityEvent, UniversityNews, ContactInformation,
    EngagementContent
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
    list_display = ['name', 'level', 'duration', 'is_active', 'created_at']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'career_paths']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'level', 'duration', 'description', 'is_active')
        }),
        ('Requirements & Curriculum', {
            'fields': ('entry_requirements', 'subjects', 'specializations')
        }),
        ('Career Information', {
            'fields': ('career_paths', 'job_prospects', 'salary_range', 'industry_connections')
        }),
    )

@admin.register(CampusFacility)
class CampusFacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'facility_type', 'capacity', 'is_available']
    list_filter = ['facility_type', 'is_available']
    search_fields = ['name', 'description', 'location']

@admin.register(AdmissionInfo)
class AdmissionInfoAdmin(admin.ModelAdmin):
    list_display = ['academic_year', 'application_deadline', 'entrance_exam_date', 'is_current']
    list_filter = ['is_current', 'application_start_date']
    fieldsets = (
        ('Academic Year', {
            'fields': ('academic_year', 'is_current')
        }),
        ('Important Dates', {
            'fields': ('application_start_date', 'application_deadline', 'entrance_exam_date', 
                      'result_announcement_date', 'admission_start_date')
        }),
        ('Requirements', {
            'fields': ('application_fee', 'requirements', 'documents_needed')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'office_hours')
        }),
    )

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'benefit_type', 'application_deadline', 'is_active']
    list_filter = ['benefit_type', 'is_active', 'application_deadline']
    search_fields = ['name', 'description', 'eligibility_criteria']

@admin.register(UniversityFee)
class UniversityFeeAdmin(admin.ModelAdmin):
    list_display = ['fee_type', 'amount', 'currency', 'academic_year', 'is_current']
    list_filter = ['fee_type', 'academic_year', 'is_current']
    search_fields = ['fee_type', 'academic_year']

@admin.register(StudentClub)
class StudentClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'club_type', 'advisor', 'is_active']
    list_filter = ['club_type', 'is_active', 'established_date']
    search_fields = ['name', 'description', 'advisor']

@admin.register(UniversityEvent)
class UniversityEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'location', 'is_public']
    list_filter = ['event_type', 'is_public', 'registration_required', 'start_date']
    search_fields = ['title', 'description', 'location', 'organizer']
    date_hierarchy = 'start_date'

@admin.register(UniversityNews)
class UniversityNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'content_approved', 'is_published', 'is_featured', 'created_at']
    list_filter = ['category', 'content_approved', 'is_published', 'is_featured', 'created_at']
    search_fields = ['title', 'content', 'tags', 'author']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'category', 'tags', 'author')
        }),
        ('Publishing', {
            'fields': ('is_published', 'is_featured', 'published_date')
        }),
        ('Content Moderation', {
            'fields': ('content_approved', 'moderator_notes'),
            'description': 'Content must be approved before being visible to users'
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Auto-approve appropriate content, require manual approval for sensitive content
        inappropriate_keywords = [
            'prettiest', 'ugliest', 'worst teacher', 'best looking', 'hottest',
            'ranking students', 'ranking staff', 'personal appearance'
        ]
        
        content_text = (obj.title + " " + obj.content).lower()
        if any(keyword in content_text for keyword in inappropriate_keywords):
            obj.content_approved = False
            obj.moderator_notes = "Requires manual review due to potentially inappropriate content"
        else:
            obj.content_approved = True
            
        super().save_model(request, obj, form, change)

@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ['department', 'phone', 'email', 'office_location', 'is_active']
    list_filter = ['is_active']
    search_fields = ['department', 'phone', 'email', 'office_location']

@admin.register(EngagementContent)
class EngagementContentAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'title', 'content_preview', 'category', 'is_active', 'created_at']
    list_filter = ['content_type', 'category', 'tone', 'is_active', 'created_at']
    search_fields = ['title', 'content', 'category']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'

# Admin site customization
admin.site.site_header = "HMAWBI University Chatbot Administration"
admin.site.site_title = "HMAWBI Admin"
admin.site.index_title = "University Guidance System Administration"
