
"""
Interactive menu for common Django management tasks
Usage: python manage.py menu
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
import sys
import os

class Command(BaseCommand):
    help = 'Interactive menu for common tasks'

    def handle(self, *args, **options):
        while True:
            self.show_menu()
            try:
                choice = input("\nEnter your choice (1-10): ").strip()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS("\nGoodbye!"))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error: {e}"))

    def show_menu(self):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🎓 HMAWBI University Chatbot Management Menu'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write("1. 📊 Show Statistics")
        self.stdout.write("2. 🎯 Create Superuser")
        self.stdout.write("3. 🔄 Run Migrations")
        self.stdout.write("4. 📚 Populate Sample Data")
        self.stdout.write("5. 🧹 Cleanup Old Conversations")
        self.stdout.write("6. 💾 Backup Data")
        self.stdout.write("7. 🔍 Search Programs")
        self.stdout.write("8. ➕ Add New Program")
        self.stdout.write("9. 📰 Add News/Announcement")
        self.stdout.write("10. 🐚 Open Django Shell")
        self.stdout.write("0. ❌ Exit")

    def handle_choice(self, choice):
        if choice == '1':
            self.show_statistics()
        elif choice == '2':
            call_command('createsuperuser')
        elif choice == '3':
            self.run_migrations()
        elif choice == '4':
            call_command('populate_resources')
        elif choice == '5':
            days = input("Delete conversations older than how many days? (default 30): ").strip()
            days = int(days) if days.isdigit() else 30
            call_command('cleanup_old_conversations', days=days)
        elif choice == '6':
            filename = input("Backup filename (default: backup.json): ").strip()
            filename = filename if filename else 'backup.json'
            call_command('update_university_data', action='backup', file=filename)
        elif choice == '7':
            query = input("Enter search term: ").strip()
            call_command('update_university_data', action='search', value=query)
        elif choice == '8':
            call_command('update_university_data', action='add_program')
        elif choice == '9':
            call_command('update_university_data', action='add_news')
        elif choice == '10':
            self.stdout.write(self.style.WARNING("Starting Django shell..."))
            call_command('shell')
        elif choice == '0':
            self.stdout.write(self.style.SUCCESS("Goodbye!"))
            sys.exit(0)
        else:
            self.stdout.write(self.style.ERROR("Invalid choice. Please try again."))

    def show_statistics(self):
        try:
            call_command('update_university_data', action='stats')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error getting statistics: {e}"))

    def run_migrations(self):
        self.stdout.write(self.style.WARNING("Making migrations..."))
        call_command('makemigrations')
        self.stdout.write(self.style.WARNING("Running migrations..."))
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS("✅ Migrations completed!"))
