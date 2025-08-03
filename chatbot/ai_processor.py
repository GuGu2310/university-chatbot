
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import openai
from django.conf import settings
import nltk
from textblob import TextBlob

# Import separated data files
from .data.university_programs import UNIVERSITY_PROGRAMS, CAMPUS_INFO, ADMISSION_INFO, STUDENT_LIFE
from .data.responses_templates import (
    CONVERSATION_STARTERS, CASUAL_RESPONSES, STUDY_TIPS, CAREER_ADVICE, 
    MOTIVATIONAL_QUOTES, COMPREHENSIVE_RESPONSES, ERROR_RESPONSES,
    URGENCY_INDICATORS, RESPONSE_CATEGORIES
)
from .data.student_engagement import (
    FUNNY_JOKES, PERSONAL_ENCOURAGEMENT, CASUAL_CHATS, STUDENT_LIFE_QUOTES,
    CELEBRATION_MESSAGES, FUN_FACTS, get_joke_by_category, get_random_encouragement
)

# Download required NLTK data
try:
    nltk.download('wordnet', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except Exception as e:
    pass

logger = logging.getLogger(__name__)

# Enhanced NLTK setup
NLTK_AVAILABLE = False
try:
    import nltk
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords
    
    try:
        nltk.data.find('corpora/wordnet.zip')
        nltk.data.find('corpora/stopwords.zip')
        NLTK_AVAILABLE = True
        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))
    except LookupError:
        logger.warning("NLTK data not found. Attempting auto-download.")
        try:
            nltk.download('wordnet', quiet=True)
            nltk.download('stopwords', quiet=True)
            NLTK_AVAILABLE = True
            lemmatizer = WordNetLemmatizer()
            stop_words = set(stopwords.words('english'))
            logger.info("NLTK data downloaded successfully.")
        except Exception as e:
            logger.error(f"Failed to auto-download NLTK data: {e}")
            NLTK_AVAILABLE = False
except ImportError:
    logger.warning("NLTK not installed. Some advanced text processing will be skipped.")
    NLTK_AVAILABLE = False


class UniversityGuidanceChatbot:
    def __init__(self):
        """Initialize the Enhanced University Guidance Chatbot"""
        # Load data from separated files
        self.university_data = {
            'hmawbi_programs': UNIVERSITY_PROGRAMS,
            'campus_info': CAMPUS_INFO,
            'admission_info': ADMISSION_INFO,
            'student_life': STUDENT_LIFE
        }
        
        # Load response templates
        self.conversation_starters = CONVERSATION_STARTERS
        self.casual_responses = CASUAL_RESPONSES
        self.study_tips = STUDY_TIPS
        self.career_advice = CAREER_ADVICE
        self.motivational_quotes = MOTIVATIONAL_QUOTES
        self.comprehensive_responses = COMPREHENSIVE_RESPONSES
        self.error_responses = ERROR_RESPONSES
        self.urgency_indicators = URGENCY_INDICATORS
        self.response_categories = RESPONSE_CATEGORIES
        
        # Load student engagement content
        self.funny_jokes = FUNNY_JOKES
        self.personal_encouragement = PERSONAL_ENCOURAGEMENT
        self.casual_chats = CASUAL_CHATS
        self.student_quotes = STUDENT_LIFE_QUOTES
        self.celebration_messages = CELEBRATION_MESSAGES
        self.fun_facts = FUN_FACTS

        # Initialize OpenAI if available
        openai.api_key = getattr(settings, 'OPENAI_API_KEY', None)

        # Conversation state
        self.last_user_intent = None
        self.last_bot_intent = None
        self.turn_count = 0

        # NLTK components
        self.lemmatizer = lemmatizer if NLTK_AVAILABLE else None
        self.stop_words = stop_words if NLTK_AVAILABLE else None

    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate enhanced contextual response based on user message and conversation history"""
        user_message = user_message.lower().strip()
        self.turn_count += 1

        # Check for urgency indicators
        is_urgent = any(indicator in user_message for indicator in self.urgency_indicators)

        # Casual conversation patterns with enhanced responses
        if any(word in user_message for word in ['hello', 'hi', 'hey', 'greetings', 'start']):
            return {
                'message': random.choice(self.casual_responses['greetings']),
                'is_urgent': False,
                'helpfulness': 0.9,
                'intent': 'greeting'
            }

        if any(phrase in user_message for phrase in ['how are you', 'how do you do', 'how are things']):
            return {
                'message': random.choice(self.casual_responses['how_are_you']),
                'is_urgent': False,
                'helpfulness': 0.8,
                'intent': 'casual_inquiry'
            }

        if any(word in user_message for word in ['thank', 'thanks', 'appreciate']):
            response = random.choice(self.casual_responses['thank_you'])
            if random.choice([True, False]):
                response += f"\n\n💡 {random.choice(self.motivational_quotes)}"
            return {
                'message': response,
                'is_urgent': False,
                'helpfulness': 0.9,
                'intent': 'gratitude'
            }

        if any(word in user_message for word in ['bye', 'goodbye', 'see you', 'farewell']):
            return {
                'message': random.choice(self.casual_responses['goodbye']),
                'is_urgent': False,
                'helpfulness': 0.8,
                'intent': 'farewell'
            }

        # Fun content and jokes
        if any(word in user_message for word in ['joke', 'funny', 'humor', 'laugh', 'fun']):
            return self._handle_fun_content(user_message, is_urgent)

        # Personal encouragement and motivation
        if any(word in user_message for word in ['stressed', 'tired', 'difficult', 'hard', 'struggling']):
            return self._handle_personal_support(user_message, is_urgent)

        # Enhanced category-based responses
        detected_category = self._detect_category(user_message)
        
        if detected_category == 'programs':
            return self._handle_program_query(user_message, is_urgent)
        elif detected_category == 'admissions':
            return self._handle_admission_query(user_message, is_urgent)
        elif detected_category == 'campus':
            return self._handle_campus_query(user_message, is_urgent)
        elif detected_category == 'career':
            return self._handle_career_query(user_message, is_urgent)
        elif detected_category == 'academic':
            return self._handle_study_query(user_message, is_urgent)
        elif detected_category == 'financial':
            return self._handle_financial_query(user_message, is_urgent)
        elif detected_category == 'student_life':
            return self._handle_student_life_query(user_message, is_urgent)

        # Enhanced default response
        helpfulness = self._analyze_helpfulness(user_message)
        return {
            'message': self._generate_comprehensive_response(user_message),
            'is_urgent': is_urgent,
            'helpfulness': helpfulness,
            'intent': 'general_inquiry'
        }

    def _detect_category(self, user_message: str) -> str:
        """Enhanced category detection with weighted scoring"""
        category_scores = {}
        
        for category, keywords in self.response_categories.items():
            score = 0
            for keyword in keywords:
                if keyword in user_message:
                    # Weight longer keywords more heavily
                    score += len(keyword.split())
            category_scores[category] = score
        
        if not any(category_scores.values()):
            return 'general'
            
        return max(category_scores, key=category_scores.get)

    def _handle_program_query(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Enhanced program-related query handling"""
        programs = list(self.university_data['hmawbi_programs'].keys())
        
        # Check for specific program mentioned
        mentioned_program = None
        for program in programs:
            if program.lower() in user_message:
                mentioned_program = program
                break

        if mentioned_program:
            program_info = self.university_data['hmawbi_programs'][mentioned_program]
            response = f"🎓 **{mentioned_program}** at HMAWBI University\n\n"
            response += f"⏱️ **Duration**: {program_info['duration']}\n"
            response += f"📖 **Description**: {program_info['description']}\n\n"
            
            response += f"💼 **Career Opportunities**:\n"
            for career in program_info['career_paths'][:4]:
                response += f"• {career}\n"
            
            response += f"\n💰 **Salary Range**: {program_info['salary_range']}\n"
            response += f"📋 **Entry Requirements**: {program_info['entry_requirements']}\n\n"
            
            response += f"🔬 **Key Subjects**: {', '.join(program_info['subjects'][:5])}...\n"
            response += f"📈 **Job Prospects**: {program_info['job_prospects']}\n\n"
            
            if 'specializations' in program_info:
                response += f"🎯 **Specializations**: {', '.join(program_info['specializations'])}\n\n"
            
            response += "💡 *Want to know more about admission requirements or other programs? Just ask!*"
        else:
            response = "🎓 **Engineering Programs at HMAWBI University**\n\n"
            for i, (program, info) in enumerate(self.university_data['hmawbi_programs'].items(), 1):
                icon = "🏗️" if "Civil" in program else "⚡" if "Electrical" in program else "💻" if "IT" in program else "🔧" if "Mechanical" in program else "🏛️" if "Architecture" in program else "🤖"
                response += f"{icon} **{program}**\n"
                response += f"   Duration: {info['duration']}\n"
                response += f"   Salary: {info['salary_range']}\n\n"
            
            response += "🔍 *Ask me about any specific program for detailed information!*\n"
            response += f"💡 *Quick tip: {random.choice(self.study_tips)}*"

        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.95,
            'intent': 'program_inquiry'
        }

    def _handle_admission_query(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Enhanced admission-related query handling"""
        admission = self.university_data['admission_info']
        
        response = "📝 **HMAWBI University Admission Guide**\n\n"
        
        # Application process
        response += "🗓️ **Important Dates & Process**:\n"
        response += f"• Application Deadline: **{admission['application_process']['deadline']}**\n"
        response += f"• Entrance Exam: {admission['application_process']['entrance_exam']}\n"
        response += f"• Interview: {admission['application_process']['interview']}\n\n"
        
        # Required documents
        response += "📋 **Required Documents**:\n"
        for i, doc in enumerate(admission['required_documents'][:5], 1):
            response += f"{i}. {doc}\n"
        if len(admission['required_documents']) > 5:
            response += f"...and {len(admission['required_documents']) - 5} more documents\n"
        
        # Fees overview
        response += f"\n💳 **Cost Overview**:\n"
        response += f"• Application Fee: {admission['fees']['application']}\n"
        response += f"• Annual Tuition: {admission['fees']['tuition_per_year']}\n"
        response += f"• Accommodation: {admission['fees']['hostel']}\n\n"
        
        # Scholarships
        response += "🏆 **Scholarship Opportunities**:\n"
        for scholarship in admission['scholarships'][:3]:
            response += f"• **{scholarship['name']}**: {scholarship['description']}\n"
        
        if is_urgent:
            response += f"\n⚠️ **Urgent Notice**: Don't miss the {admission['application_process']['deadline']} deadline!\n"
        
        response += "\n💡 *Need help with your application? I can guide you through each step!*"

        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.95,
            'intent': 'admission_inquiry'
        }

    def _handle_campus_query(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Enhanced campus and facilities query handling"""
        campus = self.university_data['campus_info']
        
        response = "🏫 **HMAWBI University Campus**\n\n"
        
        # Location info
        response += f"📍 **Location**: {campus['location']['address']}\n"
        response += f"🌳 **Campus Size**: {campus['location']['campus_size']}\n"
        response += f"📅 **Established**: {campus['location']['established']}\n\n"
        
        # Key facilities
        response += "🏗️ **Campus Facilities**:\n"
        facilities = campus['facilities']
        response += f"📚 **Library**: {facilities['libraries']}\n"
        response += f"🔬 **Labs**: {facilities['laboratories']}\n"
        response += f"🏠 **Housing**: {facilities['dormitories']}\n"
        response += f"⚽ **Sports**: {facilities['sports']}\n"
        response += f"🍽️ **Dining**: {facilities['dining']}\n"
        response += f"🏥 **Medical**: {facilities['medical']}\n"
        response += f"🚌 **Transport**: {facilities['transportation']}\n"
        response += f"📶 **Internet**: {facilities['wifi']}\n\n"
        
        # Student services
        if 'student_services' in campus:
            response += "🎯 **Student Support Services**:\n"
            for service, description in campus['student_services'].items():
                response += f"• **{service.replace('_', ' ').title()}**: {description}\n"
        
        response += "\n🌟 *Our campus provides everything you need for a comfortable and productive university experience!*"

        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.9,
            'intent': 'campus_inquiry'
        }

    def _handle_career_query(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Enhanced career and job-related query handling"""
        response = "💼 **Career Success at HMAWBI University**\n\n"

        # Salary ranges
        response += "💰 **Expected Salary Ranges**:\n"
        for program, info in self.university_data['hmawbi_programs'].items():
            icon = "🏗️" if "Civil" in program else "⚡" if "Electrical" in program else "💻" if "IT" in program else "🔧"
            response += f"{icon} **{program}**: {info['salary_range']}\n"

        # Career advice
        response += f"\n🎯 **Success Strategies**:\n"
        selected_advice = random.sample(self.career_advice, 3)
        for advice in selected_advice:
            response += f"• {advice}\n"

        # Industry connections
        response += "\n🏢 **Industry Partners & Employers**:\n"
        response += "• Myanmar Engineering Society\n"
        response += "• International construction companies\n"
        response += "• Leading tech startups and MNCs\n"
        response += "• Government infrastructure projects\n"
        response += "• Regional manufacturing companies\n"

        # Practical experience
        student_life = self.university_data['student_life']
        if 'academic_programs' in student_life:
            response += f"\n🚀 **Practical Experience**:\n"
            response += f"• {student_life['academic_programs']['internships']}\n"
            response += f"• {student_life['academic_programs']['research']}\n"
            response += f"• {student_life['academic_programs']['projects']}\n"

        response += f"\n💡 *{random.choice(self.motivational_quotes)}*"

        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.9,
            'intent': 'career_inquiry'
        }

    def _handle_study_query(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Enhanced study tips and academic help query handling"""
        response = "📚 **Academic Success at HMAWBI**\n\n"
        
        # Study tips
        response += "✅ **Proven Study Strategies**:\n"
        selected_tips = random.sample(self.study_tips, 4)
        for tip in selected_tips:
            response += f"• {tip}\n"

        # Academic resources
        response += "\n🎯 **Academic Support Resources**:\n"
        response += "• 📖 Comprehensive digital library with 24/7 access\n"
        response += "• 👥 Peer tutoring programs for challenging subjects\n"
        response += "• 🏫 Professor office hours and academic mentoring\n"
        response += "• 💻 Online learning platforms and simulation software\n"
        response += "• 🔬 State-of-the-art laboratory facilities\n"
        response += "• 📊 Study groups and collaborative learning spaces\n"

        # Student support
        student_life = self.university_data['student_life']
        if 'support_services' in student_life:
            response += "\n🤝 **Student Support Services**:\n"
            for service, description in student_life['support_services'].items():
                response += f"• **{service.title()}**: {description}\n"

        if is_urgent:
            response += "\n⚠️ **Need immediate help?** Visit the tutoring center or contact your academic advisor!\n"

        response += f"\n🌟 *{random.choice(self.motivational_quotes)}*"

        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.85,
            'intent': 'academic_inquiry'
        }

    def _handle_financial_query(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Enhanced financial query handling"""
        admission = self.university_data['admission_info']
        fees = admission['fees']
        scholarships = admission['scholarships']

        response = "💰 **Financial Information & Support**\n\n"
        
        # Comprehensive cost breakdown
        response += "📊 **Complete Cost Breakdown (Annual)**:\n"
        total_cost = 0
        for fee_type, amount in fees.items():
            if fee_type != 'application':
                amount_num = int(''.join(filter(str.isdigit, amount)))
                total_cost += amount_num
                response += f"• {fee_type.replace('_', ' ').title()}: {amount}\n"
        
        response += f"\n💳 **Total Annual Cost**: ~{total_cost:,} MMK\n"
        response += f"📝 **One-time Application Fee**: {fees['application']}\n\n"

        # Scholarship opportunities
        response += "🏆 **Scholarship Programs**:\n"
        for scholarship in scholarships:
            response += f"• **{scholarship['name']}**\n"
            response += f"  {scholarship['description']}\n"
            response += f"  *Criteria: {scholarship['criteria']}*\n\n"

        # Financial planning tips
        response += "💡 **Financial Planning Tips**:\n"
        response += "• 📅 Apply early for maximum scholarship consideration\n"
        response += "• 💼 Consider work-study programs and campus jobs\n"
        response += "• 🏦 Explore government education loan options\n"
        response += "• 👨‍🏫 Look into part-time tutoring opportunities\n"
        response += "• 💰 Budget for books, supplies, and personal expenses\n"

        if is_urgent:
            response += f"\n⚠️ **Financial Deadline Alert**: Scholarship applications due {admission['application_process']['deadline']}!\n"

        response += "\n🎯 *Need personalized financial planning help? I can provide more detailed guidance!*"

        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.9,
            'intent': 'financial_inquiry'
        }

    def _handle_student_life_query(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Enhanced student life and activities query handling"""
        student_life = self.university_data['student_life']

        response = "🎓 **Vibrant Student Life at HMAWBI**\n\n"

        # Student organizations
        response += "🏛️ **Student Organizations & Clubs**:\n"
        for club in student_life['clubs_organizations']:
            response += f"• **{club['name']}**\n"
            response += f"  {club['description']}\n"
            response += f"  Activities: {', '.join(club['activities'])}\n\n"

        # Annual events
        response += "🎉 **Major Annual Events**:\n"
        for event in student_life['annual_events']:
            response += f"• **{event['name']}** ({event['period']})\n"
            response += f"  {event['description']}\n\n"

        # Academic enrichment
        if 'academic_programs' in student_life:
            response += "🚀 **Academic Enrichment Programs**:\n"
            for program, description in student_life['academic_programs'].items():
                response += f"• **{program.title()}**: {description}\n"

        # Why students love HMAWBI
        response += "\n🌟 **Why Students Love HMAWBI**:\n"
        response += "• 🤝 Strong sense of community and belonging\n"
        response += "• 🌐 Extensive alumni network across industries\n"
        response += "• 🏗️ Hands-on learning with real-world projects\n"
        response += "• 🌳 Beautiful, modern campus in peaceful Hmawbi\n"
        response += "• 👨‍🏫 Supportive faculty with industry experience\n"
        response += "• 🚀 Innovation-focused learning environment\n"

        response += "\n💫 *Ready to join our amazing community? Ask me about any specific activity or how to get involved!*"

        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.85,
            'intent': 'student_life_inquiry'
        }

    def _generate_comprehensive_response(self, user_message: str) -> str:
        """Generate enhanced comprehensive response for general queries"""
        return random.choice(self.comprehensive_responses)

    def _handle_fun_content(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Handle requests for jokes and fun content"""
        response = "😄 **Time for Some Engineering Fun!** 🎉\n\n"
        
        # Detect specific engineering category for targeted jokes
        program_keywords = {
            'civil': ['civil', 'construction', 'building'],
            'electrical': ['electrical', 'power', 'energy'],
            'mechanical': ['mechanical', 'machine', 'automotive'],
            'it': ['programming', 'computer', 'software', 'coding'],
            'architecture': ['architecture', 'design'],
            'mechatronics': ['robotics', 'automation', 'robot']
        }
        
        joke_category = "general"
        for category, keywords in program_keywords.items():
            if any(keyword in user_message for keyword in keywords):
                joke_category = category
                break
        
        # Get jokes by category or random
        relevant_jokes = get_joke_by_category(joke_category)
        if not relevant_jokes:
            relevant_jokes = self.funny_jokes
        
        # Select and format jokes
        selected_jokes = random.sample(relevant_jokes, min(2, len(relevant_jokes)))
        
        for i, joke in enumerate(selected_jokes, 1):
            response += f"**Joke #{i}:**\n"
            response += f"Q: {joke['setup']}\n"
            response += f"A: {joke['punchline']}\n\n"
        
        # Add a fun fact
        response += f"🤓 **Bonus Fun Fact:**\n{random.choice(self.fun_facts)}\n\n"
        
        # Add encouraging note
        response += f"💡 {random.choice(self.student_quotes)}"
        
        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.85,
            'intent': 'entertainment'
        }

    def _handle_personal_support(self, user_message: str, is_urgent: bool = False) -> Dict[str, Any]:
        """Handle personal encouragement and emotional support"""
        response = "💙 **You're Not Alone in This Journey!** 🌟\n\n"
        
        # Detect context for targeted encouragement
        if any(word in user_message for word in ['exam', 'test', 'grade']):
            context = 'exam_stress'
        elif any(word in user_message for word in ['assignment', 'project', 'homework']):
            context = 'academic_struggle'
        elif any(word in user_message for word in ['tired', 'exhausted', 'sleepy']):
            context = 'general'
        else:
            context = 'general'
        
        # Get relevant encouragement
        relevant_encouragement = get_random_encouragement(context)
        if not relevant_encouragement:
            relevant_encouragement = self.personal_encouragement
        
        # Select encouraging messages
        selected_msg = random.choice(relevant_encouragement)
        response += f"{selected_msg['message']}\n\n"
        
        # Add practical tips
        response += "🎯 **Quick Mood Boosters:**\n"
        response += "• Take 5 deep breaths and stretch 🧘‍♀️\n"
        response += "• Grab a healthy snack and water 🍎💧\n"
        response += "• Chat with a friend or family member 👥\n"
        response += "• Take a 10-minute walk outside 🚶‍♂️\n"
        response += "• Listen to your favorite music 🎵\n\n"
        
        # Add motivational quote
        response += f"✨ **Remember:** {random.choice(self.student_quotes)}\n\n"
        
        # Check for casual chat triggers
        for chat in self.casual_chats:
            if any(trigger in user_message for trigger in chat['trigger']):
                response += f"💬 {random.choice(chat['responses'])}\n\n"
                break
        
        response += "🤗 **I'm here whenever you need support! Feel free to chat anytime!**"
        
        return {
            'message': response,
            'is_urgent': is_urgent,
            'helpfulness': 0.9,
            'intent': 'emotional_support'
        }

    def _analyze_helpfulness(self, message: str) -> float:
        """Enhanced sentiment analysis for helpfulness"""
        try:
            blob = TextBlob(message)
            sentiment = blob.sentiment.polarity
            
            # Adjust sentiment based on question complexity
            question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'who']
            question_count = sum(1 for word in question_words if word in message.lower())
            
            # More complex questions get higher helpfulness scores
            complexity_bonus = min(question_count * 0.1, 0.3)
            
            return max(0.1, min(1.0, 0.7 + sentiment * 0.2 + complexity_bonus))
        except Exception as e:
            logger.error(f"Sentiment analysis error: {e}")
            return 0.7  # Default moderate helpfulness
