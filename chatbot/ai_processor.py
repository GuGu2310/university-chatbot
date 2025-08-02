import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import openai
from django.conf import settings
import nltk

# Download WordNet if it's not already downloaded
nltk.download('wordnet')
logger = logging.getLogger(__name__)

# For enhanced tokenization/lemmatization (if NLTK is available, otherwise fallback)
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
        logger.warning(
            "NLTK data (wordnet/stopwords) not found. Attempting auto-download."
        )
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
    logger.warning(
        "NLTK not installed. Some advanced text processing will be skipped.")
    NLTK_AVAILABLE = False


class UniversityGuidanceChatbot:
    def __init__(self):
        """Initialize the University Guidance Chatbot with comprehensive knowledge base"""
        self.university_data = {
            "hmawbi_programs": {
                "Civil Engineering": {
                    "duration": "5 years",
                    "description": "Design and construction of infrastructure projects including roads, bridges, buildings, and water systems",
                    "career_paths": ["Structural Engineer", "Construction Manager", "Urban Planner", "Project Manager"],
                    "entry_requirements": "Mathematics, Physics, Chemistry with minimum 75% marks",
                    "subjects": ["Structural Analysis", "Concrete Technology", "Soil Mechanics", "Highway Engineering", "Construction Management"],
                    "job_prospects": "High demand in Myanmar's infrastructure development projects",
                    "salary_range": "500,000 - 2,000,000 MMK per month"
                },
                "Mechanical Engineering": {
                    "duration": "5 years",
                    "description": "Design, development, and manufacturing of mechanical systems and machinery",
                    "career_paths": ["Mechanical Design Engineer", "Manufacturing Engineer", "Automotive Engineer", "HVAC Engineer"],
                    "entry_requirements": "Mathematics, Physics with minimum 75% marks",
                    "subjects": ["Thermodynamics", "Machine Design", "Manufacturing Processes", "Fluid Mechanics", "Control Systems"],
                    "job_prospects": "Growing opportunities in manufacturing and automotive sectors",
                    "salary_range": "600,000 - 2,500,000 MMK per month"
                },
                "Electrical Engineering": {
                    "duration": "5 years",
                    "description": "Power systems, electronics, telecommunications, and electrical infrastructure",
                    "career_paths": ["Power Engineer", "Electronics Engineer", "Telecommunications Engineer", "Control Systems Engineer"],
                    "entry_requirements": "Mathematics, Physics with minimum 75% marks",
                    "subjects": ["Circuit Analysis", "Power Systems", "Digital Electronics", "Microprocessors", "Signal Processing"],
                    "job_prospects": "Excellent opportunities in power generation and telecommunications",
                    "salary_range": "700,000 - 3,000,000 MMK per month"
                },
                "Computer Engineering": {
                    "duration": "5 years",
                    "description": "Hardware and software systems, computer networks, and embedded systems",
                    "career_paths": ["Software Engineer", "Network Engineer", "Systems Analyst", "IT Consultant"],
                    "entry_requirements": "Mathematics, Physics with minimum 75% marks",
                    "subjects": ["Programming", "Computer Networks", "Database Systems", "Software Engineering", "Cybersecurity"],
                    "job_prospects": "Very high demand in IT sector and digital transformation",
                    "salary_range": "800,000 - 4,000,000 MMK per month"
                },
                "Electronic Engineering": {
                    "duration": "5 years",
                    "description": "Electronic devices, circuits, communication systems, and automation",
                    "career_paths": ["Electronics Design Engineer", "Test Engineer", "R&D Engineer", "Technical Sales Engineer"],
                    "entry_requirements": "Mathematics, Physics with minimum 75% marks",
                    "subjects": ["Analog Electronics", "Digital Systems", "Communication Systems", "Embedded Systems", "VLSI Design"],
                    "job_prospects": "Growing field with automation and IoT development",
                    "salary_range": "650,000 - 2,800,000 MMK per month"
                },
                "Chemical Engineering": {
                    "duration": "5 years",
                    "description": "Chemical processes, manufacturing, petroleum refining, and environmental engineering",
                    "career_paths": ["Process Engineer", "Chemical Plant Manager", "Environmental Engineer", "Research Scientist"],
                    "entry_requirements": "Mathematics, Physics, Chemistry with minimum 75% marks",
                    "subjects": ["Chemical Process Design", "Thermodynamics", "Mass Transfer", "Reaction Engineering", "Process Control"],
                    "job_prospects": "Opportunities in oil & gas, pharmaceuticals, and chemical industries",
                    "salary_range": "750,000 - 3,500,000 MMK per month"
                }
            },
            "admission_info": {
                "application_deadline": "June 30th each year",
                "entrance_exam": "University Entrance Examination (UEE) required",
                "required_documents": ["High School Certificate", "Transcript", "Recommendation Letters", "Medical Certificate"],
                "fees": {
                    "application": "50,000 MMK",
                    "tuition_per_year": "1,500,000 MMK",
                    "hostel": "600,000 MMK per year",
                    "meal_plan": "800,000 MMK per year"
                },
                "scholarships": [
                    "Merit-based scholarships (50% tuition reduction)",
                    "Need-based financial aid",
                    "Government scholarships for outstanding students",
                    "Industry-sponsored scholarships"
                ]
            },
            "campus_facilities": {
                "libraries": "Central Library with 100,000+ books and digital resources",
                "laboratories": "State-of-the-art labs for each engineering discipline",
                "dormitories": "On-campus housing for 2,000+ students",
                "sports": "Football field, basketball courts, swimming pool, gymnasium",
                "dining": "Multiple cafeterias serving local and international cuisine",
                "medical": "Campus health center with 24/7 emergency services",
                "transportation": "Free shuttle service to Yangon city center",
                "wifi": "High-speed internet across entire campus"
            },
            "student_life": {
                "clubs": ["Engineering Society", "Robotics Club", "Photography Club", "Debate Society", "Cultural Club"],
                "events": ["Annual Tech Festival", "Engineering Day", "Cultural Night", "Sports Week", "Career Fair"],
                "internships": "Mandatory 6-month internship program with industry partners",
                "research": "Undergraduate research opportunities with faculty"
            }
        }

        self.conversation_starters = [
            "Hi! I'm here to help you with everything about HMAWBI Technological University!",
            "Hello! Ready to explore your engineering future at HMAWBI?",
            "Welcome! I can help you with admissions, programs, and student life at HMAWBI.",
            "Greetings! Let's discuss your path to becoming an engineer at HMAWBI University!"
        ]

        self.casual_responses = {
            "greetings": [
                "Hello! Great to meet you! What would you like to know about HMAWBI University?",
                "Hi there! I'm excited to help you explore engineering opportunities at HMAWBI!",
                "Welcome! I'm your guide to everything HMAWBI Technological University!"
            ],
            "how_are_you": [
                "I'm doing great, thank you! I love helping students like you discover amazing opportunities at HMAWBI!",
                "I'm fantastic! Every day I get to help students plan their engineering careers - it's awesome!",
                "I'm wonderful! Ready to chat about your future at HMAWBI University?"
            ],
            "thank_you": [
                "You're very welcome! I'm here whenever you need guidance about HMAWBI!",
                "Happy to help! Feel free to ask me anything else about university life or programs!",
                "My pleasure! That's what I'm here for - helping you succeed at HMAWBI!"
            ]
        }

        self.study_tips = [
            "Form study groups with classmates - engineering is better learned together!",
            "Practice coding daily if you're in Computer/Electronic Engineering",
            "Visit the lab frequently to get hands-on experience with equipment",
            "Join the Engineering Society to network with seniors and professionals",
            "Attend guest lectures by industry experts - they're incredibly valuable!",
            "Start working on projects early - don't wait until the deadline!",
            "Use office hours to connect with professors - they love helping dedicated students!"
        ]

        self.career_advice = [
            "Internships are crucial - they often lead to job offers after graduation!",
            "Build a portfolio of projects to showcase your skills to employers",
            "Learn both technical and soft skills - communication is key in engineering",
            "Consider specializing in emerging fields like renewable energy or AI",
            "Network with alumni - HMAWBI has graduates in top companies worldwide!",
            "Stay updated with industry trends through professional journals and conferences",
            "Consider pursuing certifications alongside your degree for competitive advantage"
        ]

        openai.api_key = getattr(settings, 'OPENAI_API_KEY', None)

        self.last_user_intent = None
        self.last_bot_intent = None
        self.turn_count = 0

        self.lemmatizer = lemmatizer if NLTK_AVAILABLE else None
        self.stop_words = stop_words if NLTK_AVAILABLE else None

    def generate_response(self, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """Generate contextual response based on user message and conversation history"""
        user_message = user_message.lower().strip()

        # Casual conversation patterns
        if any(word in user_message for word in ['hello', 'hi', 'hey', 'greetings']):
            return {
                'message': random.choice(self.casual_responses['greetings']),
                'is_urgent': False,
                'helpfulness': 0.9
            }

        if any(phrase in user_message for phrase in ['how are you', 'how do you do', 'how are things']):
            return {
                'message': random.choice(self.casual_responses['how_are_you']),
                'is_urgent': False,
                'helpfulness': 0.8
            }

        if any(word in user_message for word in ['thank', 'thanks', 'appreciate']):
            return {
                'message': random.choice(self.casual_responses['thank_you']),
                'is_urgent': False,
                'helpfulness': 0.9
            }

        # Program-specific queries
        if any(word in user_message for word in ['program', 'course', 'degree', 'study']):
            return self._handle_program_query(user_message)

        # Admission queries
        if any(word in user_message for word in ['admission', 'apply', 'application', 'requirements', 'deadline']):
            return self._handle_admission_query(user_message)

        # Campus and facilities
        if any(word in user_message for word in ['campus', 'facilities', 'library', 'hostel', 'dorm']):
            return self._handle_campus_query(user_message)

        # Career and job prospects
        if any(word in user_message for word in ['career', 'job', 'salary', 'employment', 'prospects']):
            return self._handle_career_query(user_message)

        # Study and academic help
        if any(word in user_message for word in ['study', 'tips', 'help', 'academic', 'exam']):
            return self._handle_study_query(user_message)

        # Fees and financial
        if any(word in user_message for word in ['fee', 'cost', 'money', 'scholarship', 'financial']):
            return self._handle_financial_query(user_message)

        # Student life
        if any(word in user_message for word in ['student life', 'clubs', 'activities', 'events']):
            return self._handle_student_life_query(user_message)

        self.turn_count += 1

        helpfulness = self.analyze_helpfulness(user_message)
        if any(word in user_message for word in ['urgent', 'emergency']):
            is_urgent = True
        else:
            is_urgent = False
        # Default comprehensive response
        return {
            'message': self._generate_comprehensive_response(user_message),
            'is_urgent': is_urgent,
            'helpfulness': helpfulness
        }

    def _handle_program_query(self, user_message: str) -> Dict[str, Any]:
        """Handle program-related queries"""
        programs = list(self.university_data['hmawbi_programs'].keys())

        # Check if specific program mentioned
        mentioned_program = None
        for program in programs:
            if program.lower() in user_message:
                mentioned_program = program
                break

        if mentioned_program:
            program_info = self.university_data['hmawbi_programs'][mentioned_program]
            response = f"**{mentioned_program}** at HMAWBI University:\n\n"
            response += f"📚 **Duration**: {program_info['duration']}\n"
            response += f"📖 **Description**: {program_info['description']}\n\n"
            response += f"💼 **Career Paths**: {', '.join(program_info['career_paths'])}\n"
            response += f"💰 **Salary Range**: {program_info['salary_range']}\n\n"
            response += f"📋 **Entry Requirements**: {program_info['entry_requirements']}\n\n"
            response += f"🔬 **Key Subjects**: {', '.join(program_info['subjects'])}\n\n"
            response += f"📈 **Job Prospects**: {program_info['job_prospects']}"
        else:
            response = "🎓 **Engineering Programs at HMAWBI University**:\n\n"
            for i, program in enumerate(programs, 1):
                response += f"{i}. **{program}** - {self.university_data['hmawbi_programs'][program]['description'][:60]}...\n"
            response += "\nAsk me about any specific program for detailed information!"

        return {
            'message': response,
            'is_urgent': False,
            'helpfulness': 0.95
        }

    def _handle_admission_query(self, user_message: str) -> Dict[str, Any]:
        """Handle admission-related queries"""
        admission = self.university_data['admission_info']

        response = "📝 **HMAWBI University Admission Information**:\n\n"
        response += f"📅 **Application Deadline**: {admission['application_deadline']}\n"
        response += f"📊 **Entrance Exam**: {admission['entrance_exam']}\n\n"
        response += "📋 **Required Documents**:\n"
        for doc in admission['required_documents']:
            response += f"• {doc}\n"
        response += f"\n💳 **Application Fee**: {admission['fees']['application']}\n"
        response += f"💰 **Annual Tuition**: {admission['fees']['tuition_per_year']}\n\n"
        response += "🏆 **Available Scholarships**:\n"
        for scholarship in admission['scholarships']:
            response += f"• {scholarship}\n"
        response += "\nNeed help with your application? I can guide you through each step!"

        return {
            'message': response,
            'is_urgent': False,
            'helpfulness': 0.95
        }

    def _handle_campus_query(self, user_message: str) -> Dict[str, Any]:
        """Handle campus and facilities queries"""
        facilities = self.university_data['campus_facilities']

        response = "🏫 **HMAWBI University Campus Facilities**:\n\n"
        response += f"📚 **Library**: {facilities['libraries']}\n"
        response += f"🔬 **Laboratories**: {facilities['laboratories']}\n"
        response += f"🏠 **Dormitories**: {facilities['dormitories']}\n"
        response += f"⚽ **Sports**: {facilities['sports']}\n"
        response += f"🍽️ **Dining**: {facilities['dining']}\n"
        response += f"🏥 **Medical**: {facilities['medical']}\n"
        response += f"🚌 **Transportation**: {facilities['transportation']}\n"
        response += f"📶 **Internet**: {facilities['wifi']}\n\n"
        response += "Our campus provides everything you need for a comfortable and productive university experience!"

        return {
            'message': response,
            'is_urgent': False,
            'helpfulness': 0.9
        }

    def _handle_career_query(self, user_message: str) -> Dict[str, Any]:
        """Handle career and job-related queries"""
        response = "💼 **Career Opportunities for HMAWBI Graduates**:\n\n"

        # Show salary ranges for all programs
        response += "💰 **Salary Ranges by Program**:\n"
        for program, info in self.university_data['hmawbi_programs'].items():
            response += f"• **{program}**: {info['salary_range']}\n"

        response += f"\n🎯 **Career Advice**:\n"
        response += f"• {random.choice(self.career_advice)}\n"
        response += f"• {random.choice(self.career_advice)}\n"

        response += "\n🏢 **Top Employers of HMAWBI Graduates**:\n"
        response += "• Myanmar Engineering Society\n• International construction companies\n• Tech startups\n• Government ministries\n• Multinational corporations\n\n"
        response += "Want to know about specific career paths? Ask me about any engineering program!"

        return {
            'message': response,
            'is_urgent': False,
            'helpfulness': 0.9
        }

    def _handle_study_query(self, user_message: str) -> Dict[str, Any]:
        """Handle study tips and academic help queries"""
        response = "📚 **Study Tips for Engineering Success**:\n\n"
        response += f"✅ {random.choice(self.study_tips)}\n"
        response += f"✅ {random.choice(self.study_tips)}\n"
        response += f"✅ {random.choice(self.study_tips)}\n\n"

        response += "🔬 **Academic Resources at HMAWBI**:\n"
        response += "• Tutoring center with peer mentors\n"
        response += "• Professor office hours\n"
        response += "• Study groups and academic clubs\n"
        response += "• Online learning platforms\n"
        response += "• 24/7 library access during exams\n\n"
        response += "Need specific help with a subject or study strategy? Just ask!"

        return {
            'message': response,
            'is_urgent': False,
            'helpfulness': 0.85
        }

    def _handle_financial_query(self, user_message: str) -> Dict[str, Any]:
        """Handle fees and financial queries"""
        fees = self.university_data['admission_info']['fees']
        scholarships = self.university_data['admission_info']['scholarships']

        response = "💰 **HMAWBI University Costs & Financial Aid**:\n\n"
        response += "📊 **Annual Costs**:\n"
        response += f"• Tuition: {fees['tuition_per_year']}\n"
        response += f"• Hostel: {fees['hostel']}\n"
        response += f"• Meal Plan: {fees['meal_plan']}\n"
        response += f"• Application Fee: {fees['application']}\n\n"

        response += "🏆 **Scholarship Opportunities**:\n"
        for scholarship in scholarships:
            response += f"• {scholarship}\n"

        response += "\n💡 **Financial Tips**:\n"
        response += "• Apply early for maximum scholarship consideration\n"
        response += "• Consider work-study programs on campus\n"
        response += "• Look into government education loans\n"
        response += "• Part-time tutoring opportunities available\n\n"
        response += "Need help planning your finances? I can provide more detailed guidance!"

        return {
            'message': response,
            'is_urgent': False,
            'helpfulness': 0.9
        }

    def _handle_student_life_query(self, user_message: str) -> Dict[str, Any]:
        """Handle student life and activities queries"""
        student_life = self.university_data['student_life']

        response = "🎓 **Student Life at HMAWBI University**:\n\n"
        response += "🏛️ **Student Clubs & Organizations**:\n"
        for club in student_life['clubs']:
            response += f"• {club}\n"

        response += "\n🎉 **Annual Events**:\n"
        for event in student_life['events']:
            response += f"• {event}\n"

        response += f"\n💼 **Practical Experience**:\n"
        response += f"• {student_life['internships']}\n"
        response += f"• {student_life['research']}\n\n"

        response += "🌟 **Why Students Love HMAWBI**:\n"
        response += "• Vibrant campus community\n"
        response += "• Strong alumni network\n"
        response += "• Industry connections\n"
        response += "• Beautiful campus in Hmawbi\n"
        response += "• Supportive faculty and staff\n\n"
        response += "Want to know more about any specific activity or club?"

        return {
            'message': response,
            'is_urgent': False,
            'helpfulness': 0.85
        }

    def _generate_comprehensive_response(self, user_message: str) -> str:
        """Generate a comprehensive response for general queries"""
        responses = [
            f"I'd love to help you with that! Here's what I can assist you with at HMAWBI University:\n\n"
            f"🎓 **Programs**: Information about our 6 engineering disciplines\n"
            f"📝 **Admissions**: Application process, requirements, and deadlines\n"
            f"🏫 **Campus Life**: Facilities, clubs, and student activities\n"
            f"💼 **Career Guidance**: Job prospects and salary information\n"
            f"💰 **Financial Aid**: Scholarships and cost information\n"
            f"📚 **Academic Support**: Study tips and resources\n\n"
            f"What specifically would you like to know more about?",

            f"Great question! As your HMAWBI University guide, I can help you with:\n\n"
            f"• Choosing the right engineering program\n"
            f"• Understanding admission requirements\n"
            f"• Exploring campus facilities\n"
            f"• Planning your career path\n"
            f"• Finding financial aid options\n"
            f"• Getting study tips and academic advice\n\n"
            f"Feel free to ask me anything specific about HMAWBI University!",

            f"I'm here to help you succeed at HMAWBI Technological University! You can ask me about:\n\n"
            f"📋 **Academic Programs** - Civil, Mechanical, Electrical, Computer, Electronic, Chemical Engineering\n"
            f"🎯 **Career Planning** - Job prospects, salaries, industry connections\n"
            f"🏠 **Campus Life** - Facilities, clubs, events, student support\n"
            f"💡 **Success Tips** - Study strategies, networking, skill development\n\n"
            f"What aspect of your university journey interests you most?"
        ]
    def analyze_helpfulness(self, message):
        """Analyze if the user found the response helpful"""
        try:
            blob = TextBlob(message)
            return blob.sentiment.polarity
        except Exception as e:
            logger.error(
                f"Sentiment analysis error for message '{message}': {e}")
            return 0.0

        return random.choice(responses)