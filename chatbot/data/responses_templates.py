
"""
Chatbot Response Templates
Centralized response management for consistent messaging
"""

CONVERSATION_STARTERS = [
    "🎓 Hi! I'm here to help you explore your engineering future at HMAWBI Technological University!",
    "👋 Hello! Ready to discover amazing opportunities at HMAWBI? Let's get started!",
    "🌟 Welcome! I can guide you through admissions, programs, and student life at HMAWBI.",
    "🚀 Greetings! Let's discuss your path to becoming an engineer at HMAWBI University!",
    "💡 Hi there! I'm excited to help you plan your engineering career at HMAWBI!"
]

CASUAL_RESPONSES = {
    "greetings": [
        "Hello! 🎉 Great to meet you! What would you like to know about HMAWBI University?",
        "Hi there! 🌟 I'm excited to help you explore engineering opportunities at HMAWBI!",
        "Welcome! 👋 I'm your personal guide to everything HMAWBI Technological University!",
        "Hey! 🚀 Ready to discover your engineering potential at HMAWBI?"
    ],
    
    "how_are_you": [
        "I'm doing fantastic! 😊 I love helping students like you discover amazing opportunities at HMAWBI!",
        "I'm wonderful! 🌈 Every day I get to help students plan their engineering careers - it's awesome!",
        "I'm great, thank you! 💪 Ready to chat about your future at HMAWBI University?",
        "Excellent! 🎯 I'm energized and ready to help you explore HMAWBI's programs!"
    ],
    
    "thank_you": [
        "You're very welcome! 🌟 I'm here whenever you need guidance about HMAWBI!",
        "Happy to help! 😊 Feel free to ask me anything else about university life or programs!",
        "My pleasure! 🎉 That's what I'm here for - helping you succeed at HMAWBI!",
        "Anytime! 💫 I love supporting future engineers like you!"
    ],
    
    "goodbye": [
        "Goodbye! 👋 Best of luck with your engineering journey at HMAWBI!",
        "See you later! 🌟 Remember, I'm always here when you need guidance!",
        "Take care! 🚀 Wishing you success in your HMAWBI adventure!",
        "Farewell! 💪 Go conquer the engineering world!"
    ]
}

STUDY_TIPS = [
    "📚 Form study groups with classmates - engineering is better learned together!",
    "💻 Practice coding daily if you're in Computer/IT Engineering - consistency is key!",
    "🔬 Visit the lab frequently to get hands-on experience with equipment and tools!",
    "🤝 Join the Engineering Society to network with seniors and industry professionals!",
    "🎯 Attend guest lectures by industry experts - they provide invaluable insights!",
    "⏰ Start working on projects early - don't wait until the deadline approaches!",
    "👥 Use professor office hours to build relationships and get personalized help!",
    "📖 Read beyond textbooks - explore engineering journals and online resources!",
    "🏗️ Work on personal projects to build your portfolio and practical skills!",
    "🗣️ Practice presentation skills - communication is crucial in engineering!"
]

CAREER_ADVICE = [
    "💼 Internships are crucial - they often lead to job offers after graduation!",
    "📂 Build a portfolio of projects to showcase your technical skills to employers!",
    "🗣️ Develop both technical and soft skills - communication is key in engineering!",
    "🌱 Consider specializing in emerging fields like renewable energy, AI, or IoT!",
    "🌐 Network with HMAWBI alumni - they're in top companies worldwide!",
    "📰 Stay updated with industry trends through professional journals and conferences!",
    "🏆 Pursue professional certifications alongside your degree for competitive advantage!",
    "🎯 Attend career fairs and industry events to meet potential employers!",
    "📈 Learn about entrepreneurship - many engineers start their own companies!",
    "🔄 Be adaptable - engineering fields evolve rapidly with new technologies!"
]

MOTIVATIONAL_QUOTES = [
    "🚀 'Engineering is not only about building bridges, but also about building the future!'",
    "💡 'Every expert was once a beginner. Every pro was once an amateur!'",
    "🌟 'Your degree is a preparation for life, not just for a job!'",
    "🎯 'Success in engineering comes from passion, persistence, and continuous learning!'",
    "🌈 'At HMAWBI, we don't just teach engineering - we inspire innovation!'"
]

COMPREHENSIVE_RESPONSES = [
    """🎓 **Welcome to HMAWBI University Guide!** I'm here to help you with:

📚 **Academic Programs**: Information about our 6 engineering disciplines
📝 **Admissions**: Application process, requirements, and important deadlines  
🏫 **Campus Life**: Facilities, student clubs, and exciting activities
💼 **Career Guidance**: Job prospects, salary information, and industry connections
💰 **Financial Support**: Scholarships, fees, and financial aid options
📖 **Study Success**: Tips, resources, and academic support services

What specific area interests you most? I'm excited to help! ✨""",

    """🌟 **Great to meet you!** As your HMAWBI University assistant, I can guide you through:

• 🎯 **Choosing the Perfect Program** - Find your ideal engineering path
• 📋 **Admission Requirements** - Everything you need to know to apply
• 🏛️ **Campus Experience** - Discover our amazing facilities and community
• 🚀 **Career Opportunities** - Explore exciting job prospects and salaries
• 💳 **Financial Planning** - Scholarships, fees, and budget planning
• 📚 **Academic Excellence** - Study strategies and success tips

Ready to explore your engineering future? Ask me anything! 💫""",

    """🚀 **Hello Future Engineer!** I'm thrilled to help you discover HMAWBI University:

🔬 **6 Engineering Programs** - Civil, Mechanical, Electrical, IT, Architecture, Mechatronics
🎯 **Career Success** - Industry connections, internships, and job placement
🏠 **Campus Community** - Modern facilities, clubs, events, and student support
💡 **Innovation Hub** - Research opportunities, labs, and cutting-edge technology
💰 **Affordable Excellence** - Competitive fees with generous scholarship programs

What aspect of your university journey excites you most? Let's dive in! 🌈"""
]

ERROR_RESPONSES = [
    "🤔 I didn't quite catch that. Could you rephrase your question about HMAWBI University?",
    "💭 Hmm, I'm not sure I understand. Try asking about admissions, programs, or campus life!",
    "🔄 Let me help you better! Could you ask about a specific topic like engineering programs or scholarships?",
    "❓ I want to give you the best answer! Could you be more specific about what you'd like to know?",
    "💡 Try asking about: programs, admissions, campus facilities, career prospects, or student life!"
]

URGENCY_INDICATORS = [
    "urgent", "emergency", "deadline", "immediate", "asap", "quickly", "hurry",
    "time-sensitive", "critical", "important deadline", "last minute"
]

RESPONSE_CATEGORIES = {
    "programs": ["program", "course", "degree", "study", "engineering", "major", "curriculum"],
    "admissions": ["admission", "apply", "application", "requirements", "deadline", "entrance"],
    "campus": ["campus", "facilities", "library", "hostel", "dorm", "accommodation", "sports"],
    "career": ["career", "job", "salary", "employment", "prospects", "work", "industry"],
    "financial": ["fee", "cost", "money", "scholarship", "financial", "tuition", "budget"],
    "student_life": ["student life", "clubs", "activities", "events", "culture", "social"],
    "academic": ["study", "tips", "help", "academic", "exam", "research", "project"]
}
