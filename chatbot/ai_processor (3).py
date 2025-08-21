"""
AI Processor for HMAWBI University Chatbot
Handles conversation processing and response generation using rule-based system
"""

from typing import Dict, List, Any, Optional
from .data_manager import DataManager
import logging
import re
import traceback

logger = logging.getLogger(__name__)


class UniversityGuidanceChatbot:
    """
    University Guidance Chatbot using rule-based system for intelligent responses
    Follows the UniGuideBot specifications for university assistance
    """

    def __init__(self):
        """Initialize the chatbot with system-based configuration"""
        self.data_manager = DataManager()
        self.response_templates = self._load_response_templates()

    def _load_response_templates(self) -> Dict[str, Any]:
        """Load response templates for different query types"""
        return {
            'greeting': [
                "Hello! I'm UniGuideBot, your HMAWBI University guidance assistant. How can I help you with information about programs, admissions, or campus life?",
                "Welcome to HMAWBI University! I'm here to help you with questions about our programs, facilities, admissions, and student services. What would you like to know?",
                "Hi there! I'm UniGuideBot, ready to assist you with any questions about HMAWBI University. How can I help you today?"
            ],
            'programs': [
                "We offer various programs at HMAWBI University. Here are some popular ones:",
                "HMAWBI University provides excellent academic programs. Let me share information about our offerings:",
                "Our university has comprehensive programs designed for your career success:"
            ],
            'admission': [
                "For admission information at HMAWBI University:",
                "Here's what you need to know about applying to HMAWBI University:",
                "Admission to HMAWBI University involves several steps:"
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
            ],
            'scholarships': [
                "HMAWBI University offers various scholarship opportunities:",
                "Scholarship programs available at our university:",
                "Financial aid and scholarship options:"
            ],
            'contact': [
                "Here's information about contacting departments at HMAWBI University:",
                "Need to reach a specific department? Here's how:",
                "Contact details for HMAWBI University departments:"
            ],
            'news': [
                "Here's what's happening at HMAWBI University:",
                "Latest news and updates from our university:",
                "Stay informed with our university news:"
            ],
            'events': [
                "Here are upcoming events at HMAWBI University:",
                "Our university hosts various events throughout the year:",
                "Check out these exciting events coming up:"
            ],
            'clubs': [
                "HMAWBI University has many active student clubs and organizations:",
                "Our student clubs offer great opportunities for involvement:",
                "Join one of our vibrant student organizations:"
            ],
            'university_info': [
                "Here's general information about HMAWBI University:",
                "Let me share some key information about our university:",
                "About HMAWBI University:"
            ],
            'default': [
                "I'm here to help with information about HMAWBI University. Could you please be more specific about what you'd like to know?",
                "I can assist you with questions about programs, admissions, campus facilities, scholarships, clubs, events, news, and general university information at HMAWBI University. What interests you?",
                "Thank you for your question. I can provide information about various aspects of HMAWBI University. Please let me know what specific area you'd like to learn about."
            ]
        }

    def generate_response(
        self,
        user_message: str,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Generate a response to user message using rule-based system

        Args:
            user_message: The user's input message
            conversation_history: Previous conversation messages for context

        Returns:
            Dict containing response message, urgency flag, and helpfulness score
        """
        if conversation_history is None:
            conversation_history = []

        try:
            # Check if this is a disallowed request
            if self._is_disallowed_request(user_message):
                return self._handle_disallowed_request(user_message)

            # Classify the message intent
            intent = self._classify_message_intent(user_message)

            # Get relevant university data for context
            context_data = self._get_relevant_context(user_message, intent) or {}

            # Generate response based on intent and context
            response = self._generate_rule_based_response(
                user_message, intent, context_data)

            # Analyze response for urgency and helpfulness
            analysis = self._analyze_response(user_message, response)

            return {
                'message': response,
                'is_urgent': analysis.get('is_urgent', False),
                'helpfulness': analysis.get('helpfulness', 0.8),
                'context_used': bool(context_data),
                'intent': intent
            }

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                'message':
                "I'm sorry, I'm having trouble processing your request right now. Please try again or contact our student services office for immediate assistance.",
                'is_urgent': False,
                'helpfulness': 0.3,
                'intent': 'error'
            }

    def _classify_message_intent(self, message: str) -> str:
        """Classify user message intent using keyword matching"""
        message_lower = message.lower()

        # University info keywords
        university_info_keywords = [
            'rector name', 'pro-rector name', 'pro rector', 'history', 'about university',
            'university information', 'general information', 'transportation',
            'bus number', 'bus no', 'how to get', 'location'
        ]
        if any(keyword in message_lower for keyword in university_info_keywords):
            return 'university_info'

        # Contact keywords and entities
        contact_keywords = [
            'contact', 'phone', 'email', 'office', 'address', 'location',
            'office hours', 'department'
        ]
        known_entities_for_contact = [
            'civil department', 'admissions', 'library', 'registrar',
            'department', 'student affairs', 'mechanical department', 
            'IT department', 'administration', 'office'
        ]

        has_contact_keywords = any(ckey in message_lower for ckey in contact_keywords)
        has_known_entity = any(entity in message_lower for entity in known_entities_for_contact)

        if has_contact_keywords and has_known_entity:
            return 'contact'

        # Greeting patterns
        greeting_patterns = [
            r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b'
        ]
        if any(re.search(pattern, message_lower) for pattern in greeting_patterns):
            return 'greeting'

        # Campus-related queries
        campus_keywords = [
            'campus', 'facility', 'library', 'hostel', 'cafeteria', 'sports',
            'gym', 'dormitory'
        ]
        if any(keyword in message_lower for keyword in campus_keywords):
            return 'campus'

        # Program keywords
        program_keywords = [
            'program', 'course', 'degree', 'study', 'major', 'curriculum',
            'engineering', 'it', 'computer', 'civil', 'electrical',
            'mechanical', 'software'
        ]
        if any(keyword in message_lower for keyword in program_keywords):
            return 'programs'

        # Club keywords
        club_keywords = [
            'club', 'organization', 'societies', 'groups', 'student club',
            'extracurricular', 'membership', 'join club'
        ]
        if any(keyword in message_lower for keyword in club_keywords):
            return 'clubs'

        # Event keywords
        event_keywords = [
            'event', 'events', 'festival', 'ceremony', 'workshop',
            'competition', 'upcoming', 'schedule'
        ]
        if any(keyword in message_lower for keyword in event_keywords):
            return 'events'

        # Student life queries (general)
        student_life_keywords = [
            'student life', 'activities', 'campus life'
        ]
        if any(keyword in message_lower for keyword in student_life_keywords):
            return 'student_life'

        # Admission-related queries
        admission_keywords = [
            'admission', 'apply', 'application', 'deadline', 'entrance',
            'enroll'
        ]
        if any(keyword in message_lower for keyword in admission_keywords):
            return 'admission'

        # Scholarship queries
        scholarship_keywords = [
            'scholarship', 'financial aid', 'grant', 'funding', 'assistance'
        ]
        if any(keyword in message_lower for keyword in scholarship_keywords):
            return 'scholarships'

        # News queries
        if any(word in message_lower for word in ['news', 'latest', 'updates', 'announcements']):
            return 'news'

        return 'default'

    def _is_disallowed_request(self, message: str) -> bool:
        """Check if the request violates privacy/gossip policies"""
        disallowed_patterns = [
            r'\b(prettiest|ugliest|worst teacher|best looking|hottest)\b',
            r'\b(rank.*students|rank.*staff)\b', r'\b(gossip|rumors)\b',
            r'\b(personal.*information|private.*data)\b'
        ]

        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in disallowed_patterns)

    def _handle_disallowed_request(self, message: str) -> Dict[str, Any]:
        """Handle requests that violate policies"""
        return {
            'message':
            "I can't help identify or rank private individuals by appearance or make negative claims about staff. I can help in one of these ways: (1) run an anonymous poll for campus awards, (2) show campus-approved highlights or official recognitions, (3) explain how to submit formal feedback. Which would you prefer?",
            'is_urgent': False,
            'helpfulness': 0.6,
            'intent': 'policy_violation'
        }

    def _get_relevant_context(self, user_message: str, intent: str) -> Dict[str, Any]:
        """Get relevant university data based on user message and intent"""
        context = {}

        if intent == 'programs':
            context['programs'] = self.data_manager.get_all_programs()
        elif intent == 'admission':
            context['admission'] = self.data_manager.get_admission_info()
        elif intent == 'campus':
            context['campus'] = self.data_manager.get_campus_info()
        elif intent == 'student_life':
            context['student_life'] = self.data_manager.get_student_life_info()
        elif intent == 'scholarships':
            context['scholarships'] = self.data_manager.get_scholarships()
        elif intent == 'clubs':
            context['clubs'] = self.data_manager.get_all_clubs()
        elif intent == 'events':
            context['events'] = self.data_manager.get_all_events()
        elif intent == 'news':
            context['news'] = self.data_manager.get_latest_news(5)
        elif intent == 'contact':
            context['contact'] = self.data_manager.get_contact_info()
        elif intent == 'university_info':
            context['university_info'] = self.data_manager.get_university_info()

        return context

    def _generate_rule_based_response(self, user_message: str, intent: str, context_data: Dict[str, Any]) -> str:
        """Generate response using rule-based system"""

        if intent == 'greeting':
            import random
            return random.choice(self.response_templates['greeting'])

        elif intent == 'programs':
            import random
            # Use a more specific prefix if the query is general, or defer to the specific program logic if a program is mentioned.
            response_prefix = random.choice(self.response_templates.get('programs', ["Here are our programs:"]))

            if 'programs' in context_data and context_data['programs']:
                message_lower = user_message.lower()
                specific_program = None

                # --- Refined Logic for finding a specific program ---
                # We want to set specific_program ONLY if the user explicitly mentions a program name.
                # General queries like "What engineering programs" should not trigger this.

                # Iterate through all program names to see if any are mentioned directly.
                for program_name in context_data['programs'].keys():
                    # Check for an exact or very close match of the program name in the user's message.
                    # Using 'in' check is generally good, but we need to ensure it's not just a keyword match.
                    # A common way to do this is to check if the program name is a substring of the message.
                    # However, to avoid matching "engineering" in "What engineering programs?" to "Civil Engineering",
                    # we can be more specific or add a check to ensure it's not just a category.

                    # A more robust check: if the program name itself is in the message
                    if program_name.lower() in message_lower:
                        # Ensure it's not just a partial match of a category word if it's too short or ambiguous.
                        # For example, "engineering programs" should not pick up "Civil Engineering".
                        # Let's try to be more strict: if the program name is mentioned, consider it specific.
                        # The current behavior implies this is already happening.
                        # The issue is that "engineering" might be part of the query, and the loop might find "Civil Engineering".
                        # Let's prioritize exact program name mentions.

                        # If the exact program name is in the message, we've found our specific program.
                        specific_program = program_name
                        break # Found a specific program, no need to check others.

                # --- Decision Branching ---
                if specific_program:
                    # User explicitly asked for a specific program. Show details.
                    prog_data = context_data['programs'][specific_program]
                    response = f"Here's information about **{specific_program}**:\n\n"
                    response += f"📚 Duration: {prog_data.get('duration', 'Not specified')}\n"
                    response += f"📝 Description: {prog_data.get('description', 'No description available')}\n"

                    # --- Handling Career Paths ---
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

                    # --- Handling Salary Range ---
                    salary_range = prog_data.get('salary_range', 'Contact career services for details')
                    if salary_range and salary_range.strip().lower() != 'not specified':
                        response += f"💰 Salary Range: {salary_range}\n"
                    else:
                        response += f"💰 Salary Range: Contact career services for details\n"

                    # --- Handling Specializations ---
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
                    # If no specific program name was explicitly found, it means the query was general
                    # (e.g., "what programs", "engineering programs"). In this case, list all programs.
                    program_names = list(context_data['programs'].keys())
                    if program_names:
                        response = response_prefix + "\n\n" + "\n".join(['• ' + prog for prog in program_names])
                        response += "\n\nWould you like detailed information about any specific program?"
                    else:
                        response = response_prefix + "\n\nSorry, no programs are currently listed. Please check back later."

                return response

            else: # If no program data is available
                return response_prefix + "\n\nI couldn't retrieve program information at the moment. Please check back later."


        elif intent == 'admission':
            import random
            response = random.choice(self.response_templates['admission'])
            if 'admission' in context_data:
                admission_info = context_data['admission']
                response += f"\n\n📅 Academic Year: {admission_info.get('academic_year', 'Current Year')}"
                response += f"\n📆 Application Deadline: {admission_info.get('application_deadline', 'Contact admissions')}"
                response += f"\n📝 Entrance Exam: {admission_info.get('entrance_exam_date', 'TBA')}"
                response += f"\n💰 Application Fee: {admission_info.get('application_fee', 'Contact for details')}"
                response += f"\n📧 Contact: {admission_info.get('contact_email', 'admissions@hmawbi.edu.mm')}"
                response += f"\n📞 Phone: {admission_info.get('contact_phone', 'Contact university')}"
                response += f"\n🕒 Office Hours: {admission_info.get('office_hours', 'Monday-Friday 9:00 AM - 5:00 PM')}"
                if 'requirements' in admission_info:
                    response += f"\n📋 Requirements: {admission_info['requirements']}"
                if 'documents_needed' in admission_info:
                    response += f"\n📄 Documents Needed: {admission_info['documents_needed']}"
            return response

        elif intent == 'campus':
            import random
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
            return response

        elif intent == 'student_life':
            import random
            response = random.choice(self.response_templates['student_life'])
            if 'student_life' in context_data:
                student_info = context_data['student_life']
                clubs = student_info.get('clubs_organizations', [])
                if clubs:
                    response += "\n\n🏛️ Student Clubs & Organizations:\n"
                    for club in clubs[:5]: # List first 5 clubs
                        response += f"• {club}\n"
                else:
                    response += "\n\n🏛️ Student Clubs & Organizations:\nWe have various clubs and organizations for students to join. Contact student services for more details."

                events = student_info.get('upcoming_events', [])
                if events:
                    response += "\n📅 Upcoming Events:\n"
                    for event in events[:3]: # List first 3 events
                        response += f"• {event.get('title', 'Event')}: {event.get('date', 'TBA')}\n"

                response += "\n\nFor detailed information about clubs or events, please ask about specific items!"
            return response

        elif intent == 'scholarships':
            import random
            response = random.choice(self.response_templates['scholarships'])
            message_lower = user_message.lower()

            asking_for_details = any(word in message_lower for word in [
                'eligibility', 'criteria', 'requirements', 'apply',
                'application', 'deadline', 'how to', 'details', 'about',
                'benefits'
            ])

            if 'scholarships' in context_data and context_data['scholarships']:
                scholarships_data = context_data['scholarships']

                # Check if asking for specific scholarship by name
                specific_scholarship = None
                for scholarship in scholarships_data:
                    if scholarship['name'].lower() in message_lower:
                        specific_scholarship = scholarship
                        break

                if specific_scholarship:
                    # Provide detailed info for a specific scholarship
                    response = f"Here's detailed information about **{specific_scholarship['name']}**:\n\n"
                    response += f"📝 Description: {specific_scholarship.get('description', 'Available for eligible students')}\n"
                    response += f"📋 Eligibility Criteria: {specific_scholarship.get('criteria', 'Contact financial aid office')}\n"
                    response += f"💵 Benefit: {specific_scholarship.get('benefit', 'Contact for details')} ({specific_scholarship.get('benefit_type', 'Financial assistance')})\n"
                    response += f"📅 Application Deadline: {specific_scholarship.get('deadline', 'No deadline specified')}\n"
                    if specific_scholarship.get('application_process'):
                        response += f"📄 Application Process: {specific_scholarship['application_process']}\n"
                    response += "\n💡 For applications and more information, please contact our financial aid office!"
                elif asking_for_details:
                    # Provide general details if asked for details but no specific scholarship
                    response = "Here's detailed information about our scholarship programs:\n\n"
                    for scholarship in scholarships_data[:3]: # List first 3 scholarships with details
                        response += f"💰 **{scholarship.get('name', 'Scholarship')}**\n"
                        response += f"   📝 Description: {scholarship.get('description', 'Available for eligible students')}\n"
                        response += f"   📋 Eligibility Criteria: {scholarship.get('criteria', 'Contact financial aid office')}\n"
                        response += f"   💵 Benefit: {scholarship.get('benefit', 'Contact for details')} ({scholarship.get('benefit_type', 'Financial assistance')})\n"
                        response += f"   📅 Application Deadline: {scholarship.get('deadline', 'No deadline specified')}\n\n"

                    response += "💡 For applications and more information, please contact our financial aid office!"
                else:
                    # List general scholarships if no specific query for details
                    response += "\n\n"
                    for scholarship in scholarships_data[:5]: # List first 5 scholarships
                        response += f"• {scholarship.get('name', 'Scholarship')}: {scholarship.get('benefit', 'Financial assistance available')}\n"
                    response += "\n💡 Ask me about a specific scholarship or 'scholarship requirements' for detailed information!"
            else: # If no scholarship data is available
                response += "\n\nSorry, I couldn't retrieve scholarship information at the moment. Please check back later."

            return response

        elif intent == 'clubs':
            import random
            response = random.choice(self.response_templates['clubs'])
            message_lower = user_message.lower()

            if 'clubs' in context_data and context_data['clubs']:
                clubs_data = context_data['clubs']

                # Check if asking for specific club by name
                specific_club = None
                for club in clubs_data:
                    if club['name'].lower() in message_lower:
                        specific_club = club
                        break

                if specific_club:
                    # Provide detailed info for a specific club
                    response = f"Here's information about **{specific_club['name']}**:\n\n"
                    response += f"📝 Description: {specific_club.get('description', 'Student organization')}\n"
                    response += f"🏷️ Type: {specific_club.get('club_type', 'Student Club')}\n"
                    response += f"👨‍🏫 Advisor: {specific_club.get('advisor', 'TBA')}\n"
                    response += f"📅 Meeting Schedule: {specific_club.get('meeting_schedule', 'TBA')}\n"
                    response += f"📋 Membership Requirements: {specific_club.get('membership_requirements', 'Open to all students')}\n"
                    response += f"📧 Contact: {specific_club.get('contact_email', 'Contact student services')}\n"
                    response += f"📅 Established: {specific_club.get('established_date', 'N/A')}\n"
                    response += "\n💡 Contact the club directly or student services for more information about joining!"
                else:
                    # List general clubs if no specific query
                    response += "\n\n"
                    for club in clubs_data[:8]: # List first 8 clubs
                        response += f"• {club.get('name', 'Club')} ({club.get('club_type', 'Student Club')})\n"
                    response += "\n💡 Ask me about a specific club for detailed information including meeting schedules and membership requirements!"
            else: # If no club data is available
                response += "\n\nSorry, I couldn't retrieve club information at the moment. Please check back later."

            return response

        elif intent == 'events':
            import random
            response = random.choice(self.response_templates['events'])
            message_lower = user_message.lower()

            if 'events' in context_data and context_data['events']:
                events_data = context_data['events']

                # Check if asking for specific event by title
                specific_event = None
                for event in events_data:
                    if event['title'].lower() in message_lower:
                        specific_event = event
                        break

                if specific_event:
                    # Provide detailed info for a specific event
                    response = f"Here's information about **{specific_event['title']}**:\n\n"
                    response += f"📝 Description: {specific_event.get('description', 'University event')}\n"
                    response += f"🏷️ Type: {specific_event.get('event_type', 'Event')}\n"
                    response += f"📅 Start Date: {specific_event.get('start_date', 'TBA')}\n"
                    response += f"📅 End Date: {specific_event.get('end_date', 'TBA')}\n"
                    response += f"📍 Location: {specific_event.get('location', 'TBA')}\n"
                    response += f"👥 Organizer: {specific_event.get('organizer', 'University')}\n"
                    response += f"📋 Registration Required: {'Yes' if specific_event.get('registration_required', False) else 'No'}\n"
                    if specific_event.get('registration_required'):
                        response += f"📅 Registration Deadline: {specific_event.get('registration_deadline', 'N/A')}\n"
                    response += f"📞 Contact: {specific_event.get('contact_info', 'Contact event organizer')}\n"
                    response += f"👥 Max Participants: {specific_event.get('max_participants', 'No limit')}\n"
                    response += "\nCheck the university website or contact the organizer for the latest updates."
                else:
                    # List general events if no specific query
                    response += "\n\n"
                    for event in events_data[:5]: # List first 5 events
                        response += f"• **{event.get('title', 'Event')}** ({event.get('event_type', 'Event')})\n"
                        response += f"  📅 {event.get('start_date', 'TBA')} at {event.get('location', 'TBA')}\n\n"
                    response += "💡 Ask me about a specific event for detailed information including registration details!"
            else: # If no event data is available
                response += "\n\nSorry, I couldn't retrieve event information at the moment. Please check back later."

            return response

        elif intent == 'contact':
            import random
            response = random.choice(self.response_templates['contact'])
            if 'contact' in context_data and context_data['contact']:
                message_lower = user_message.lower()
                specific_department = None

                # Check if asking for a specific department
                for department_name, department_data in context_data['contact'].items():
                    if department_name.lower() in message_lower or department_name.lower().replace(" ", "") in message_lower.replace(" ", ""):
                        specific_department = department_name
                        break

                if specific_department:
                    # Provide detailed info for a specific department
                    dept_data = context_data['contact'][specific_department]
                    response = f"Here's the contact information for **{specific_department}**:\n\n"
                    response += f"📞 **Phone:** {dept_data.get('phone', 'Not specified')}\n"
                    response += f"📧 **Email:** {dept_data.get('email', 'Not specified')}\n"
                    response += f"👨‍🏫 **Teacher:** {dept_data.get('teacher', 'Not specified')}\n"
                    if dept_data.get('location'):
                        response += f"📍 **Location:** {dept_data.get('location', 'Not specified')}\n"
                    response += f"🕒 **Office Hours:** {dept_data.get('hours', 'Not specified')}\n"
                    response += f"📝 **Description:** {dept_data.get('description', 'Not specified')}\n"
                    response += "\nWould you like to know about other departments?"
                else:
                    # List general departments if no specific query
                    departments = list(context_data['contact'].keys())[:5]
                    response += "\n\n" + "\n".join(['• ' + dept for dept in departments])
                    response += "\n\nWould you like detailed contact information for any specific department?"
            else: # If no contact data is available
                response = "I couldn't retrieve any department contact information at the moment. Please check back later or contact the main university line."
            return response

        elif intent == 'news':
            import random
            response = random.choice(self.response_templates['news']) + "\n\n"

            try:
                news_items = context_data.get('news', [])

                if news_items:
                    message_lower = user_message.lower()

                    # Check if asking for specific news by title
                    specific_news = None
                    for news_item in news_items:
                        if news_item.get('title', '').lower() in message_lower:
                            specific_news = news_item
                            break

                    if specific_news:
                        # Provide detailed info for specific news
                        response = f"Here's the full story about **{specific_news.get('title', 'University News')}**:\n\n"
                        response += f"📅 **Date:** {specific_news.get('date', 'N/A')}\n"
                        response += f"🏷️ **Category:** {specific_news.get('category', 'General')}\n"
                        if specific_news.get('tags'):
                            response += f"🏷️ **Tags:** {', '.join(specific_news.get('tags', []))}\n"
                        response += f"\n📰 **Content:**\n{specific_news.get('content', 'No content available.')}\n"
                    else:
                        # List general news if no specific query
                        response += "**Latest Updates:**\n"
                        for i, news_item in enumerate(news_items[:5], 1): # List first 5 news items with summary
                            title = news_item.get('title', 'University News')
                            date = news_item.get('date', 'N/A')
                            content = news_item.get('content', 'No description available.')

                            # Truncate content for summary
                            short_description = content
                            if len(short_description) > 100:
                                short_description = short_description[:97] + "..."

                            response += f"{i}. **{title}** ({date})\n"
                            response += f"   {short_description}\n\n"

                        response += "💡 Ask me about a specific news title for the full story!"
                else: # If no news data is available
                    response += "📰 Stay tuned for exciting university updates and announcements!\n"

                return response

            except Exception as news_error:
                logger.error(f"Error in news handling: {news_error}")
                logger.error(f"Full traceback: {traceback.format_exc()}")
                return "I'm having trouble accessing the news right now. Please try again later or contact our information desk."

        elif intent == 'university_info':
            import random
            response = random.choice(self.response_templates['university_info'])
            message_lower = user_message.lower()

            if 'university_info' in context_data and context_data['university_info']:
                university_info_data = context_data['university_info']

                # Check if user is asking about a specific type of info (general, leadership, location, etc.)
                specific_info_type = None
                for info_type_key, info_content in university_info_data.items():
                    if info_type_key.lower() in message_lower:
                        specific_info_type = info_type_key
                        break

                if specific_info_type:
                    # Provide detailed info for a specific university info type
                    info_item = university_info_data[specific_info_type]
                    response = f"Here is the information about **{specific_info_type}** at HMAWBI University:\n\n"
                    response += f"📚 **{info_item.get('title', specific_info_type)}**\n"
                    response += f"   {info_item.get('content', 'No content available.')}\n"
                    if info_item.get('description'):
                        response += f"   {info_item.get('description')}\n"
                else:
                    # Provide general university info if no specific type is mentioned
                    response += "\n\n"
                    for info_type_key, info_item in university_info_data.items():
                        response += f"📚 **{info_item.get('title', info_type_key)}**:\n"
                        # Display a short snippet of content
                        content_snippet = info_item.get('content', 'No details available.')
                        if len(content_snippet) > 150:
                            content_snippet = content_snippet[:147] + "..."
                        response += f"   {content_snippet}\n\n"
                    response += "💡 You can ask for specific details like 'university leadership', 'university transportation', or 'university history'."
            else: # If no university info data is available
                response += "\n\nSorry, I couldn't retrieve university information at the moment. Please check back later."
            return response

        else:  # default intent
            import random
            return random.choice(self.response_templates['default'])

    def _analyze_response(self, user_message: str,
                          response: str) -> Dict[str, Any]:
        """Analyze the response for urgency and helpfulness"""
        is_urgent = any(keyword in user_message.lower() for keyword in [
            'urgent', 'emergency', 'deadline', 'immediately', 'asap', 'help',
            'problem'
        ])

        # Calculate helpfulness based on response quality
        helpfulness = 0.8  # Default helpfulness
        if len(response) < 50: # Short responses might be less helpful
            helpfulness = 0.5
        elif "I don't have that info" in response or "I'm not sure" in response or "Sorry, I couldn't retrieve" in response: # Responses indicating lack of info
            helpfulness = 0.6
        elif any(word in response.lower() for word in ['contact', 'office', 'email', 'phone']): # Responses with contact info are generally helpful
            helpfulness = 0.9

        return {'is_urgent': is_urgent, 'helpfulness': helpfulness}

    def get_conversation_starters(self) -> List[str]:
        """Get suggested conversation starters"""
        return [
            "What engineering programs do you offer?",
            "How can I apply for admission?",
            "What are the tuition fees?",
            "Tell me about campus facilities",
            "Are there any scholarships available?",
            "What is student life like at HMAWBI?",
            "What clubs can I join?",
            "What are the membership requirements for clubs?",
            "How do I apply for scholarships?",
            "What are the latest university news?",
            "Contact information for admissions",
            "Tell me about the university's history.",
            "How do I get to the campus?"
        ]

    def search_programs(self, query: str) -> List[str]:
        """Search for programs based on query"""
        return self.data_manager.search_programs(query)

    def get_quick_responses(self, category: str) -> List[str]:
        """Get quick responses for specific categories"""
        return self.response_templates.get(category,
                                           self.response_templates['default'])

# Utility functions for testing and development
def test_chatbot():
    """Test function for development"""
    chatbot = UniversityGuidanceChatbot()

    test_messages = [
        "Hello",
        "Hi there",
        "What engineering programs do you offer?",
        "Tell me about Computer Science program",
        "How can I apply for admission?",
        "Tell me about student clubs",
        "What are the membership requirements for clubs?",
        "Tell me about scholarships",
        "How do I apply for scholarships?",
        "Who is the prettiest student?",  # Should be blocked
        "What are the campus facilities?",
        "Contact information for Admissions",  # Test contact intent
        "What's the phone number for the library?",  # Test contact intent
        "What are the latest news?",
        "Tell me about the university's history.",
        "How do I get to the campus?"
    ]

    for message in test_messages:
        print(f"\nUser: {message}")
        response = chatbot.generate_response(message)
        print(f"Bot: {response['message']}")
        print(
            f"Intent: {response.get('intent', 'unknown')}, Urgent: {response['is_urgent']}, Helpfulness: {response['helpfulness']}"
        )


if __name__ == "__main__":
    test_chatbot()