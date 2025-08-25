"""
Data Manager for HMAWBI University Chatbot
Now integrated with Django models for admin panel management
"""

from typing import Dict, List, Any, Optional
import logging
import traceback

from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured

# Set up logging
logger = logging.getLogger(__name__)


class DataManager:
    """Centralized data management using Django models"""

    def __init__(self):
        # Fallback data for when models are not available
        self.fallback_data = {
            'programs': {
                'Civil Engineering': {
                    'duration': '5 years',
                    'description': 'Comprehensive civil engineering program',
                    'career_paths': ['Civil Engineer', 'Construction Manager'],
                    'entry_requirements': 'Matriculation with strong math and physics'
                }
            },
            'campus': {
                'location': 'Hmawbi Township, Yangon Region',
                'facilities': ['Library', 'Computer Lab', 'Hostel']
            },
            'admission': {
                'deadline': 'May 31st',
                'contact_email': 'admissions@hmawbi.edu.mm'
            },
            'university_info': {
                'General Information': 'HMAWBI University is a leading institution in Myanmar.',
                'Leadership': 'Rector: Dr. John Doe, Pro-Rector: Dr. Jane Smith',
                'Location & Transportation': 'Located in Hmawbi Township, accessible by Bus No. 45, 67'
            }
        }

    def _import_models(self):
        """Safely import Django models"""
        try:
            from chatbot.models import (UniversityProgram, CampusFacility,
                                        ContactInformation, AdmissionInfo,
                                        Scholarship, StudentClub, UniversityEvent,
                                        UniversityNews, UniversityInfo)
            return {
                'UniversityProgram': UniversityProgram,
                'CampusFacility': CampusFacility,
                'ContactInformation': ContactInformation,
                'AdmissionInfo': AdmissionInfo,
                'Scholarship': Scholarship,
                'StudentClub': StudentClub,
                'UniversityEvent': UniversityEvent,
                'UniversityNews': UniversityNews,
                'UniversityInfo': UniversityInfo
            }
        except (ImportError, ImproperlyConfigured) as e:
            logger.warning(f"Could not import Django models: {e}")
            return None

    def _get_display_value(self, instance, field_name: str) -> str:
        """Safely get display value for choice fields"""
        try:
            # Try to get the display method first
            display_method = getattr(instance, f'get_{field_name}_display', None)
            if display_method and callable(display_method):
                return display_method()

            # Fallback: try to get choices from the field and do manual lookup
            field_value = getattr(instance, field_name, None)
            if field_value:
                # Get field choices from model meta
                for field in instance._meta.fields:
                    if field.name == field_name and hasattr(field, 'choices'):
                        choices_dict = dict(field.choices)
                        return choices_dict.get(field_value, field_value)

            return str(field_value) if field_value else 'Unknown'
        except (AttributeError, TypeError):
            return str(getattr(instance, field_name, 'Unknown'))

    def get_program_info(self, program_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific program"""
        models = self._import_models()
        if not models:
            return self.fallback_data['programs'].get(program_name, {})

        try:
            UniversityProgram = models['UniversityProgram']
            program = UniversityProgram.objects.filter(
                name__icontains=program_name, is_active=True).first()

            if program:
                return {
                    'name': program.name,
                    'duration': program.duration,
                    'description': program.description,
                    'career_paths': [path.strip() for path in program.career_paths.split(',')],
                    'entry_requirements': program.entry_requirements,
                    'subjects': [subj.strip() for subj in program.subjects.split(',')],
                    'job_prospects': program.job_prospects,
                    'salary_range': program.salary_range,
                    'specializations': [
                        spec.strip()
                        for spec in program.specializations.split(',')
                        if spec.strip()
                    ]
                }
        except Exception as e:
            logger.error(f"Error getting program info for {program_name}: {e}")

        return self.fallback_data['programs'].get(program_name, {})

    def get_all_programs(self) -> Dict[str, Any]:
        """Get information about all active programs"""
        models = self._import_models()
        if not models:
            return self.fallback_data['programs']

        try:
            UniversityProgram = models['UniversityProgram']
            programs = UniversityProgram.objects.filter(is_active=True)
            result = {}

            for program in programs:
                result[program.name] = {
                    'duration': program.duration,
                    'description': program.description,
                    'career_paths': [path.strip() for path in program.career_paths.split(',')],
                    'entry_requirements': program.entry_requirements,
                    'subjects': [subj.strip() for subj in program.subjects.split(',')],
                    'job_prospects': program.job_prospects,
                    'salary_range': program.salary_range
                }
            return result
        except Exception as e:
            logger.error(f"Error getting all programs: {e}")
            return self.fallback_data['programs']

    def get_campus_info(self) -> Dict[str, Any]:
        """Get campus facilities information"""
        models = self._import_models()
        if not models:
            return self.fallback_data['campus']

        try:
            CampusFacility = models['CampusFacility']
            ContactInformation = models['ContactInformation']

            facilities = CampusFacility.objects.filter(is_available=True)
            contacts = ContactInformation.objects.filter(is_active=True)

            facilities_by_type = {}
            for facility in facilities:
                facility_type_display = self._get_display_value(facility, 'facility_type')

                if facility_type_display not in facilities_by_type:
                    facilities_by_type[facility_type_display] = []

                facility_info = facility.name
                if facility.capacity:
                    facility_info += f" ({facility.capacity})"
                facilities_by_type[facility_type_display].append(facility_info)

            contact_info = {}
            for contact in contacts:
                contact_info[contact.department] = {
                    'phone': contact.phone,
                    'email': contact.email,
                    'location': contact.office_location,
                    'hours': contact.office_hours
                }

            return {
                'location': 'Hmawbi Township, Yangon Region, Myanmar',
                'facilities': facilities_by_type,
                'contact': contact_info
            }
        except Exception as e:
            logger.error(f"Error getting campus info: {e}")
            return self.fallback_data['campus']

    def get_admission_info(self) -> Dict[str, Any]:
        """Get current admission information"""
        models = self._import_models()
        if not models:
            return self.fallback_data['admission']

        try:
            AdmissionInfo = models['AdmissionInfo']
            Scholarship = models['Scholarship']

            current_admission = AdmissionInfo.objects.filter(is_current=True).first()
            scholarships = Scholarship.objects.filter(is_active=True)

            result = {}

            if current_admission:
                result = {
                    'academic_year': current_admission.academic_year,
                    'application_deadline': current_admission.application_deadline.strftime('%B %d, %Y'),
                    'entrance_exam_date': (current_admission.entrance_exam_date.strftime('%B %d, %Y')
                                         if current_admission.entrance_exam_date else 'TBA'),
                    'requirements': current_admission.requirements,
                    'documents_needed': current_admission.documents_needed,
                    'contact_email': current_admission.contact_email,
                    'contact_phone': current_admission.contact_phone,
                    'office_hours': current_admission.office_hours,
                    'application_fee': f"{current_admission.application_fee} MMK"
                }

            # Add scholarships
            scholarship_list = []
            for scholarship in scholarships:
                scholarship_list.append({
                    'name': scholarship.name,
                    'criteria': scholarship.eligibility_criteria,
                    'benefit': scholarship.benefit_amount
                })
            result['scholarships'] = scholarship_list

            return result
        except Exception as e:
            logger.error(f"Error getting admission info: {e}")
            return self.fallback_data['admission']

    def get_scholarships(self) -> List[Dict[str, Any]]:
        """Get active scholarships"""
        models = self._import_models()
        if not models:
            return []

        try:
            Scholarship = models['Scholarship']
            scholarships = Scholarship.objects.filter(is_active=True)
            result = []
            for scholarship in scholarships:
                benefit_type_display = self._get_display_value(scholarship, 'benefit_type')

                result.append({
                    'name': scholarship.name,
                    'description': scholarship.description,
                    'criteria': scholarship.eligibility_criteria,
                    'benefit': scholarship.benefit_amount,
                    'benefit_type': benefit_type_display,
                    'deadline': (scholarship.application_deadline.strftime('%B %d, %Y')
                               if scholarship.application_deadline else 'No deadline specified'),
                    'application_process': scholarship.application_process
                })
            return result
        except Exception as e:
            logger.error(f"Error getting scholarships: {e}")
            return []

    def get_scholarship_info(self, scholarship_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific scholarship"""
        models = self._import_models()
        if not models:
            return {}

        try:
            Scholarship = models['Scholarship']
            scholarship = Scholarship.objects.filter(
                name__icontains=scholarship_name, is_active=True).first()

            if scholarship:
                benefit_type_display = self._get_display_value(scholarship, 'benefit_type')
                return {
                    'name': scholarship.name,
                    'description': scholarship.description,
                    'criteria': scholarship.eligibility_criteria,
                    'benefit': scholarship.benefit_amount,
                    'benefit_type': benefit_type_display,
                    'deadline': (scholarship.application_deadline.strftime('%B %d, %Y')
                               if scholarship.application_deadline else 'No deadline specified'),
                    'application_process': scholarship.application_process,
                    'contact_email': scholarship.contact_email if scholarship.contact_email else 'Contact financial aid office'
                }
        except Exception as e:
            logger.error(f"Error getting scholarship info for {scholarship_name}: {e}")

        return {}

    def get_student_life_info(self) -> Dict[str, Any]:
        """Get student life information"""
        models = self._import_models()
        default_result = {
            'clubs_organizations': ['Engineering Student Association', 'Computer Club', 'Drama Club'],
            'upcoming_events': []
        }

        if not models:
            return default_result

        try:
            StudentClub = models['StudentClub']
            UniversityEvent = models['UniversityEvent']

            clubs = StudentClub.objects.filter(is_active=True)
            upcoming_events = UniversityEvent.objects.filter(
                start_date__gte=timezone.now(),
                is_public=True).order_by('start_date')[:10]

            club_list = [club.name for club in clubs]
            event_list = []
            for event in upcoming_events:
                event_type_display = self._get_display_value(event, 'event_type')

                event_list.append({
                    'title': event.title,
                    'date': event.start_date.strftime('%B %d, %Y'),
                    'location': event.location,
                    'type': event_type_display
                })

            return {
                'clubs_organizations': club_list,
                'upcoming_events': event_list
            }
        except Exception as e:
            logger.error(f"Error getting student life info: {e}")
            return default_result

    def get_all_clubs(self) -> List[Dict[str, Any]]:
        """Get all active clubs"""
        models = self._import_models()
        if not models:
            return []

        try:
            StudentClub = models['StudentClub']
            clubs = StudentClub.objects.filter(is_active=True)
            result = []

            for club in clubs:
                club_type_display = self._get_display_value(club, 'club_type')
                result.append({
                    'name': club.name,
                    'description': club.description,
                    'club_type': club_type_display,
                    'advisor': club.advisor if club.advisor else 'TBA',
                    'contact_email': club.contact_email if club.contact_email else 'Contact student services',
                    'meeting_schedule': club.meeting_schedule if club.meeting_schedule else 'TBA',
                    'membership_requirements': club.membership_requirements if club.membership_requirements else 'Open to all students',
                    'established_date': club.established_date.strftime('%Y') if club.established_date else 'N/A'
                })

            return result
        except Exception as e:
            logger.error(f"Error getting all clubs: {e}")
            return []

    def get_club_info(self, club_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific club"""
        models = self._import_models()
        if not models:
            return {}

        try:
            StudentClub = models['StudentClub']
            club = StudentClub.objects.filter(
                name__icontains=club_name, is_active=True).first()

            if club:
                club_type_display = self._get_display_value(club, 'club_type')
                return {
                    'name': club.name,
                    'description': club.description,
                    'club_type': club_type_display,
                    'advisor': club.advisor if club.advisor else 'TBA',
                    'contact_email': club.contact_email if club.contact_email else 'Contact student services',
                    'meeting_schedule': club.meeting_schedule if club.meeting_schedule else 'TBA',
                    'membership_requirements': club.membership_requirements if club.membership_requirements else 'Open to all students',
                    'established_date': club.established_date.strftime('%Y') if club.established_date else 'N/A'
                }
        except Exception as e:
            logger.error(f"Error getting club info for {club_name}: {e}")

        return {}

    def get_all_events(self) -> List[Dict[str, Any]]:
        """Get all upcoming events"""
        models = self._import_models()
        if not models:
            return []

        try:
            UniversityEvent = models['UniversityEvent']
            # Fetch events that start from now onwards
            events = UniversityEvent.objects.filter(
                start_date__gte=timezone.now(),
                is_public=True).order_by('start_date')

            result = []
            for event in events:
                event_type_display = self._get_display_value(event, 'event_type')
                result.append({
                    'title': event.title,
                    'description': event.description,
                    'event_type': event_type_display,
                    'start_date': event.start_date.strftime('%B %d, %Y at %I:%M %p'),
                    'end_date': event.end_date.strftime('%B %d, %Y at %I:%M %p'),
                    'location': event.location,
                    'organizer': event.organizer if event.organizer else 'University',
                    'registration_required': event.registration_required,
                    'registration_deadline': (event.registration_deadline.strftime('%B %d, %Y')
                                            if event.registration_deadline else 'N/A'),
                    'contact_info': event.contact_info if event.contact_info else 'Contact event organizer',
                    'max_participants': event.max_participants if event.max_participants else 'No limit'
                })

            return result
        except Exception as e:
            logger.error(f"Error getting all events: {e}")
            # Return empty list on error to prevent crashing the chatbot
            return []

    # Add this method
    def get_past_events(self, num_events: int) -> List[Dict[str, Any]]:
        """Get the last N past events that are public"""
        models = self._import_models()
        if not models:
            return []

        try:
            UniversityEvent = models['UniversityEvent']
            # Fetch events that ended before now
            events = UniversityEvent.objects.filter(
                end_date__lt=timezone.now(), # Event has already ended
                is_public=True).order_by('-end_date') # Order by end date descending (most recent first)
            
            # Limit the queryset to the desired number of events
            events = events[:num_events] 

            result = []
            for event in events:
                event_type_display = self._get_display_value(event, 'event_type')
                result.append({
                    'title': event.title,
                    'description': event.description,
                    'event_type': event_type_display,
                    'start_date': event.start_date.strftime('%B %d, %Y at %I:%M %p'),
                    'end_date': event.end_date.strftime('%B %d, %Y at %I:%M %p'), # Keep end date for context
                    'location': event.location,
                    'organizer': event.organizer if event.organizer else 'University',
                    'registration_required': event.registration_required,
                    'registration_deadline': (event.registration_deadline.strftime('%B %d, %Y')
                                            if event.registration_deadline else 'N/A'),
                    'contact_info': event.contact_info if event.contact_info else 'Contact event organizer',
                    'max_participants': event.max_participants if event.max_participants else 'No limit'
                })

            return result
        except Exception as e:
            logger.error(f"Error getting past events: {e}")
            # Return empty list on error to prevent crashing the chatbot
            return []

    def get_event_info(self, event_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific event"""
        models = self._import_models()
        if not models:
            return {}

        try:
            UniversityEvent = models['UniversityEvent']
            # NOTE: This method currently only finds upcoming events.
            # If you want it to find past events too, you'd need to adjust the filter.
            event = UniversityEvent.objects.filter(
                title__icontains=event_name,
                start_date__gte=timezone.now(), # Currently only looks for upcoming events
                is_public=True).first()

            if event:
                event_type_display = self._get_display_value(event, 'event_type')
                return {
                    'title': event.title,
                    'description': event.description,
                    'event_type': event_type_display,
                    'start_date': event.start_date.strftime('%B %d, %Y at %I:%M %p'),
                    'end_date': event.end_date.strftime('%B %d, %Y at %I:%M %p'),
                    'location': event.location,
                    'organizer': event.organizer if event.organizer else 'University',
                    'registration_required': event.registration_required,
                    'registration_deadline': (event.registration_deadline.strftime('%B %d, %Y')
                                            if event.registration_deadline else 'N/A'),
                    'contact_info': event.contact_info if event.contact_info else 'Contact event organizer',
                    'max_participants': event.max_participants if event.max_participants else 'No limit'
                }
        except Exception as e:
            logger.error(f"Error getting event info for {event_name}: {e}")

        return {}

    def get_latest_news(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get latest approved university news"""
        models = self._import_models()
        default_result = [{
            'title': 'Welcome to HMAWBI University',
            'content': 'New academic year has started with exciting opportunities',
            'category': 'General',
            'date': '2024-01-15',
            'tags': []
        }]

        if not models:
            return default_result

        try:
            UniversityNews = models['UniversityNews']
            news_items = UniversityNews.objects.filter(
                is_published=True,
                content_approved=True).order_by('-created_at')[:limit]

            result = []
            for news in news_items:
                tags_list = []
                if news.tags:
                    tags_list = [tag.strip() for tag in news.tags.split(',') if tag.strip()]

                category_display = self._get_display_value(news, 'category')

                result.append({
                    'id': news.pk,
                    'title': news.title,
                    'content': news.content,
                    'category': category_display,
                    'date': news.created_at.strftime('%Y-%m-%d'),
                    'tags': tags_list
                })
            return result
        except Exception as e:
            logger.error(f"Error getting latest news: {e}")
            return default_result

    def get_news_info(self, news_title: str) -> Dict[str, Any]:
        """Get detailed information about a specific news item"""
        models = self._import_models()
        if not models:
            return {}

        try:
            UniversityNews = models['UniversityNews']
            news = UniversityNews.objects.filter(
                title__icontains=news_title,
                is_published=True,
                content_approved=True).first()

            if news:
                tags_list = []
                if news.tags:
                    tags_list = [tag.strip() for tag in news.tags.split(',') if tag.strip()]

                category_display = self._get_display_value(news, 'category')

                return {
                    'id': news.pk,
                    'title': news.title,
                    'content': news.content,
                    'category': category_display,
                    'date': news.created_at.strftime('%Y-%m-%d'),
                    'tags': tags_list,
                    'author': news.author if news.author else 'HMAWBI University'
                }
        except Exception as e:
            logger.error(f"Error getting news info for {news_title}: {e}")

        return {}

    def search_university_news(self, keyword: str) -> List[Dict[str, Any]]:
        """Search university news by keyword"""
        models = self._import_models()
        if not models:
            logger.warning("Models not available, returning empty list")
            return []

        try:
            UniversityNews = models['UniversityNews']

            # Create a more robust query
            from django.db.models import Q

            # Build the search query
            search_query = Q(title__icontains=keyword,
                             is_published=True,
                             content_approved=True) | Q(
                                 content__icontains=keyword,
                                 is_published=True,
                                 content_approved=True) | Q(
                                     tags__icontains=keyword,
                                     is_published=True,
                                     content_approved=True)

            news_items = UniversityNews.objects.filter(search_query).distinct()

            logger.info(f"Found {news_items.count()} news items for keyword: {keyword}")

            result = []
            for news in news_items:
                try:
                    # Handle tags more safely
                    tags_list = []
                    if hasattr(news, 'tags') and news.tags:
                        tags_list = [
                            tag.strip() for tag in str(news.tags).split(',')
                            if tag.strip()
                        ]

                    # Safe handling of get_category_display
                    category_display = self._get_display_value(news, 'category')

                    result.append({
                        'id': news.pk,
                        'title': str(news.title) if news.title else 'Untitled',
                        'content': str(news.content) if news.content else 'No content available',
                        'category': category_display,
                        'date': news.created_at.strftime('%Y-%m-%d') if hasattr(
                            news, 'created_at') else 'Unknown date',
                        'tags': tags_list
                    })

                except Exception as item_error:
                    logger.error(f"Error processing news item {news.pk}: {item_error}")
                    continue

            logger.info(f"Successfully processed {len(result)} news items")
            return result

        except Exception as e:
            logger.error(f"Error searching university news for '{keyword}': {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return []

    def get_contact_info(self, department: Optional[str] = None) -> Dict[str, Any]:
        """Get contact information for departments"""
        models = self._import_models()
        default_contact = {
            'phone': '+95-1-234567',
            'email': 'info@hmawbi.edu.mm',
            'teacher': 'Dr.MayCho',
            'office_hours': 'Monday-Friday 9AM-4PM',
            'description': 'University Information'
        }

        if not models:
            return default_contact

        try:
            ContactInformation = models['ContactInformation']

            if department:
                contact = ContactInformation.objects.filter(
                    department__icontains=department, is_active=True).first()
                if contact:
                    return {
                        'department': contact.department,
                        'phone': contact.phone,
                        'email': contact.email,
                        'teacher': contact.teacher,
                        'location': contact.office_location,
                        'hours': contact.office_hours,
                        'description': contact.description if contact.description else 'Not specified'
                    }
                return default_contact
            else:
                contacts = ContactInformation.objects.filter(is_active=True)
                result = {}
                for contact in contacts:
                    result[contact.department] = {
                        'phone': contact.phone,
                        'email': contact.email,
                        'teacher': contact.teacher,
                        'location': contact.office_location,
                        'hours': contact.office_hours,
                        'description': contact.description if contact.description else 'Not specified'
                    }
                return result if result else default_contact
        except Exception as e:
            logger.error(f"Error getting contact info: {e}")
            return default_contact

    def get_university_info(self, info_type: Optional[str] = None) -> Dict[str, Any]:
        """Get university information"""
        models = self._import_models()
        if not models:
            return self.fallback_data['university_info']

        try:
            UniversityInfo = models['UniversityInfo']

            if info_type:
                info_item = UniversityInfo.objects.filter(
                    info_type__icontains=info_type, is_active=True).first()
                if info_item:
                    info_type_display = self._get_display_value(info_item, 'info_type')
                    return {
                        'title': info_item.title,
                        'info_type': info_type_display,
                        'content': info_item.content,
                        'description': info_item.description if info_item.description else 'Not specified'
                    }
                return {}
            else:
                info_items = UniversityInfo.objects.filter(is_active=True)
                result = {}
                for info in info_items:
                    info_type_display = self._get_display_value(info, 'info_type')
                    result[info_type_display] = {
                        'title': info.title,
                        'content': info.content,
                        'description': info.description if info.description else 'Not specified'
                    }
                return result if result else self.fallback_data['university_info']
        except Exception as e:
            logger.error(f"Error getting university info: {e}")
            return self.fallback_data['university_info']

    def search_programs(self, query: str) -> List[str]:
        """Search programs by keyword"""
        models = self._import_models()
        if not models:
            return []

        try:
            UniversityProgram = models['UniversityProgram']
            programs = UniversityProgram.objects.filter(
                name__icontains=query,
                is_active=True) | UniversityProgram.objects.filter(
                    description__icontains=query,
                    is_active=True) | UniversityProgram.objects.filter(
                        career_paths__icontains=query, is_active=True)

            return [program.name for program in programs.distinct()]
        except Exception as e:
            logger.error(f"Error searching programs: {e}")
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the university data"""
        models = self._import_models()
        default_stats = {
            'total_programs': 4,
            'total_facilities': 8,
            'total_scholarships': 2,
            'student_clubs': 7,
            'upcoming_events': 3,
            'published_news': 5
        }

        if not models:
            return default_stats

        try:
            stats = {
                'total_programs': models['UniversityProgram'].objects.filter(is_active=True).count(),
                'total_facilities': models['CampusFacility'].objects.filter(is_available=True).count(),
                'total_scholarships': models['Scholarship'].objects.filter(is_active=True).count(),
                'student_clubs': models['StudentClub'].objects.filter(is_active=True).count(),
                'upcoming_events': models['UniversityEvent'].objects.filter(
                    start_date__gte=timezone.now(), is_public=True).count(),
                'published_news': models['UniversityNews'].objects.filter(
                    is_published=True, content_approved=True).count()
            }

            return stats

        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return default_stats


# Convenience functions for testing
def test_data_manager():
    """Test function for development"""
    manager = DataManager()

    print("Programs:", list(manager.get_all_programs().keys()))
    print("Campus Info:", manager.get_campus_info())
    print("Statistics:", manager.get_statistics())


if __name__ == "__main__":
    test_data_manager()