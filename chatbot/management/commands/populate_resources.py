
from django.core.management.base import BaseCommand
from chatbot.models import UniversityProgram, CareerPath, AdmissionResource, StudentCampaign

class Command(BaseCommand):
    help = 'Populate the database with sample university guidance data'

    def handle(self, *args, **options):
        self.stdout.write('Populating university guidance data...')

        # Create HMAWBI Technological University programs
        programs_data = [
            {
                'name': 'Civil Engineering',
                'university': 'HMAWBI Technological University',
                'level': 'undergraduate',
                'description': 'Comprehensive program covering structural design, construction management, and infrastructure development for Myanmar\'s growing cities.',
                'requirements': 'Matriculation exam with strong physics and mathematics scores',
                'duration': '5 years',
                'career_prospects': 'Civil Engineer, Construction Manager, Infrastructure Planner, Government Engineer'
            },
            {
                'name': 'Computer Engineering',
                'university': 'HMAWBI Technological University',
                'level': 'undergraduate',
                'description': 'Advanced program combining hardware and software engineering for Myanmar\'s digital transformation.',
                'requirements': 'Matriculation exam with strong mathematics and physics, basic computer literacy',
                'duration': '5 years',
                'career_prospects': 'Software Engineer, Systems Analyst, IT Manager, Technology Consultant'
            },
            {
                'name': 'Electrical Engineering',
                'university': 'HMAWBI Technological University',
                'level': 'undergraduate',
                'description': 'Comprehensive electrical engineering program focusing on power systems, electronics, and renewable energy for Myanmar.',
                'requirements': 'Matriculation exam with excellent physics and mathematics scores',
                'duration': '5 years',
                'career_prospects': 'Electrical Engineer, Power Systems Engineer, Electronics Designer, Renewable Energy Specialist'
            },
            {
                'name': 'Mechanical Engineering',
                'university': 'HMAWBI Technological University',
                'level': 'undergraduate',
                'description': 'Engineering program covering manufacturing, automotive, and industrial systems for Myanmar\'s industrial development.',
                'requirements': 'Matriculation exam with strong physics, mathematics, and chemistry scores',
                'duration': '5 years',
                'career_prospects': 'Mechanical Engineer, Manufacturing Engineer, Industrial Designer, Automotive Engineer'
            },
            {
                'name': 'Chemical Engineering',
                'university': 'HMAWBI Technological University',
                'level': 'undergraduate',
                'description': 'Specialized program in chemical processes, petrochemicals, and environmental engineering for Myanmar\'s industrial sector.',
                'requirements': 'Matriculation exam with excellent chemistry, physics, and mathematics scores',
                'duration': '5 years',
                'career_prospects': 'Chemical Engineer, Process Engineer, Environmental Engineer, Petrochemical Specialist'
            },
            {
                'name': 'Information Technology',
                'university': 'HMAWBI Technological University',
                'level': 'undergraduate',
                'description': 'Modern IT program focusing on software development, networking, and digital systems for Myanmar\'s tech industry.',
                'requirements': 'Matriculation exam with strong mathematics, basic computer knowledge',
                'duration': '4 years',
                'career_prospects': 'IT Specialist, Network Administrator, Software Developer, Database Administrator'
            }
        ]

        for program_data in programs_data:
            program, created = UniversityProgram.objects.get_or_create(
                name=program_data['name'],
                university=program_data['university'],
                defaults=program_data
            )
            if created:
                self.stdout.write(f'Created program: {program.name}')

        # Create Myanmar technology career paths
        careers_data = [
            {
                'title': 'Civil Engineer (Myanmar Infrastructure)',
                'description': 'Design and supervise construction of roads, bridges, and buildings for Myanmar\'s development projects.',
                'required_education': 'Bachelor\'s in Civil Engineering from HMAWBI or recognized technological university',
                'skills_needed': 'Structural analysis, project management, AutoCAD, site supervision',
                'salary_range': '800,000 - 2,500,000 MMK per month',
                'job_outlook': 'High demand due to Myanmar\'s infrastructure development'
            },
            {
                'title': 'Software Engineer (Myanmar Tech Sector)',
                'description': 'Develop software applications and digital solutions for Myanmar\'s growing technology companies.',
                'required_education': 'Bachelor\'s in Computer Engineering or Information Technology from HMAWBI',
                'skills_needed': 'Programming, web development, mobile apps, database management',
                'salary_range': '600,000 - 2,000,000 MMK per month',
                'job_outlook': 'Rapidly growing with Myanmar\'s digital transformation'
            },
            {
                'title': 'Electrical Engineer (Power Systems)',
                'description': 'Design and maintain electrical power systems for Myanmar\'s energy infrastructure.',
                'required_education': 'Bachelor\'s in Electrical Engineering from HMAWBI Technological University',
                'skills_needed': 'Power systems, renewable energy, electrical design, safety protocols',
                'salary_range': '700,000 - 2,200,000 MMK per month',
                'job_outlook': 'Strong demand for Myanmar\'s electrification projects'
            },
            {
                'title': 'Mechanical Engineer (Manufacturing)',
                'description': 'Design and improve manufacturing processes for Myanmar\'s industrial sector.',
                'required_education': 'Bachelor\'s in Mechanical Engineering from HMAWBI',
                'skills_needed': 'Manufacturing processes, quality control, machinery design, production management',
                'salary_range': '650,000 - 1,800,000 MMK per month',
                'job_outlook': 'Good prospects with industrial development'
            }
        ]

        for career_data in careers_data:
            career, created = CareerPath.objects.get_or_create(
                title=career_data['title'],
                defaults=career_data
            )
            if created:
                self.stdout.write(f'Created career: {career.title}')

        # Create sample admission resources
        resources_data = [
            {
                'title': 'Common Application Tips',
                'description': 'Essential tips for completing your college application.',
                'resource_type': 'application_tips',
                'is_priority': True
            },
            {
                'title': 'Merit Scholarship Program',
                'description': 'Academic excellence scholarship for high-achieving students.',
                'resource_type': 'scholarship',
                'is_priority': True
            }
        ]

        for resource_data in resources_data:
            resource, created = AdmissionResource.objects.get_or_create(
                title=resource_data['title'],
                defaults=resource_data
            )
            if created:
                self.stdout.write(f'Created resource: {resource.title}')

        # Create sample student campaigns
        campaigns_data = [
            {
                'title': 'Study Abroad Program',
                'description': 'Semester abroad opportunities in Europe and Asia.',
                'campaign_type': 'study_abroad',
                'benefits': 'Cultural experience, language skills, global perspective',
                'is_active': True
            },
            {
                'title': 'Research Assistant Positions',
                'description': 'Undergraduate research opportunities with faculty.',
                'campaign_type': 'research',
                'benefits': 'Research experience, mentorship, academic credit',
                'is_active': True
            }
        ]

        for campaign_data in campaigns_data:
            campaign, created = StudentCampaign.objects.get_or_create(
                title=campaign_data['title'],
                defaults=campaign_data
            )
            if created:
                self.stdout.write(f'Created campaign: {campaign.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated university guidance data!'))
