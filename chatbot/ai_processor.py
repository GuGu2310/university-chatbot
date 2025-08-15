
"""
AI Processor for HMAWBI University Chatbot
Handles conversation processing and response generation using OpenAI
"""

import os
import openai
from typing import Dict, List, Any, Optional
from django.conf import settings
from .data_manager import DataManager
import logging
import json
import re

logger = logging.getLogger(__name__)

class UniversityGuidanceChatbot:
    """
    University Guidance Chatbot using OpenAI GPT for intelligent responses
    Follows the UniGuideBot specifications for university assistance
    """
    
    def __init__(self):
        """Initialize the chatbot with OpenAI configuration"""
        self.api_key = getattr(settings, 'OPENAI_API_KEY', '')
        if self.api_key:
            openai.api_key = self.api_key
        
        self.data_manager = DataManager()
        self.system_prompt = self._get_system_prompt()
        self.temperature = 0.15
        self.max_tokens = 600
        
    def _get_system_prompt(self) -> str:
        """Get the comprehensive system prompt for UniGuideBot"""
        return """You are "UniGuideBot," the official HMAWBI University guidance assistant. Your role is to give accurate, helpful, and neutral information about the university: organization, departments, programs, admission dates and requirements, tuition and fees, location and campus map, events and student activities, clubs, facilities, transport options, exams/announcements, job/internship opportunities, partnerships, scholarships, and other student services.

Always:
- Use a friendly, concise, professional tone
- Answer from the university knowledge base when available. If you are not sure, say "I don't have that info right now" and offer to find it or provide the next steps
- Ask a clarifying question if the user request is incomplete
- Respect privacy and safety: never produce content that identifies private individuals in a defamatory way
- For "fun news" / gossip: only publish content that is campus-official, aggregated anonymous poll results, or clearly labeled fiction
- Provide sources for factual answers when possible
- If user needs official action (complaint, discipline, legal), provide the relevant office contact and recommend filing an official report
- When asked about events, ask whether they want dates, registration, or directions
- If the user is a prospective student, include admission deadlines, required documents, contacts, and next steps
- Indicate escalation to human office when necessary

For disallowed requests (identifying/ranking individuals), politely refuse and offer alternatives like anonymous polls or campus-approved highlights."""

    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Generate a response to user message using OpenAI
        
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
            
            # Get relevant university data for context
            context_data = self._get_relevant_context(user_message)
            
            # Build messages for OpenAI
            messages = self._build_messages(user_message, conversation_history, context_data)
            
            # Generate response using OpenAI
            if self.api_key:
                response = self._call_openai(messages)
            else:
                response = self._fallback_response(user_message, context_data)
            
            # Analyze response for urgency and helpfulness
            analysis = self._analyze_response(user_message, response)
            
            return {
                'message': response,
                'is_urgent': analysis.get('is_urgent', False),
                'helpfulness': analysis.get('helpfulness', 0.8),
                'context_used': bool(context_data)
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'message': "I'm sorry, I'm having trouble processing your request right now. Please try again or contact our student services office for immediate assistance.",
                'is_urgent': False,
                'helpfulness': 0.3
            }
    
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
            'helpfulness': 0.6
        }
    
    def _get_relevant_context(self, user_message: str) -> Dict[str, Any]:
        """Get relevant university data based on user message"""
        context = {}
        message_lower = user_message.lower()
        
        # Check for program-related queries
        if any(word in message_lower for word in ['program', 'degree', 'course', 'study', 'major']):
            context['programs'] = self.data_manager.get_all_programs()
        
        # Check for admission-related queries
        if any(word in message_lower for word in ['admission', 'apply', 'requirement', 'deadline', 'entrance']):
            context['admission'] = self.data_manager.get_admission_info()
        
        # Check for campus-related queries
        if any(word in message_lower for word in ['campus', 'facility', 'library', 'hostel', 'cafeteria']):
            context['campus'] = self.data_manager.get_campus_info()
        
        # Check for news-related queries
        if any(word in message_lower for word in ['news', 'announcement', 'event', 'happening']):
            context['news'] = self.data_manager.get_latest_news(5)
        
        # Check for fun content requests
        if any(word in message_lower for word in ['joke', 'fun', 'funny', 'laugh']):
            context['jokes'] = self.data_manager.get_engagement_content('joke', 3)
        
        if any(word in message_lower for word in ['motivation', 'encourage', 'support', 'help']):
            context['encouragement'] = self.data_manager.get_engagement_content('encouragement', 2)
        
        if any(word in message_lower for word in ['fact', 'interesting', 'trivia']):
            context['fun_facts'] = self.data_manager.get_engagement_content('fun_fact', 2)
        
        return context
    
    def _build_messages(self, user_message: str, conversation_history: List[Dict], context_data: Dict) -> List[Dict]:
        """Build message array for OpenAI API"""
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add conversation history if available
        if conversation_history:
            messages.extend(conversation_history[-6:])  # Last 6 messages for context
        
        # Add context data as system message
        if context_data:
            context_message = "Here's relevant university information to help answer the user:\n"
            for key, value in context_data.items():
                context_message += f"\n{key.upper()}:\n{json.dumps(value, indent=2)}\n"
            
            messages.append({"role": "system", "content": context_message})
        
        # Add user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def _call_openai(self, messages: List[Dict]) -> str:
        """Call OpenAI API to generate response"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use gpt-4 if available
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _fallback_response(self, user_message: str, context_data: Dict) -> str:
        """Generate fallback response when OpenAI is not available"""
        message_lower = user_message.lower()
        
        # Program queries
        if 'program' in message_lower or 'course' in message_lower:
            programs = self.data_manager.get_all_programs()
            if programs:
                program_names = list(programs.keys())[:5]
                return f"We offer several programs including: {', '.join(program_names)}. Would you like detailed information about any specific program?"
        
        # Admission queries
        if 'admission' in message_lower or 'apply' in message_lower:
            admission_info = self.data_manager.get_admission_info()
            return f"For admissions, you can contact us at: {admission_info.get('contact_email', 'admissions@hmawbi.edu.mm')}. Visit our admissions office during {admission_info.get('office_hours', 'business hours')}."
        
        # Fun content
        if 'joke' in message_lower:
            jokes = self.data_manager.get_engagement_content('joke', 1)
            if jokes:
                joke = jokes[0]
                if 'title' in joke:
                    return f"Here's a joke for you: {joke['content']}"
                else:
                    return f"Here's a joke for you: {joke['content']}"
        
        # Default response
        return "Thank you for your question! I'm here to help with information about HMAWBI University programs, admissions, campus facilities, and student services. Could you please be more specific about what you'd like to know?"
    
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
        responses = {
            'greeting': [
                "Hello! I'm UniGuideBot, your HMAWBI University assistant. How can I help you today?",
                "Welcome to HMAWBI University! What would you like to know about our programs and services?",
                "Hi there! I'm here to help with any questions about university life, admissions, or programs."
            ],
            'goodbye': [
                "Thank you for visiting HMAWBI University! Feel free to reach out anytime you need assistance.",
                "Goodbye! Best of luck with your academic journey at HMAWBI University!",
                "Take care! I'm always here if you need more information about our university."
            ],
            'thanks': [
                "You're welcome! Is there anything else I can help you with?",
                "Happy to help! Feel free to ask if you have more questions.",
                "Glad I could assist! Let me know if you need anything else."
            ]
        }
        return responses.get(category, [])


# Utility functions for testing and development
def test_chatbot():
    """Test function for development"""
    chatbot = UniversityGuidanceChatbot()
    
    test_messages = [
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
        print(f"Urgent: {response['is_urgent']}, Helpfulness: {response['helpfulness']}")


if __name__ == "__main__":
    test_chatbot()
