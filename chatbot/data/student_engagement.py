
"""
Student Engagement Content for University Chatbot
Includes jokes, encouragement, fun facts, and news with proper content policies
"""

from datetime import datetime
from typing import List, Dict, Any

# Fun content that follows university policies
FUNNY_JOKES = [
    {
        "setup": "Why did the engineering student bring a ladder to class?",
        "punchline": "Because they heard the course was on the next level!",
        "category": "academic"
    },
    {
        "setup": "What's an engineer's favorite type of music?",
        "punchline": "Heavy metal... and concrete!",
        "category": "engineering"
    },
    {
        "setup": "Why don't programmers like nature?",
        "punchline": "It has too many bugs!",
        "category": "computer_science"
    }
]

PERSONAL_ENCOURAGEMENT = [
    {
        "message": "Every expert was once a beginner. Keep pushing forward!",
        "tone": "encouraging",
        "context": "academic_struggle"
    },
    {
        "message": "Your hard work today is building your future success.",
        "tone": "motivational", 
        "context": "general"
    },
    {
        "message": "Remember: every problem is an opportunity to learn something new.",
        "tone": "supportive",
        "context": "problem_solving"
    }
]

FUN_FACTS = [
    "HMAWBI University was the first technological university in Yangon Region",
    "Our alumni have worked on major infrastructure projects across Myanmar",
    "The university library contains over 50,000 engineering books and journals",
    "Students from all 14 states and regions of Myanmar study here"
]

# University news with proper content policies
UNIVERSITY_NEWS = [
    {
        "id": 1,
        "title": "New Computer Lab Opens",
        "content": "State-of-the-art computer laboratory with 50 new workstations now available for students",
        "category": "facilities",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": ["technology", "facilities", "students"]
    },
    {
        "id": 2,
        "title": "Engineering Week 2024 Announced",
        "content": "Annual Engineering Week will feature competitions, exhibitions, and industry talks from March 15-22",
        "category": "events",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": ["events", "engineering", "competitions"]
    },
    {
        "id": 3,
        "title": "Student Research Awards",
        "content": "Three students received recognition for outstanding research projects in renewable energy",
        "category": "academic",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": ["research", "awards", "renewable_energy"]
    }
]

# Functions to manage engagement content
def add_joke(setup: str, punchline: str, category: str = "general") -> bool:
    """Add a new joke following content policies"""
    joke = {
        "setup": setup,
        "punchline": punchline, 
        "category": category
    }
    FUNNY_JOKES.append(joke)
    return True

def add_encouragement(message: str, tone: str = "encouraging", context: str = "general") -> bool:
    """Add encouragement message"""
    encouragement = {
        "message": message,
        "tone": tone,
        "context": context
    }
    PERSONAL_ENCOURAGEMENT.append(encouragement)
    return True

def add_fun_fact(fact: str) -> bool:
    """Add university fun fact"""
    if fact not in FUN_FACTS:
        FUN_FACTS.append(fact)
        return True
    return False

def add_university_news(title: str, content: str, category: str = "general", tags: List[str] = None) -> bool:
    """Add university news following content policies"""
    # Check for inappropriate content
    inappropriate_keywords = [
        "prettiest", "ugliest", "worst teacher", "best looking", "hottest",
        "ranking students", "ranking staff", "personal appearance"
    ]
    
    content_lower = (title + " " + content).lower()
    if any(keyword in content_lower for keyword in inappropriate_keywords):
        return False  # Reject inappropriate content
    
    news_item = {
        "id": len(UNIVERSITY_NEWS) + 1,
        "title": title,
        "content": content,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": tags or []
    }
    UNIVERSITY_NEWS.append(news_item)
    return True

def search_news(keyword: str) -> List[Dict[str, Any]]:
    """Search university news by keyword"""
    keyword = keyword.lower()
    results = []
    for news in UNIVERSITY_NEWS:
        if (keyword in news["title"].lower() or 
            keyword in news["content"].lower() or
            keyword in [tag.lower() for tag in news["tags"]]):
            results.append(news)
    return results

def get_news_by_category(category: str) -> List[Dict[str, Any]]:
    """Get news by category"""
    return [news for news in UNIVERSITY_NEWS if news["category"] == category]
