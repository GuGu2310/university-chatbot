
"""
Django management command for updating university data
Usage: python manage.py update_university_data
"""

from django.core.management.base import BaseCommand
from chatbot.data_manager import DataManager
import json

class Command(BaseCommand):
    help = 'Update university data easily'

    def add_arguments(self, parser):
        parser.add_argument('--action', type=str, help='Action to perform: add_program, update_fees, add_tip, backup, stats')
        parser.add_argument('--program', type=str, help='Program name')
        parser.add_argument('--field', type=str, help='Field to update')
        parser.add_argument('--value', type=str, help='New value')
        parser.add_argument('--file', type=str, help='File path for backup/restore')

    def handle(self, *args, **options):
        manager = DataManager()
        
        action = options.get('action')
        
        if action == 'stats':
            self.show_statistics(manager)
        elif action == 'backup':
            self.backup_data(manager, options.get('file', 'university_data_backup.json'))
        elif action == 'add_program':
            self.add_program_interactive(manager)
        elif action == 'update_fees':
            self.update_fees_interactive(manager)
        elif action == 'add_tip':
            self.add_study_tip_interactive(manager)
        elif action == 'search':
            self.search_programs(manager, options.get('value', ''))
        else:
            self.stdout.write(self.style.WARNING('Available actions: stats, backup, add_program, update_fees, add_tip, search'))

    def show_statistics(self, manager):
        """Display current data statistics"""
        stats = manager.get_statistics()
        self.stdout.write(self.style.SUCCESS('\n=== University Data Statistics ==='))
        for key, value in stats.items():
            formatted_key = key.replace('_', ' ').title()
            self.stdout.write(f"  {formatted_key}: {value}")

    def backup_data(self, manager, filepath):
        """Backup data to JSON file"""
        success = manager.export_data_to_json(filepath)
        if success:
            self.stdout.write(self.style.SUCCESS(f'Data backed up to {filepath}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to backup data to {filepath}'))

    def add_program_interactive(self, manager):
        """Interactive program addition"""
        self.stdout.write(self.style.WARNING('\n=== Add New Program ==='))
        
        program_name = input("Program name: ")
        duration = input("Duration: ")
        description = input("Description: ")
        entry_requirements = input("Entry requirements: ")
        salary_range = input("Salary range: ")
        job_prospects = input("Job prospects: ")
        
        # Career paths
        career_paths = []
        self.stdout.write("Enter career paths (press Enter on empty line to finish):")
        while True:
            career = input("Career path: ")
            if not career:
                break
            career_paths.append(career)
        
        # Subjects
        subjects = []
        self.stdout.write("Enter subjects (press Enter on empty line to finish):")
        while True:
            subject = input("Subject: ")
            if not subject:
                break
            subjects.append(subject)
        
        program_data = {
            "duration": duration,
            "description": description,
            "career_paths": career_paths,
            "entry_requirements": entry_requirements,
            "subjects": subjects,
            "job_prospects": job_prospects,
            "salary_range": salary_range
        }
        
        # Validate data
        missing_fields = manager.validate_program_data(program_data)
        if missing_fields:
            self.stdout.write(self.style.ERROR(f'Missing required fields: {missing_fields}'))
            return
        
        success = manager.add_program(program_name, program_data)
        if success:
            self.stdout.write(self.style.SUCCESS(f'Program "{program_name}" added successfully!'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to add program "{program_name}"'))

    def update_fees_interactive(self, manager):
        """Interactive fee update"""
        self.stdout.write(self.style.WARNING('\n=== Update Fees ==='))
        
        current_fees = manager.get_admission_info()['fees']
        self.stdout.write("Current fees:")
        for fee_type, amount in current_fees.items():
            self.stdout.write(f"  {fee_type}: {amount}")
        
        fee_type = input("\nFee type to update: ")
        new_amount = input("New amount: ")
        
        success = manager.update_fees(fee_type, new_amount)
        if success:
            self.stdout.write(self.style.SUCCESS(f'Fee "{fee_type}" updated to {new_amount}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to update fee "{fee_type}"'))

    def add_study_tip_interactive(self, manager):
        """Interactive study tip addition"""
        self.stdout.write(self.style.WARNING('\n=== Add Study Tip ==='))
        
        tip = input("Enter new study tip: ")
        success = manager.add_study_tip(tip)
        
        if success:
            self.stdout.write(self.style.SUCCESS('Study tip added successfully!'))
        else:
            self.stdout.write(self.style.ERROR('Failed to add study tip (might already exist)'))

    def search_programs(self, manager, query):
        """Search programs by keyword"""
        if not query:
            query = input("Enter search query: ")
        
        results = manager.search_programs(query)
        
        if results:
            self.stdout.write(self.style.SUCCESS(f'\nFound {len(results)} programs matching "{query}":'))
            for program in results:
                self.stdout.write(f"  - {program}")
        else:
            self.stdout.write(self.style.WARNING(f'No programs found matching "{query}"'))
