"""
Data Manager for HMAWBI University Chatbot
Now integrated with Django models for admin panel management
"""

import json
import os
from typing import Dict, List, Any, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

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
                'fees': {'tuition': '150,000 MMK per year'},
                'contact_email': 'admissions@hmawbi.edu.mm'
            }
        }

    def get_program_info(self, program_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific program"""
        try:
            from .models import UniversityProgram
            program = UniversityProgram.objects.filter(
                name__icontains=program_name, 
                is_active=True
            ).first()

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
                    'specializations': [spec.strip() for spec in program.specializations.split(',') if spec.strip()]
                }
        except:
            pass

        return self.fallback_data['programs'].get(program_name, {})

    def get_all_programs(self) -> Dict[str, Any]:
        """Get information about all active programs"""
        try:
            from .models import UniversityProgram
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
        except:
            return self.fallback_data['programs']

    def get_campus_info(self) -> Dict[str, Any]:
        """Get campus facilities information"""
        try:
            from .models import CampusFacility, ContactInformation
            facilities = CampusFacility.objects.filter(is_available=True)
            contacts = ContactInformation.objects.filter(is_active=True)

            facilities_by_type = {}
            for facility in facilities:
                facility_type = facility.facility_type
                if facility_type not in facilities_by_type:
                    facilities_by_type[facility_type] = []

                facility_info = facility.name
                if facility.capacity:
                    facility_info += f" ({facility.capacity})"
                facilities_by_type[facility_type].append(facility_info)

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
        except:
            return self.fallback_data['campus']

    def get_admission_info(self) -> Dict[str, Any]:
        """Get current admission information"""
        try:
            from .models import AdmissionInfo, Scholarship, UniversityFee

            current_admission = AdmissionInfo.objects.filter(is_current=True).first()
            scholarships = Scholarship.objects.filter(is_active=True)
            current_fees = UniversityFee.objects.filter(is_current=True)

            result = {}

            if current_admission:
                result = {
                    'academic_year': current_admission.academic_year,
                    'application_deadline': current_admission.application_deadline.strftime('%B %d, %Y'),
                    'entrance_exam_date': current_admission.entrance_exam_date.strftime('%B %d, %Y') if current_admission.entrance_exam_date else 'TBA',
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

            # Add fees
            fees = {}
            for fee in current_fees:
                fees[fee.fee_type] = f"{fee.amount} {fee.currency}"
            result['fees'] = fees

            return result
        except Exception as e:
            print(f"Error getting admission info: {e}")
            return self.fallback_data['admission']

    def get_scholarships(self) -> List[Dict[str, Any]]:
        """Get active scholarships"""
        try:
            from .models import Scholarship

            scholarships = Scholarship.objects.filter(is_active=True)
            result = []
            for scholarship in scholarships:
                result.append({
                    'name': scholarship.name,
                    'description': scholarship.description,
                    'criteria': scholarship.eligibility_criteria,
                    'benefit': scholarship.benefit_amount,
                    'benefit_type': scholarship.get_benefit_type_display(),
                    'deadline': scholarship.application_deadline.strftime('%B %d, %Y') if scholarship.application_deadline else 'No deadline specified',
                    'application_process': scholarship.application_process
                })
            return result
        except Exception as e:
            print(f"Error getting scholarships: {e}")
            return []

    def get_student_life_info(self) -> Dict[str, Any]:
        """Get student life information"""
        try:
            from .models import StudentClub, UniversityEvent

            clubs = StudentClub.objects.filter(is_active=True)
            upcoming_events = UniversityEvent.objects.filter(
                start_date__gte=timezone.now(),
                is_public=True
            ).order_by('start_date')[:10]

            club_list = [club.name for club in clubs]
            event_list = []
            for event in upcoming_events:
                event_list.append({
                    'title': event.title,
                    'date': event.start_date.strftime('%B %d, %Y'),
                    'location': event.location,
                    'type': event.get_event_type_display()
                })

            return {
                'clubs_organizations': club_list,
                'upcoming_events': event_list
            }
        except:
            return {
                'clubs_organizations': ['Engineering Student Association', 'Computer Club', 'Drama Club'],
                'upcoming_events': []
            }

    def get_latest_news(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get latest approved university news"""
        try:
            from .models import UniversityNews

            news_items = UniversityNews.objects.filter(
                is_published=True,
                content_approved=True
            ).order_by('-created_at')[:limit]

            result = []
            for news in news_items:
                result.append({
                    'id': news.id,
                    'title': news.title,
                    'content': news.content,
                    'category': news.get_category_display(),
                    'date': news.created_at.strftime('%Y-%m-%d'),
                    'tags': [tag.strip() for tag in news.tags.split(',') if tag.strip()]
                })
            return result
        except:
            return [
                {
                    'title': 'Welcome to HMAWBI University',
                    'content': 'New academic year has started with exciting opportunities',
                    'category': 'General',
                    'date': '2024-01-15'
                }
            ]

    def search_programs(self, query: str) -> List[str]:
        """Search programs by keyword"""
        try:
            from .models import UniversityProgram

            programs = UniversityProgram.objects.filter(
                name__icontains=query,
                is_active=True
            ) | UniversityProgram.objects.filter(
                description__icontains=query,
                is_active=True
            ) | UniversityProgram.objects.filter(
                career_paths__icontains=query,
                is_active=True
            )

            return [program.name for program in programs.distinct()]
        except:
            return []

    def get_engagement_content(self, content_type: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Get engagement content (jokes, encouragement, etc.)"""
        try:
            from .models import EngagementContent

            content = EngagementContent.objects.filter(
                content_type=content_type,
                is_active=True
            ).order_by('?')[:limit]  # Random order

            result = []
            for item in content:
                content_data = {
                    'content': item.content,
                    'category': item.category
                }
                if item.title:
                    content_data['title'] = item.title
                if item.tone:
                    content_data['tone'] = item.tone
                if item.context:
                    content_data['context'] = item.context

                result.append(content_data)
            return result
        except:
            # Fallback content
            if content_type == 'joke':
                return [
                    {
                        'setup': 'Why did the engineering student bring a ladder to class?',
                        'punchline': 'Because they heard the course was on the next level!',
                        'category': 'academic'
                    }
                ]
            elif content_type == 'encouragement':
                return [
                    {
                        'message': 'Every expert was once a beginner. Keep pushing forward!',
                        'tone': 'encouraging'
                    }
                ]
            elif content_type == 'fun_fact':
                return [
                    {
                        'content': 'HMAWBI University was the first technological university in Yangon Region'
                    }
                ]
            return []

    def search_university_news(self, keyword: str) -> List[Dict[str, Any]]:
        """Search university news by keyword"""
        try:
            from .models import UniversityNews

            news_items = UniversityNews.objects.filter(
                title__icontains=keyword,
                is_published=True,
                content_approved=True
            ) | UniversityNews.objects.filter(
                content__icontains=keyword,
                is_published=True,
                content_approved=True
            ) | UniversityNews.objects.filter(
                tags__icontains=keyword,
                is_published=True,
                content_approved=True
            )

            result = []
            for news in news_items.distinct():
                result.append({
                    'id': news.id,
                    'title': news.title,
                    'content': news.content,
                    'category': news.get_category_display(),
                    'date': news.created_at.strftime('%Y-%m-%d'),
                    'tags': [tag.strip() for tag in news.tags.split(',') if tag.strip()]
                })
            return result
        except:
            return []

    def get_contact_info(self, department: str = None) -> Dict[str, Any]:
        """Get contact information for departments"""
        try:
            from .models import ContactInformation

            if department:
                contact = ContactInformation.objects.filter(
                    department__icontains=department,
                    is_active=True
                ).first()
                if contact:
                    return {
                        'department': contact.department,
                        'phone': contact.phone,
                        'email': contact.email,
                        'location': contact.office_location,
                        'hours': contact.office_hours
                    }
            else:
                contacts = ContactInformation.objects.filter(is_active=True)
                result = {}
                for contact in contacts:
                    result[contact.department] = {
                        'phone': contact.phone,
                        'email': contact.email,
                        'location': contact.office_location,
                        'hours': contact.office_hours
                    }
                return result
        except:
            return {
                'phone': '+95-1-234567',
                'email': 'info@hmawbi.edu.mm',
                'office_hours': 'Monday-Friday 9AM-4PM'
            }

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the university data"""
        try:
            from .models import (
                UniversityProgram, CampusFacility, Scholarship, 
                StudentClub, UniversityEvent, UniversityNews, EngagementContent
            )

            return {
                'total_programs': UniversityProgram.objects.filter(is_active=True).count(),
                'total_facilities': CampusFacility.objects.filter(is_available=True).count(),
                'total_scholarships': Scholarship.objects.filter(is_active=True).count(),
                'student_clubs': StudentClub.objects.filter(is_active=True).count(),
                'upcoming_events': UniversityEvent.objects.filter(
                    start_date__gte=timezone.now(),
                    is_public=True
                ).count(),
                'published_news': UniversityNews.objects.filter(
                    is_published=True,
                    content_approved=True
                ).count(),
                'engagement_content': EngagementContent.objects.filter(is_active=True).count()
            }
        except:
            return {
                'total_programs': 4,
                'total_facilities': 8,
                'total_scholarships': 2,
                'student_clubs': 7,
                'upcoming_events': 3,
                'published_news': 5,
                'engagement_content': 10
            }


# Convenience functions for testing
def test_data_manager():
    """Test function for development"""
    manager = DataManager()

    print("Programs:", list(manager.get_all_programs().keys()))
    print("Campus Info:", manager.get_campus_info())
    print("Statistics:", manager.get_statistics())

if __name__ == "__main__":
    test_data_manager()