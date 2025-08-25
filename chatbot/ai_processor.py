"""
AI Processor for HMAWBI University Chatbot
Main orchestrator that uses specialized handlers
"""

from typing import Dict, List, Any, Optional
from .data_manager import DataManager
from .handlers.info_handler import InfoHandler
from .handlers.activity_handler import ActivityHandler
from .handlers.academic_handler import AcademicHandler
import logging
import re
import traceback
import random

logger = logging.getLogger(__name__)


class UniversityGuidanceChatbot:
    """
    University Guidance Chatbot using rule-based system with specialized handlers
    """

    def __init__(self):
        """Initialize the chatbot with specialized handlers"""
        self.data_manager = DataManager()
        self.info_handler = InfoHandler()
        self.activity_handler = ActivityHandler()
        self.academic_handler = AcademicHandler()
        self.response_templates = self._load_response_templates()

    def _load_response_templates(self) -> Dict[str, Any]:
        """Load response templates for different query types"""
        return {
            'greeting': [
                "Hello! I'm UniGuideBot, your HMAWBI University guidance assistant. How can I help you with information about programs, admissions, or campus life?",
                "Welcome to HMAWBI University! I'm here to help you with questions about our programs, facilities, admissions, and student services. What would you like to know?",
                "Hi there! I'm UniGuideBot, ready to assist you with any questions about HMAWBI University. How can I help you today?"
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
        """Generate a response to user message using specialized handlers"""
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

            # Generate response based on intent using appropriate handler
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

        contact_info_keywords = [
            'contact information', 'contact details', 'contact', 'phone', 'email', 
            'office', 'department contacts', 'reach', 'get in touch'
        ]
        
        # Check for general contact requests first
        if any(keyword in message_lower for keyword in contact_info_keywords):
            return 'contact_info'

        # PRIORITY FIX: Check for office-related queries (even if they contain rector/pro-rector)
        if 'office' in message_lower:
            return 'contact_info'

        # Check for specific departments (for contact)
        department_entities = [
            'information technology department', 'it department',
            'electrical power department', 'electrical department', 
            'electronic department', 'mechatronic department',
            
            'civil engineering department', 'civil department',
            'mechanical engineering department', 'mechanical department',
            'architecture department', 'rector office', 'pro rector office',
            # Also add the "Department of X" format
            'department of information technology', 'department of civil engineering',
            'department of mechanical engineering', 'department of electrical power engineering',
            'department of electronic', 'department of mechatronic', 'department of architecture'
        ]
        
        if any(entity in message_lower for entity in department_entities):
            return 'contact_info'

        # University info keywords (MOVE AFTER CONTACT CHECKS)
        university_info_keywords = [
            'who is rector', 'rector name', 'who is pro-rector', 'pro-rector name', 
            'current rector', 'current pro-rector',  # Make these more specific
            'history', 'about university', 'university information', 'general information', 
            'transportation', 'bus number', 'bus no', 'how to get', 'location', 
            'administration', 'officials', 'leadership'
        ]
        if any(keyword in message_lower for keyword in university_info_keywords):
            return 'university_info'
        # Campus-related queries
        campus_keywords = [
            'campus', 'facility', 'library', 'hostel', 'cafeteria', 'sports',
            'gym', 'dormitory', 'campus life'
        ]
        if any(keyword in message_lower for keyword in campus_keywords):
            return 'campus'

        # Club keywords
        club_keywords = [
        'club', 'organization', 'societies', 'groups', 'student club',
        'extracurricular', 'membership', 'join club', 'club details', 
        'club requirements', 'club membership', 'membership requirements'
        ]
        # Check for club-related queries first (before programs)
        if any(keyword in message_lower for keyword in club_keywords):
            return 'clubs'
        
        # Program keywords
        program_keywords = [
            'program', 'course', 'degree', 'study', 'major', 'curriculum',
            'engineering', 'it', 'computer', 'civil', 'electrical',
            'mechanical', 'software', 'bachelor', 'master', 'phd'
        ]
        if any(keyword in message_lower for keyword in program_keywords):
            return 'programs'

        
        
        # Greeting patterns
        greeting_patterns = [
            r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b'
        ]
        if any(re.search(pattern, message_lower) for pattern in greeting_patterns):
            return 'greeting'

        
        # Event keywords
        event_keywords = [
            'event', 'events', 'festival', 'ceremony', 'workshop',
            'competition', 'upcoming', 'schedule', 'past events', 'previous events'
        ]
        if any(keyword in message_lower for keyword in event_keywords):
            return 'events'

        # Student life queries
        student_life_keywords = [
            'student life', 'activities', 'student services', 'campus activities'
        ]
        if any(keyword in message_lower for keyword in student_life_keywords):
            return 'student_life'

        # Admission-related queries
        admission_keywords = [
            'admission', 'apply', 'application', 'deadline', 'entrance',
            'enroll', 'requirements', 'how to apply'
        ]
        if any(keyword in message_lower for keyword in admission_keywords):
            return 'admission'

        # Scholarship queries
        scholarship_keywords = [
            'scholarship', 'financial aid', 'grant', 'funding', 'assistance', 'scholarship details', 'scholarship requirements'
        ]
        if any(keyword in message_lower for keyword in scholarship_keywords):
            return 'scholarships'

        # News queries - UPDATED
        news_keywords = [
            'news', 'latest', 'updates', 'announcements', 'headlines',
            'tell me about', 'full story', 'more about', 'details about', 'story of'
        ]
        if any(word in message_lower for word in news_keywords):
            return 'news'
        
        return 'default'

    def _is_disallowed_request(self, message: str) -> bool:
        """Check if the request violates privacy/gossip policies"""
        disallowed_patterns = [
            r'\b(prettiest|ugliest|worst teacher|best looking|hottest|ugly|beautiful)\b',
            r'\b(rank.*students|rank.*staff)\b', r'\b(gossip|rumors)\b',
            r'\b(personal.*information|private.*data)\b'
        ]

        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in disallowed_patterns)

    def _handle_disallowed_request(self, message: str) -> Dict[str, Any]:
        """Handle requests that violate policies"""
        return {
            'message':
            "I can't help identify or rank private individuals by appearance or make negative claims about staff. My purpose is to provide information about HMAWBI University's programs, admissions, campus life, and more. How can I assist you with university-related information?",
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
            context['past_events'] = self.data_manager.get_past_events(3)
        elif intent == 'news':
            context['news'] = self.data_manager.get_latest_news(5)
        elif intent == 'contact_info':
            context['contact'] = self.data_manager.get_contact_info()
        elif intent == 'university_info':
            context['university_info'] = self.data_manager.get_university_info()

        return context

    def _generate_rule_based_response(self, user_message: str, intent: str, context_data: Dict[str, Any]) -> str:
        """Generate response using appropriate specialized handler"""

        if intent == 'greeting':
            return random.choice(self.response_templates['greeting'])

        # Info Handler (University Information, Admission, Contact)
        elif intent == 'admission':
            return self.info_handler.handle_admission(context_data)
        elif intent == 'contact_info':
            return self.info_handler.handle_contact(user_message, context_data)
        elif intent == 'university_info':
            return self.info_handler.handle_university_info(user_message, context_data)

        # Activity Handler (Clubs, News, Events, Scholarships)
        elif intent == 'scholarships':
            return self.activity_handler.handle_scholarships(user_message, context_data)
        elif intent == 'clubs':
            return self.activity_handler.handle_clubs(user_message, context_data)
        elif intent == 'events':
            return self.activity_handler.handle_events(user_message, context_data)
        elif intent == 'news':
            return self.activity_handler.handle_news(user_message, context_data)

        # Academic Handler (Programs, Campus Facilities)
        elif intent == 'programs':
            return self.academic_handler.handle_programs(user_message, context_data)
        elif intent == 'campus':
            return self.academic_handler.handle_campus(context_data)
        elif intent == 'student_life':
            return self.academic_handler.handle_student_life(context_data)

        else: # Default case
            return random.choice(self.response_templates['default'])

    def _analyze_response(self, user_message: str, response: str) -> Dict[str, Any]:
        """Analyze the response for urgency and helpfulness"""
        is_urgent = any(keyword in user_message.lower() for keyword in [
            'urgent', 'emergency', 'deadline', 'immediately', 'asap', 'help',
            'problem'
        ])

        # Calculate helpfulness based on response quality
        helpfulness = 0.8  # Default helpfulness
        if len(response) < 50:
            helpfulness = 0.5
        elif "I don't have that info" in response or "I'm not sure" in response or "Sorry, I couldn't retrieve" in response:
            helpfulness = 0.6
        elif any(word in response.lower() for word in ['contact', 'office', 'email', 'phone']):
            helpfulness = 0.9

        return {'is_urgent': is_urgent, 'helpfulness': helpfulness}

    def get_conversation_starters(self) -> List[str]:
        """Get suggested conversation starters"""
        return [
            "What engineering programs do you offer?",
            "How can I apply for admission?",
            "Tell me about campus facilities",
            "Are there any scholarships available?",
            "What clubs can I join?",
            "What are the membership requirements for clubs?",
            "What are the latest university news?",
            "Contact information for Department of Civil Engineering",
            "Contact information for Department of Architecture",
            "Tell me about the university's history.",
            "How do I get to the campus?"
        ]

    def search_programs(self, query: str) -> List[str]:
        """Search for programs based on query"""
        return self.data_manager.search_programs(query)


# Utility functions for testing
def test_chatbot():
    """Test function for development"""
    chatbot = UniversityGuidanceChatbot()

    test_messages = [
        "Hello",
        "What engineering programs do you offer?",
        "Tell me about Computer Science program",
        "How can I apply for admission?",
        "Tell me about student clubs",
        "What are the membership requirements for Guitar Club?",
        "Tell me about scholarships",
        "What are the latest news?",
        "Tell me about the university's history.",
        "Contact information for Department of Civil Engineering",
        "Contact information for Department of Architecture"
    ]

    for message in test_messages:
        print(f"\nUser: {message}")
        response = chatbot.generate_response(message)
        print(f"Bot: {response['message']}")
        print(f"Intent: {response.get('intent', 'unknown')}, Helpfulness: {response['helpfulness']}")


if __name__ == "__main__":
    test_chatbot()