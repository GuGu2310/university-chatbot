"""
Academic Handler for HMAWBI University Chatbot
Handles programs, campus facilities, and student life
"""

from typing import Dict, List, Any, Optional
import random
import logging

logger = logging.getLogger(__name__)


class AcademicHandler:
    """Handler for programs, campus facilities, and student life queries"""
    
    def __init__(self):
        self.response_templates = {
            'programs': [
                "We offer various programs at HMAWBI University. Here are some popular ones:",
                "HMAWBI University provides excellent academic programs. Let me share information about our offerings:",
                "Our university has comprehensive programs designed for your career success:"
            ],
            'campus': [
                "HMAWBI University campus offers excellent facilities:",
                "Our campus provides a comprehensive learning environment:",
                "Campus life at HMAWBI University includes:"
            ],
            'student_life': [
                "Student life at HMAWBI University is vibrant and engaging:",
                "Our university offers a rich student experience:",
                "Campus life includes many opportunities for growth and engagement:"
            ]
        }

    def handle_programs(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to university programs."""
        response_prefix = random.choice(self.response_templates.get('programs', ["Here are our programs:"]))

        if 'programs' in context_data and context_data['programs']:
            message_lower = user_message.lower()
            specific_program = None

            # --- Logic for finding a specific program ---
            for program_name in context_data['programs'].keys():
                if program_name.lower() in message_lower:
                    specific_program = program_name
                    break

            if specific_program:
                # User explicitly asked for a specific program. Show details.
                prog_data = context_data['programs'][specific_program]
                response = f"Here's information about **{specific_program}**:\n\n"
                response += f"📚 Duration: {prog_data.get('duration', 'Not specified')}\n"
                response += f"📝 Description: {prog_data.get('description', 'No description available')}\n"

                career_paths = prog_data.get('career_paths', [])
                if isinstance(career_paths, list):
                    valid_paths = [path.strip() for path in career_paths if path and path.strip().lower() != 'not specified']
                    if valid_paths:
                        response += f"🎯 Career Paths: {', '.join(valid_paths)}\n"
                    else:
                        response += f"🎯 Career Paths: Contact career services for details\n"
                elif isinstance(career_paths, str) and career_paths.strip() and career_paths.strip().lower() != 'not specified':
                    response += f"🎯 Career Paths: {career_paths}\n"
                else:
                    response += f"🎯 Career Paths: Contact career services for details\n"

                response += f"📋 Entry Requirements: {prog_data.get('entry_requirements', 'Contact admissions for details')}\n"

                salary_range = prog_data.get('salary_range', 'Contact career services for details')
                if salary_range and salary_range.strip().lower() != 'not specified':
                    response += f"💰 Salary Range: {salary_range}\n"
                else:
                    response += f"💰 Salary Range: Contact career services for details\n"

                specializations = prog_data.get('specializations', [])
                if isinstance(specializations, list):
                    valid_specs = [spec.strip() for spec in specializations if spec and spec.strip().lower() != 'not specified']
                    if valid_specs:
                        response += f"🔬 Specializations: {', '.join(valid_specs)}\n"
                    else:
                        response += f"🔬 Specializations: Contact academic office for details\n"
                elif isinstance(specializations, str) and specializations.strip() and specializations.strip().lower() != 'not specified':
                    response += f"🔬 Specializations: {specializations}\n"
                else:
                    response += f"🔬 Specializations: Contact academic office for details\n"

                response += "\nWould you like detailed information about any other programs?"

            else:
                # If no specific program name was explicitly found, list all programs.
                program_names = list(context_data['programs'].keys())
                if program_names:
                    response = response_prefix + "\n\n" + "\n".join(['• ' + prog for prog in program_names])
                    response += "\n\nWould you like detailed information about any specific program?"
                else:
                    response = response_prefix + "\n\nSorry, no programs are currently listed. Please check back later."

            return response

        else: # If no program data is available
            return response_prefix + "\n\nI couldn't retrieve program information at the moment. Please check back later."

    def handle_campus(self, context_data: Dict[str, Any]) -> str:
        """Handles responses related to campus facilities."""
        response = random.choice(self.response_templates['campus'])
        if 'campus' in context_data:
            campus_info = context_data['campus']
            facilities = campus_info.get('facilities', {})
            if facilities:
                response += "\n\n"
                for facility_type, facility_list in facilities.items():
                    if facility_list:
                        response += f"🏛️ {facility_type.replace('_', ' ').title()}:\n"
                        for facility in facility_list[:3]: # Show first 3 facilities of each type
                            response += f"  • {facility}\n"
                        response += "\n"
                        
            # Add additional campus info if available
            if campus_info.get('campus_size'):
                response += f"📏 Campus Size: {campus_info.get('campus_size')}\n"
            if campus_info.get('wifi_available'):
                response += f"📶 WiFi: {'Available' if campus_info.get('wifi_available') else 'Limited'}\n"
            if campus_info.get('parking'):
                response += f"🅿️ Parking: {campus_info.get('parking')}\n"
            if campus_info.get('security'):
                response += f"🔒 Security: {campus_info.get('security')}\n"
                
            response += "\n💡 Would you like more details about any specific facility?"
        return response

    def handle_student_life(self, context_data: Dict[str, Any]) -> str:
        """Handles responses related to student life."""
        response = random.choice(self.response_templates['student_life'])
        if 'student_life' in context_data:
            student_info = context_data['student_life']
            
            # Student clubs and organizations
            clubs = student_info.get('clubs_organizations', [])
            if clubs:
                response += "\n\n🏛️ Student Clubs & Organizations:\n"
                for club in clubs[:5]: # List first 5 clubs
                    response += f"• {club}\n"
            else:
                response += "\n\n🏛️ Student Clubs & Organizations:\nWe have various clubs and organizations for students to join. Contact student services for more details."

            # Student services
            services = student_info.get('student_services', [])
            if services:
                response += "\n📋 Student Services:\n"
                for service in services[:5]: # List first 5 services
                    response += f"• {service}\n"

            # Upcoming events
            events = student_info.get('upcoming_events', [])
            if events:
                response += "\n📅 Upcoming Events:\n"
                for event in events[:3]: # List first 3 events
                    response += f"• {event.get('title', 'Event')}: {event.get('date', 'TBA')}\n"

            # Student support
            if student_info.get('counseling_services'):
                response += f"\n🧠 Counseling Services: {student_info.get('counseling_services')}\n"
            if student_info.get('health_services'):
                response += f"🏥 Health Services: {student_info.get('health_services')}\n"
            if student_info.get('career_services'):
                response += f"💼 Career Services: {student_info.get('career_services')}\n"

            response += "\n\n💡 For detailed information about clubs, events, or services, please ask about specific items!"
        return response