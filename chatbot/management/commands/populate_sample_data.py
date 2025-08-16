
from django.core.management.base import BaseCommand
from chatbot.models import UniversityProgram, AdmissionInfo, Scholarship, UniversityFee, EngagementContent
from decimal import Decimal
from django.utils import timezone
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populate sample data for university chatbot'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample data...')

        # Create University Programs
        programs_data = [
            {
                'name': 'Civil Engineering',
                'duration': '5 years',
                'description': 'Comprehensive civil engineering program covering structural, environmental, and transportation engineering.',
                'entry_requirements': 'High school graduation with strong mathematics and physics background. Minimum GPA of 3.0.',
                'career_paths': 'Civil Engineer, Structural Engineer, Construction Manager, Project Engineer',
                'subjects': 'Mathematics, Physics, Engineering Mechanics, Structural Analysis, Concrete Technology',
                'job_prospects': 'Excellent job prospects in construction, infrastructure development, and government sectors.',
                'salary_range': '500,000 - 1,500,000 MMK per month',
                'specializations': 'Structural Engineering, Environmental Engineering, Transportation Engineering',
                'level': 'undergraduate'
            },
            {
                'name': 'Computer Science and IT',
                'duration': '4 years',
                'description': 'Modern computer science program focusing on software development, AI, and system administration.',
                'entry_requirements': 'High school graduation with mathematics background. Basic computer literacy preferred.',
                'career_paths': 'Software Developer, System Administrator, Data Analyst, AI Engineer',
                'subjects': 'Programming, Data Structures, Algorithms, Database Systems, Web Development',
                'job_prospects': 'High demand in IT sector, startups, and multinational companies.',
                'salary_range': '600,000 - 2,000,000 MMK per month',
                'specializations': 'Software Engineering, Data Science, Cybersecurity, AI/ML',
                'level': 'undergraduate'
            },
            {
                'name': 'Electrical Engineering',
                'duration': '5 years',
                'description': 'Electrical engineering program covering power systems, electronics, and telecommunications.',
                'entry_requirements': 'High school graduation with strong mathematics and physics. Understanding of basic electrical concepts.',
                'career_paths': 'Electrical Engineer, Power Systems Engineer, Electronics Engineer, Telecommunications Engineer',
                'subjects': 'Circuit Analysis, Power Systems, Electronics, Control Systems, Telecommunications',
                'job_prospects': 'Good opportunities in power sector, telecommunications, and manufacturing.',
                'salary_range': '550,000 - 1,800,000 MMK per month',
                'specializations': 'Power Engineering, Electronics, Telecommunications, Control Systems',
                'level': 'undergraduate'
            },
            {
                'name': 'Mechanical Engineering',
                'duration': '5 years',
                'description': 'Mechanical engineering program focusing on design, manufacturing, and thermal systems.',
                'entry_requirements': 'High school graduation with strong mathematics and physics background.',
                'career_paths': 'Mechanical Engineer, Manufacturing Engineer, Design Engineer, Automotive Engineer',
                'subjects': 'Thermodynamics, Fluid Mechanics, Machine Design, Manufacturing Processes, CAD',
                'job_prospects': 'Opportunities in manufacturing, automotive, and industrial sectors.',
                'salary_range': '500,000 - 1,600,000 MMK per month',
                'specializations': 'Automotive Engineering, Manufacturing, Thermal Systems, Design',
                'level': 'undergraduate'
            }
        ]

        for prog_data in programs_data:
            program, created = UniversityProgram.objects.get_or_create(
                name=prog_data['name'],
                defaults=prog_data
            )
            if created:
                self.stdout.write(f'Created program: {program.name}')

        # Create Admission Info
        admission_data = {
            'academic_year': '2025-2026',
            'application_start_date': date.today(),
            'application_deadline': date.today() + timedelta(days=90),
            'entrance_exam_date': date.today() + timedelta(days=60),
            'application_fee': Decimal('50000'),
            'requirements': 'High school graduation certificate, transcripts, entrance exam pass, medical certificate',
            'documents_needed': 'Academic transcripts, ID card copy, passport photos, medical certificate, recommendation letters',
            'contact_email': 'admissions@hmawbi.edu.mm',
            'contact_phone': '+95-1-234567',
            'office_hours': 'Monday-Friday 9:00 AM - 5:00 PM',
            'is_current': True
        }

        admission, created = AdmissionInfo.objects.get_or_create(
            academic_year='2025-2026',
            defaults=admission_data
        )
        if created:
            self.stdout.write('Created admission information')

        # Create Scholarships
        scholarships_data = [
            {
                'name': 'Merit Scholarship',
                'description': 'Scholarship for outstanding academic performance',
                'eligibility_criteria': 'Minimum GPA of 3.8, excellent entrance exam scores',
                'benefit_amount': '50% tuition reduction',
                'benefit_type': 'tuition_reduction',
                'application_process': 'Submit application with academic transcripts and essay'
            },
            {
                'name': 'Need-Based Financial Aid',
                'description': 'Financial assistance for students from low-income families',
                'eligibility_criteria': 'Family income below specified threshold, good academic standing',
                'benefit_amount': '200,000 MMK monthly stipend',
                'benefit_type': 'stipend',
                'application_process': 'Submit financial documents and application form'
            }
        ]

        for schol_data in scholarships_data:
            scholarship, created = Scholarship.objects.get_or_create(
                name=schol_data['name'],
                defaults=schol_data
            )
            if created:
                self.stdout.write(f'Created scholarship: {scholarship.name}')

        # Create University Fees
        fees_data = [
            {
                'fee_type': 'tuition',
                'amount': Decimal('1500000'),
                'academic_year': '2025-2026',
                'payment_schedule': 'Annual or two installments',
                'is_current': True
            },
            {
                'fee_type': 'hostel',
                'amount': Decimal('300000'),
                'academic_year': '2025-2026',
                'payment_schedule': 'Annual',
                'is_current': True
            },
            {
                'fee_type': 'application',
                'amount': Decimal('50000'),
                'academic_year': '2025-2026',
                'payment_schedule': 'One-time',
                'is_current': True
            }
        ]

        for fee_data in fees_data:
            fee, created = UniversityFee.objects.get_or_create(
                fee_type=fee_data['fee_type'],
                academic_year=fee_data['academic_year'],
                defaults=fee_data
            )
            if created:
                self.stdout.write(f'Created fee: {fee.get_fee_type_display()}')

        # Create Engagement Content
        engagement_data = [
            {
                'content_type': 'joke',
                'content': 'Why did the engineering student bring a ladder to class? Because they heard the course was on the next level!',
                'category': 'academic'
            },
            {
                'content_type': 'joke',
                'content': 'Why do programmers prefer dark mode? Because light attracts bugs!',
                'category': 'technology'
            },
            {
                'content_type': 'encouragement',
                'content': 'Every expert was once a beginner. Keep pushing forward and believe in yourself!',
                'tone': 'motivational'
            },
            {
                'content_type': 'encouragement',
                'content': 'Success is not final, failure is not fatal: it is the courage to continue that counts. You got this!',
                'tone': 'inspirational'
            },
            {
                'content_type': 'fun_fact',
                'content': 'HMAWBI University was established to provide quality technical education in Myanmar and has graduated thousands of engineers.',
                'category': 'university'
            },
            {
                'content_type': 'tip',
                'content': 'Study tip: Use the Pomodoro Technique - study for 25 minutes, then take a 5-minute break. This helps maintain focus and retention.',
                'category': 'study'
            }
        ]

        for content_data in engagement_data:
            content, created = EngagementContent.objects.get_or_create(
                content_type=content_data['content_type'],
                content=content_data['content'],
                defaults=content_data
            )
            if created:
                self.stdout.write(f'Created engagement content: {content.get_content_type_display()}')

        self.stdout.write(self.style.SUCCESS('Sample data populated successfully!'))
