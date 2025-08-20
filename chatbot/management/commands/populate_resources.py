"""
Django management command for populating university data
Usage: python manage.py populate_resources
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.management.color import Style
from datetime import datetime, timedelta
from chatbot.models import (UniversityProgram, CampusFacility, AdmissionInfo,
                            Scholarship, UniversityFee, StudentClub,
                            UniversityEvent, UniversityNews,
                            ContactInformation, EngagementContent)


class Command(BaseCommand):
    help = 'Populate the database with sample university guidance data'

    def handle(self, *args, **options):
        self.stdout.write('Populating university guidance data...')

        # Create university programs
        self.create_programs()

        # Create campus facilities
        self.create_facilities()

        # Create admission information
        self.create_admission_info()

        # Create scholarships
        self.create_scholarships()

        # Create fees
        self.create_fees()

        # Create student clubs
        self.create_clubs()

        # Create events
        self.create_events()

        # Create news
        self.create_news()

        # Create contact information
        self.create_contacts()

        # Create engagement content
        self.create_engagement_content()

        self.stdout.write(
            Style().SUCCESS('Successfully populated university data!'))

    def create_programs(self):
        """Create university programs"""
        programs_data = [{
            'name': 'Civil Engineering',
            'duration': '5 years',
            'description':
            'Comprehensive program covering structural design, construction management, and infrastructure development for Myanmar\'s growing cities.',
            'entry_requirements':
            'Matriculation exam with strong physics and mathematics scores',
            'career_paths':
            'Civil Engineer, Construction Manager, Infrastructure Planner, Government Engineer',
            'subjects':
            'Structural Engineering, Construction Management, Hydraulics, Surveying, Materials Science',
            'job_prospects':
            'High demand in construction and infrastructure development',
            'salary_range': '800,000 - 2,500,000 MMK per month',
            'specializations':
            'Structural Engineering, Transportation Engineering, Water Resources',
            'industry_connections':
            'Myanmar Construction Association, Public Works Department',
            'level': 'undergraduate'
        }, {
            'name': 'Computer Engineering',
            'duration': '5 years',
            'description':
            'Advanced program combining hardware and software engineering for Myanmar\'s digital transformation.',
            'entry_requirements':
            'Matriculation exam with strong mathematics and physics, basic computer literacy',
            'career_paths':
            'Software Engineer, Systems Analyst, IT Manager, Technology Consultant',
            'subjects':
            'Programming, Computer Networks, Database Systems, Software Engineering, AI & Machine Learning',
            'job_prospects':
            'Excellent opportunities in tech industry and government IT',
            'salary_range': '1,000,000 - 3,500,000 MMK per month',
            'specializations':
            'Software Development, Network Engineering, Cybersecurity',
            'industry_connections':
            'Myanmar Computer Federation, Tech companies in Yangon',
            'level': 'undergraduate'
        }, {
            'name': 'Electrical Engineering',
            'duration': '5 years',
            'description':
            'Comprehensive electrical engineering program focusing on power systems, electronics, and renewable energy for Myanmar.',
            'entry_requirements':
            'Matriculation exam with excellent physics and mathematics scores',
            'career_paths':
            'Electrical Engineer, Power Systems Engineer, Electronics Designer, Renewable Energy Specialist',
            'subjects':
            'Circuit Analysis, Power Systems, Electronics, Control Systems, Renewable Energy',
            'job_prospects':
            'Growing opportunities in power generation and renewable energy',
            'salary_range': '900,000 - 3,000,000 MMK per month',
            'specializations': 'Power Systems, Electronics, Renewable Energy',
            'industry_connections':
            'Ministry of Electric Power, Renewable Energy Companies',
            'level': 'undergraduate'
        }, {
            'name': 'Mechanical Engineering',
            'duration': '5 years',
            'description':
            'Engineering program covering manufacturing, automotive, and industrial systems for Myanmar\'s industrial development.',
            'entry_requirements':
            'Matriculation exam with strong physics, mathematics, and chemistry scores',
            'career_paths':
            'Mechanical Engineer, Manufacturing Engineer, Industrial Designer, Automotive Engineer',
            'subjects':
            'Thermodynamics, Fluid Mechanics, Manufacturing Processes, Machine Design, Automotive Engineering',
            'job_prospects':
            'Strong demand in manufacturing and automotive sectors',
            'salary_range': '850,000 - 2,800,000 MMK per month',
            'specializations': 'Manufacturing, Automotive, Industrial Design',
            'industry_connections':
            'Myanmar Industries Association, Automotive Companies',
            'level': 'undergraduate'
        }]

        for program_data in programs_data:
            program, created = UniversityProgram.objects.get_or_create(  # type: ignore
                name=program_data['name'],
                defaults=program_data)
            if created:
                self.stdout.write(f'Created program: {program.name}')

    def create_facilities(self):
        """Create campus facilities"""
        facilities_data = [
            {
                'name': 'Central Library',
                'facility_type': 'library',
                'description': 'Main university library with 50,000+ books',
                'capacity': '200 seats'
            },
            {
                'name': 'Computer Laboratory',
                'facility_type': 'laboratory',
                'description': 'State-of-the-art computer lab',
                'capacity': '50 workstations'
            },
            {
                'name': 'Male Hostel',
                'facility_type': 'hostel',
                'description': 'On-campus accommodation for male students',
                'capacity': '500 students'
            },
            {
                'name': 'Female Hostel',
                'facility_type': 'hostel',
                'description': 'On-campus accommodation for female students',
                'capacity': '300 students'
            },
            {
                'name': 'Main Cafeteria',
                'facility_type': 'cafeteria',
                'description': 'Primary dining facility',
                'capacity': '400 seats'
            },
            {
                'name': 'Sports Complex',
                'facility_type': 'sports',
                'description': 'Multi-purpose sports facility',
                'capacity': '1000 spectators'
            },
            {
                'name': 'University Bus Service',
                'facility_type': 'transport',
                'description': 'Transportation to Yangon city center',
                'capacity': '5 buses'
            },
        ]

        for facility_data in facilities_data:
            facility, created = CampusFacility.objects.get_or_create(  # type: ignore
                name=facility_data['name'],
                defaults=facility_data)
            if created:
                self.stdout.write(f'Created facility: {facility.name}')

    def create_admission_info(self):
        """Create admission information"""
        admission_data = {
            'academic_year': '2024-2025',
            'application_start_date': datetime(2024, 3, 1).date(),
            'application_deadline': datetime(2024, 5, 31).date(),
            'entrance_exam_date': datetime(2024, 6, 15).date(),
            'result_announcement_date': datetime(2024, 7, 15).date(),
            'admission_start_date': datetime(2024, 8, 1).date(),
            'application_fee': 10000,
            'requirements':
            'Matriculation exam pass with minimum 60% overall score',
            'documents_needed':
            'Matriculation certificate, Birth certificate, ID card copy, Passport photos',
            'contact_email': 'admissions@hmawbi.edu.mm',
            'contact_phone': '+95-1-234567',
            'office_hours': 'Monday-Friday 9AM-4PM',
            'is_current': True
        }

        admission, created = AdmissionInfo.objects.get_or_create(  # type: ignore
            academic_year=admission_data['academic_year'],
            defaults=admission_data)
        if created:
            self.stdout.write(
                f'Created admission info: {admission.academic_year}')

    def create_scholarships(self):
        """Create scholarships"""
        scholarships_data = [{
            'name':
            'Merit Scholarship',
            'description':
            'For academically excellent students',
            'eligibility_criteria':
            'Top 10% of entrance exam scores',
            'benefit_amount':
            '50% tuition reduction',
            'benefit_type':
            'tuition_reduction',
            'application_deadline':
            datetime(2024, 6, 1).date(),
            'application_process':
            'Automatic consideration based on entrance exam results'
        }, {
            'name':
            'Need-based Scholarship',
            'description':
            'For students from low-income families',
            'eligibility_criteria':
            'Family income below 500,000 MMK per month',
            'benefit_amount':
            'Full tuition waiver',
            'benefit_type':
            'full_tuition',
            'application_deadline':
            datetime(2024, 6, 15).date(),
            'application_process':
            'Submit income documents and application form'
        }]

        for scholarship_data in scholarships_data:
            scholarship, created = Scholarship.objects.get_or_create(  # type: ignore
                name=scholarship_data['name'],
                defaults=scholarship_data)
            if created:
                self.stdout.write(f'Created scholarship: {scholarship.name}')

    def create_fees(self):
        """Create university fees"""
        fees_data = [
            {
                'fee_type': 'tuition',
                'amount': 150000,
                'academic_year': '2024-2025'
            },
            {
                'fee_type': 'application',
                'amount': 10000,
                'academic_year': '2024-2025'
            },
            {
                'fee_type': 'hostel',
                'amount': 80000,
                'academic_year': '2024-2025'
            },
            {
                'fee_type': 'library',
                'amount': 15000,
                'academic_year': '2024-2025'
            },
            {
                'fee_type': 'sports',
                'amount': 10000,
                'academic_year': '2024-2025'
            },
        ]

        for fee_data in fees_data:
            fee, created = UniversityFee.objects.get_or_create(  # type: ignore
                fee_type=fee_data['fee_type'],
                academic_year=fee_data['academic_year'],
                defaults=fee_data)
            if created:
                self.stdout.write(f'Created fee: {fee.get_fee_type_display()}')

    def create_clubs(self):
        """Create student clubs"""
        clubs_data = [
            {
                'name': 'Engineering Student Association',
                'club_type': 'academic',
                'description':
                'Main student organization for engineering students'
            },
            {
                'name': 'Computer Club',
                'club_type': 'academic',
                'description': 'For computer science and IT enthusiasts'
            },
            {
                'name': 'Drama Club',
                'club_type': 'cultural',
                'description': 'Theater and performing arts'
            },
            {
                'name': 'Sports Club',
                'club_type': 'sports',
                'description': 'Various sports activities and competitions'
            },
            {
                'name': 'Volunteer Club',
                'club_type': 'volunteer',
                'description': 'Community service and social work'
            },
        ]

        for club_data in clubs_data:
            club, created = StudentClub.objects.get_or_create(  # type: ignore
                name=club_data['name'], defaults=club_data)
            if created:
                self.stdout.write(f'Created club: {club.name}')

    def create_events(self):
        """Create university events"""
        now = timezone.now()
        events_data = [{
            'title': 'Engineering Week 2024',
            'description':
            'Annual engineering festival with competitions and exhibitions',
            'event_type': 'festival',
            'start_date': now + timedelta(days=30),
            'end_date': now + timedelta(days=37),
            'location': 'University Campus',
            'organizer': 'Engineering Student Association'
        }, {
            'title': 'Technical Seminar',
            'description': 'Industry experts share latest technology trends',
            'event_type': 'academic',
            'start_date': now + timedelta(days=45),
            'end_date': now + timedelta(days=45),
            'location': 'Main Auditorium',
            'organizer': 'Computer Club'
        }]

        for event_data in events_data:
            event, created = UniversityEvent.objects.get_or_create(  # type: ignore
                title=event_data['title'],
                defaults=event_data)
            if created:
                self.stdout.write(f'Created event: {event.title}')

    def create_news(self):
        """Create university news"""
        news_data = [{
            'title': 'New Computer Laboratory Opens',
            'content':
            'The university has opened a state-of-the-art computer laboratory with 50 modern workstations, providing students with access to the latest technology for their studies.',
            'category': 'facilities',
            'tags': 'technology, facilities, students',
            'content_approved': True
        }, {
            'title': 'Students Win National Competition',
            'content':
            'Three students from the Civil Engineering department won first place in the National Bridge Design Competition, showcasing excellent technical skills.',
            'category': 'achievements',
            'tags': 'competition, civil engineering, students',
            'content_approved': True
        }, {
            'title': 'Career Fair 2024 Announced',
            'content':
            'Annual career fair scheduled for next month, featuring 20+ companies offering internships and job opportunities to students.',
            'category': 'events',
            'tags': 'career, jobs, internships',
            'content_approved': True
        }]

        for news_item in news_data:
            news, created = UniversityNews.objects.get_or_create(  # type: ignore
                title=news_item['title'], defaults=news_item)
            if created:
                self.stdout.write(f'Created news: {news.title}')

    def create_contacts(self):
        """Create contact information"""
        contacts_data = [{
            'department': 'Admissions Office',
            'phone': '+95-1-234567',
            'email': 'admissions@hmawbi.edu.mm',
            'office_location': 'Administration Building, Room 101',
            'office_hours': 'Monday-Friday 9AM-4PM'
        }, {
            'department': 'Student Affairs',
            'phone': '+95-1-234568',
            'email': 'students@hmawbi.edu.mm',
            'office_location': 'Student Center, Room 201',
            'office_hours': 'Monday-Friday 8AM-5PM'
        }, {
            'department': 'Academic Office',
            'phone': '+95-1-234569',
            'email': 'academic@hmawbi.edu.mm',
            'office_location': 'Academic Building, Room 301',
            'office_hours': 'Monday-Friday 9AM-4PM'
        }]

        for contact_data in contacts_data:
            contact, created = ContactInformation.objects.get_or_create(  # type: ignore
                department=contact_data['department'],
                defaults=contact_data)
            if created:
                self.stdout.write(f'Created contact: {contact.department}')

    def create_engagement_content(self):
        """Create engagement content"""
        content_data = [
            # Jokes
            {
                'content_type': 'joke',
                'title': 'Engineering Joke',
                'content':
                'Why did the engineering student bring a ladder to class? Because they heard the course was on the next level!',
                'category': 'academic'
            },
            {
                'content_type': 'joke',
                'title': 'Computer Joke',
                'content':
                'Why don\'t programmers like nature? It has too many bugs!',
                'category': 'computer_science'
            },
            # Encouragement
            {
                'content_type': 'encouragement',
                'content':
                'Every expert was once a beginner. Keep pushing forward!',
                'tone': 'encouraging',
                'context': 'academic_struggle'
            },
            {
                'content_type': 'encouragement',
                'content':
                'Your hard work today is building your future success.',
                'tone': 'motivational',
                'context': 'general'
            },
            # Fun Facts
            {
                'content_type': 'fun_fact',
                'content':
                'HMAWBI University was the first technological university in Yangon Region',
                'category': 'history'
            },
            {
                'content_type': 'fun_fact',
                'content':
                'Our university library contains over 50,000 engineering books and journals',
                'category': 'facilities'
            },
            # Study Tips
            {
                'content_type': 'tip',
                'content':
                'Create a consistent study schedule and stick to it',
                'context': 'study_habits'
            },
            {
                'content_type': 'tip',
                'content':
                'Form study groups with classmates for better understanding',
                'context': 'collaboration'
            },
            # Career Advice
            {
                'content_type': 'advice',
                'content':
                'Start building your professional network early in your academic career',
                'context': 'networking'
            },
            {
                'content_type': 'advice',
                'content':
                'Gain practical experience through internships and projects',
                'context': 'experience'
            }
        ]

        for content_item in content_data:
            content, created = EngagementContent.objects.get_or_create(  # type: ignore
                content_type=content_item['content_type'],
                content=content_item['content'],
                defaults=content_item)
            if created:
                self.stdout.write(
                    f'Created {content.content_type}: {content.content[:30]}...'
                )
