
"""
AI Processor for HMAWBI University Chatbot
Handles conversation processing and response generation using rule-based system
"""

from typing import Dict, List, Any, Optional
from django.conf import settings
from .data_manager import DataManager
import logging
import json
import re

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
            'fees': [
                "Regarding fees and financial information:",
                "Here's information about costs at HMAWBI University:",
                "Financial details for HMAWBI University:"
            ],
            'scholarships': [
                "HMAWBI University offers various scholarship opportunities:",
                "Scholarship programs available at our university:",
                "Financial aid and scholarship options:"
            ],
            'default': [
                "I'm here to help with information about HMAWBI University. Could you please be more specific about what you'd like to know?",
                "I can assist you with questions about programs, admissions, campus facilities, fees, scholarships, and student life at HMAWBI University. What interests you?",
                "Thank you for your question. I can provide information about various aspects of HMAWBI University. Please let me know what specific area you'd like to learn about."
            ]
        }

    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Generate a response to user message using rule-based system
        
        Args:
            user_message: The user's input message
            conversation_history: Previous conversation messages for context
            
        Returns:
            Dict containing response message, urgency flag, and helpfulness score
        """
        try:
            # Check if this is a disallowed request
            if self._is_disallowed_request(user_message):
                return self._handle_disallowed_request(user_message)
            
            # Classify the message intent
            intent = self._classify_message_intent(user_message)
            
            # Get relevant university data for context
            context_data = self._get_relevant_context(user_message, intent)
            
            # Generate response based on intent and context
            response = self._generate_rule_based_response(user_message, intent, context_data)
            
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
            return {
                'message': "I'm sorry, I'm having trouble processing your request right now. Please try again or contact our student services office for immediate assistance.",
                'is_urgent': False,
                'helpfulness': 0.3,
                'intent': 'error'
            }
    
    def _classify_message_intent(self, message: str) -> str:
        """Classify user message intent using keyword matching"""
        message_lower = message.lower()
        
        # Greeting patterns
        greeting_patterns = [r'\b(hello|hi|hey|good morning|good afternoon|good evening)\b']
        if any(re.search(pattern, message_lower) for pattern in greeting_patterns):
            return 'greeting'
        
        # Program-related queries
        program_keywords = ['program', 'course', 'degree', 'study', 'major', 'curriculum', 'engineering', 'it', 'computer', 'civil', 'electrical', 'mechanical', 'software']
        if any(keyword in message_lower for keyword in program_keywords):
            return 'programs'
        
        # Admission-related queries
        admission_keywords = ['admission', 'apply', 'application', 'requirement', 'deadline', 'entrance', 'enroll']
        if any(keyword in message_lower for keyword in admission_keywords):
            return 'admission'
        
        # Campus-related queries
        campus_keywords = ['campus', 'facility', 'library', 'hostel', 'cafeteria', 'sports', 'gym', 'dormitory']
        if any(keyword in message_lower for keyword in campus_keywords):
            return 'campus'
        
        # Fee-related queries
        fee_keywords = ['fee', 'cost', 'tuition', 'price', 'payment', 'financial', 'money']
        if any(keyword in message_lower for keyword in fee_keywords):
            return 'fees'
        
        # Scholarship queries
        scholarship_keywords = ['scholarship', 'financial aid', 'grant', 'funding', 'assistance']
        if any(keyword in message_lower for keyword in scholarship_keywords):
            return 'scholarships'
        
        # Fun content requests
        if any(word in message_lower for word in ['joke', 'fun', 'funny', 'laugh']):
            return 'entertainment'
        
        if any(word in message_lower for word in ['motivation', 'encourage', 'support']):
            return 'motivation'
        
        if any(word in message_lower for word in ['fact', 'interesting', 'trivia', 'news']):
            return 'news'
        
        return 'default'
    
    def _is_disallowed_request(self, message: str) -> bool:
        """Check if the request violates privacy/gossip policies"""
        disallowed_patterns = [
            r'\b(prettiest|ugliest|worst teacher|best looking|hottest)\b',
            r'\b(rank.*students|rank.*staff)\b',
            r'\b(gossip|rumors)\b',
            r'\b(personal.*information|private.*data)\b'
        ]
        
        message_lower = message.lower()
        return any(re.search(pattern, message_lower) for pattern in disallowed_patterns)
    
    def _handle_disallowed_request(self, message: str) -> Dict[str, Any]:
        """Handle requests that violate policies"""
        return {
            'message': "I can't help identify or rank private individuals by appearance or make negative claims about staff. I can help in one of these ways: (1) run an anonymous poll for campus awards, (2) show campus-approved highlights or official recognitions, (3) explain how to submit formal feedback. Which would you prefer?",
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
        elif intent == 'fees':
            context['admission'] = self.data_manager.get_admission_info()
        elif intent == 'scholarships':
            context['scholarships'] = self.data_manager.get_scholarships()
        elif intent == 'entertainment':
            context['jokes'] = self.data_manager.get_engagement_content('joke', 3)
        elif intent == 'motivation':
            context['encouragement'] = self.data_manager.get_engagement_content('encouragement', 2)
        elif intent == 'news':
            context['news'] = self.data_manager.get_latest_news(5)
            context['fun_facts'] = self.data_manager.get_engagement_content('fun_fact', 2)
        
        return context
    
    def _generate_rule_based_response(self, user_message: str, intent: str, context_data: Dict) -> str:
        """Generate response using rule-based system"""
        
        if intent == 'greeting':
            import random
            return random.choice(self.response_templates['greeting'])
        
        elif intent == 'programs':
            import random
            response = random.choice(self.response_templates['programs'])
            if 'programs' in context_data and context_data['programs']:
                # Check if user asked about a specific program
                message_lower = user_message.lower()
                specific_program = None
                for program_name, program_data in context_data['programs'].items():
                    if any(word in message_lower for word in program_name.lower().split()):
                        specific_program = program_name
                        break
                
                if specific_program:
                    # Show detailed info for specific program
                    prog_data = context_data['programs'][specific_program]
                    response = f"Here's information about {specific_program}:\n\n"
                    response += f"📚 Duration: {prog_data.get('duration', 'Not specified')}\n"
                    response += f"📝 Description: {prog_data.get('description', 'No description available')}\n"
                    response += f"🎯 Career Paths: {', '.join(prog_data.get('career_paths', ['Not specified']))}\n"
                    response += f"📋 Entry Requirements: {prog_data.get('entry_requirements', 'Contact admissions for details')}\n"
                    response += f"💰 Salary Range: {prog_data.get('salary_range', 'Contact career services for details')}\n"
                    if prog_data.get('specializations'):
                        response += f"🔬 Specializations: {', '.join(prog_data.get('specializations', []))}\n"
                else:
                    # Show list of all programs
                    programs = list(context_data['programs'].keys())[:5]
                    response += f"\n\n• {chr(10).join(['• ' + prog for prog in programs])}"
                    response += "\n\nWould you like detailed information about any specific program?"
            return response
        
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
                facilities = campus_info.get('facilities', [])
                if facilities:
                    response += f"\n\n• {chr(10).join(['• ' + facility for facility in facilities[:5]])}"
            return response
        
        elif intent == 'fees':
            import random
            response = random.choice(self.response_templates['fees'])
            if 'admission' in context_data:
                fees = context_data['admission'].get('fees', {})
                if fees:
                    response += "\n\n"
                    for fee_type, amount in fees.items():
                        response += f"• {fee_type.replace('_', ' ').title()}: {amount}\n"
            return response
        
        elif intent == 'scholarships':
            import random
            response = random.choice(self.response_templates['scholarships'])
            if 'scholarships' in context_data and context_data['scholarships']:
                scholarships = context_data['scholarships'][:3]
                response += "\n\n"
                for scholarship in scholarships:
                    response += f"• {scholarship.get('name', 'Scholarship')}: {scholarship.get('description', 'Available for eligible students')}\n"
            return response
        
        elif intent == 'entertainment':
            if 'jokes' in context_data and context_data['jokes']:
                joke = context_data['jokes'][0]
                return f"Here's a joke for you: {joke['content']}"
            else:
                return "Here's a little university humor: Why don't engineers ever get lost on campus? Because they always know how to find their way around problems! 😄"
        
        elif intent == 'motivation':
            if 'encouragement' in context_data and context_data['encouragement']:
                encouragement = context_data['encouragement'][0]
                return encouragement['content']
            else:
                return "Remember, every expert was once a beginner. Your journey at HMAWBI University is just the beginning of great achievements! Keep pushing forward! 💪"
        
        elif intent == 'news':
            response = "Here's what's happening at HMAWBI University:\n\n"
            if 'news' in context_data and context_data['news']:
                for news_item in context_data['news'][:3]:
                    response += f"• {news_item.get('title', 'University News')}: {news_item.get('content', 'Updates coming soon')}\n"
            else:
                response += "• Stay tuned for exciting university updates and announcements!\n"
            
            if 'fun_facts' in context_data and context_data['fun_facts']:
                fact = context_data['fun_facts'][0]
                response += f"\n🎓 Fun Fact: {fact['content']}"
            
            return response
        
        else:  # default
            import random
            return random.choice(self.response_templates['default'])
    
    def _analyze_response(self, user_message: str, response: str) -> Dict[str, Any]:
        """Analyze the response for urgency and helpfulness"""
        message_lower = user_message.lower()
        
        # Check for urgent keywords
        urgent_keywords = ['urgent', 'emergency', 'deadline', 'immediately', 'asap', 'help', 'problem']
        is_urgent = any(keyword in message_lower for keyword in urgent_keywords)
        
        # Calculate helpfulness based on response quality
        helpfulness = 0.8  # Default
        if len(response) < 50:
            helpfulness = 0.5
        elif "I don't have that info" in response or "I'm not sure" in response:
            helpfulness = 0.6
        elif any(word in response.lower() for word in ['contact', 'office', 'email', 'phone']):
            helpfulness = 0.9
        
        return {
            'is_urgent': is_urgent,
            'helpfulness': helpfulness
        }
    
    def get_conversation_starters(self) -> List[str]:
        """Get suggested conversation starters"""
        return [
            "What engineering programs do you offer?",
            "How can I apply for admission?",
            "What are the tuition fees?",
            "Tell me about campus facilities",
            "Are there any scholarships available?",
            "What is student life like at HMAWBI?",
            "Can you tell me a joke?",
            "What are the latest university news?"
        ]
    
    def search_programs(self, query: str) -> List[str]:
        """Search for programs based on query"""
        return self.data_manager.search_programs(query)
    
    def get_quick_responses(self, category: str) -> List[str]:
        """Get quick responses for specific categories"""
        return self.response_templates.get(category, self.response_templates['default'])


# Utility functions for testing and development
def test_chatbot():
    """Test function for development"""
    chatbot = UniversityGuidanceChatbot()
    
    test_messages = [
        "Hello",
        "Hi there",
        "What engineering programs do you offer?",
        "How can I apply for admission?",
        "Tell me a joke",
        "Who is the prettiest student?",  # Should be blocked
        "What are the campus facilities?"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        response = chatbot.generate_response(message)
        print(f"Bot: {response['message']}")
        print(f"Intent: {response.get('intent', 'unknown')}, Urgent: {response['is_urgent']}, Helpfulness: {response['helpfulness']}")


if __name__ == "__main__":
    test_chatbot()
