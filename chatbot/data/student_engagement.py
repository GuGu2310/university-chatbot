"""
Student Engagement Content
Fun jokes, personal speech data, and entertainment content for students
"""

FUNNY_JOKES = [
    {
        "setup": "Why don't engineers ever get lost?",
        "punchline": "Because they always know their coordinates! 📐",
        "category": "engineering"
    },
    {
        "setup": "What did the civil engineer say when asked about his favorite music?",
        "punchline": "I love heavy metal... especially steel beams! 🏗️",
        "category": "civil"
    },
    {
        "setup": "Why did the electrical engineer break up with the mechanical engineer?",
        "punchline": "There was no spark, and their relationship had too much friction! ⚡🔧",
        "category": "engineering"
    },
    {
        "setup": "How many programmers does it take to change a light bulb?",
        "punchline": "None. That's a hardware problem! 💻",
        "category": "it"
    },
    {
        "setup": "Why did the architecture student always carry a ruler?",
        "punchline": "Because they wanted to measure up to their dreams! 📏",
        "category": "architecture"
    },
    {
        "setup": "What's an engineer's favorite type of music?",
        "punchline": "Rock and COIL! 🎵",
        "category": "electrical"
    },
    {
        "setup": "Why don't civil engineers ever tell construction jokes?",
        "punchline": "Because they're still working on the foundation! 🏢",
        "category": "civil"
    },
    {
        "setup": "What did the mechatronics engineer say at the robotics competition?",
        "punchline": "Let's get this party automated! 🤖",
        "category": "mechatronics"
    }
]

PERSONAL_ENCOURAGEMENT = [
    {
        "message": "Hey future engineer! 🌟 Remember, every expert was once a beginner. You're doing amazing!",
        "tone": "encouraging",
        "context": "general"
    },
    {
        "message": "Feeling stressed about exams? 📚 Take a deep breath! Even the greatest engineers had tough days. You've got this! 💪",
        "tone": "supportive",
        "context": "exam_stress"
    },
    {
        "message": "Did you know? Some of the world's greatest innovations came from students just like you! 🚀 Keep dreaming big!",
        "tone": "inspiring",
        "context": "motivation"
    },
    {
        "message": "Having a tough day with assignments? 📝 Remember: every line of code, every calculation brings you closer to your dreams! ✨",
        "tone": "motivational",
        "context": "academic_struggle"
    },
    {
        "message": "Coffee break time? ☕ Fun fact: Many famous engineers had their best ideas during breaks! So relax and let creativity flow! 💡",
        "tone": "casual",
        "context": "break_time"
    },
    {
        "message": "Stuck on a problem? 🤔 That's not failure, that's your brain preparing for a breakthrough! Keep pushing! 🔥",
        "tone": "encouraging",
        "context": "problem_solving"
    }
]

CASUAL_CHATS = [
    {
        "trigger": ["tired", "exhausted", "sleepy"],
        "responses": [
            "I hear you! 😴 Engineering studies can be exhausting. Maybe grab some tea and take a 10-minute break?",
            "Feeling drained? 🔋 Even robots need to recharge! How about a quick walk or some fresh air?",
            "Tired brain = time for a reset! 🧠⚡ Sometimes the best solutions come after a good rest!"
        ]
    },
    {
        "trigger": ["hungry", "food", "snack"],
        "responses": [
            "Hungry brain needs fuel! 🍎 Fun fact: glucose is your brain's favorite energy source!",
            "Food time! 🍜 Did you know engineers burn extra calories thinking? Treat yourself!",
            "Snack attack? 🥨 Pro tip: nuts and fruits are great brain food for studying!"
        ]
    },
    {
        "trigger": ["weekend", "friday", "party"],
        "responses": [
            "Weekend vibes! 🎉 Time to balance equations AND fun! You've earned it!",
            "Friday feeling? 🎊 Even engineers need to decompress! What's your weekend plan?",
            "Party time? 🥳 Remember: work hard, play hard is the engineer's motto!"
        ]
    },
    {
        "trigger": ["rain", "weather", "cold"],
        "responses": [
            "Rainy day perfect for coding! ☔💻 There's something cozy about indoor engineering work!",
            "Cold weather? ❄️ Perfect excuse for hot chocolate and warm study sessions!",
            "Weather update: 100% chance of learning something awesome today! 🌈"
        ]
    }
]

STUDENT_LIFE_QUOTES = [
    "🎓 'The best engineers are those who never stop being students!' - Keep that curiosity alive!",
    "🚀 'Your degree is your rocket fuel, but your passion is what gets you to the stars!'",
    "💡 'Every problem is just an opportunity wearing work clothes!' - Keep innovating!",
    "🌟 'Engineering isn't just about building things, it's about building dreams!'",
    "🔧 'Code, coffee, and creativity - the holy trinity of engineering students!'",
    "📚 'Study today, engineer tomorrow, change the world forever!'",
    "⚡ 'You're not just learning engineering, you're learning to shape the future!'"
]

CELEBRATION_MESSAGES = [
    {
        "occasion": "exam_pass",
        "messages": [
            "🎉 WOOHOO! You crushed that exam! Time for a victory dance! 💃🕺",
            "🏆 Exam conquered! You're officially amazing! Celebration time! 🎊",
            "⚡ POW! Another exam down! You're unstoppable! 🚀"
        ]
    },
    {
        "occasion": "project_complete",
        "messages": [
            "🎯 Project DONE! You're a coding/engineering wizard! ✨",
            "🏗️ Another masterpiece completed! Your future employers will be lucky! 💼",
            "🔥 Project finished! Time to add this victory to your portfolio! 📁"
        ]
    },
    {
        "occasion": "assignment_submit",
        "messages": [
            "📝 Assignment submitted! That's what we call engineering efficiency! ⚙️",
            "✅ BOOM! Assignment in! You're keeping that GPA looking good! 📈",
            "🎪 Another assignment bites the dust! You're on fire! 🔥"
        ]
    }
]

FUN_FACTS = [
    "🤓 Fun fact: The first computer programmer was a woman - Ada Lovelace in 1843!",
    "🌉 Did you know? The Golden Gate Bridge sways up to 27 feet in strong winds!",
    "💡 Cool fact: Edison didn't invent the light bulb - he just made it practical!",
    "🚀 Space fact: Engineers designed spacecraft computers less powerful than your phone!",
    "🏗️ Amazing: The Burj Khalifa can sway up to 6 feet at the top!",
    "💻 Tech fact: The first 1GB hard drive in 1980 weighed 550 pounds!",
    "⚡ Electric fact: Lightning strikes the Earth 100 times per second!",
    "🔧 Engineering fact: The word 'robot' comes from Czech word 'robota' meaning work!"
]

# Easy data management functions
def add_joke(setup, punchline, category="general"):
    """Add a new joke to the collection"""
    new_joke = {
        "setup": setup,
        "punchline": punchline,
        "category": category
    }
    FUNNY_JOKES.append(new_joke)
    return True

def add_encouragement(message, tone="encouraging", context="general"):
    """Add new encouragement message"""
    new_message = {
        "message": message,
        "tone": tone,
        "context": context
    }
    PERSONAL_ENCOURAGEMENT.append(new_message)
    return True

def add_fun_fact(fact):
    """Add a new fun fact"""
    if fact not in FUN_FACTS:
        FUN_FACTS.append(fact)
        return True
    return False

def get_joke_by_category(category="general"):
    """Get jokes by specific category"""
    return [joke for joke in FUNNY_JOKES if joke.get("category", "general") == category]

def get_random_encouragement(context="general"):
    """Get encouragement by context"""
    return [msg for msg in PERSONAL_ENCOURAGEMENT if msg.get("context", "general") == context]

# Example usage functions for easy data addition
def quick_add_engineering_joke():
    """Example: Add a new engineering joke"""
    return add_joke(
        "Why did the engineer cross the road?",
        "To get to the other site! 🏗️",
        "engineering"
    )

def quick_add_motivation():
    """Example: Add new motivational message"""
    return add_encouragement(
        "You're not just studying engineering - you're training to become a problem-solving superhero! 🦸‍♂️⚡",
        "inspiring",
        "motivation"
    )

UNIVERSITY_NEWS = [
    {
        "title": "Basketball Championship Victory! 🏆",
        "content": "The Mechanical Engineering team won the Inter-Faculty Basketball Championship 2024! Congratulations to our amazing athletes!",
        "category": "sports",
        "date": "2024-12-15",
        "tags": ["basketball", "championship", "mechanical", "sports"]
    },
    {
        "title": "HMAWBI University Queen 2024 👑",
        "content": "Miss Thant Zin from Civil Engineering has been crowned HMAWBI University Queen 2024! She impressed judges with her talent and advocacy for women in engineering.",
        "category": "campus_life",
        "date": "2024-11-20",
        "tags": ["beauty_pageant", "civil", "women_empowerment"]
    },
    {
        "title": "Robotics Team Wins National Competition 🤖",
        "content": "Our Mechatronics students won 1st place at the Myanmar National Robotics Competition with their innovative automation project!",
        "category": "academic",
        "date": "2024-10-25",
        "tags": ["robotics", "mechatronics", "competition", "innovation"]
    },
    {
        "title": "New Research Lab Opening 🔬",
        "content": "HMAWBI University is opening a state-of-the-art AI and Machine Learning Research Lab in collaboration with international partners!",
        "category": "facilities",
        "date": "2024-09-30",
        "tags": ["research", "ai", "lab", "technology"]
    },
    {
        "title": "Football Team Reaches Finals ⚽",
        "content": "The HMAWBI Eagles football team has reached the University League Finals! Match scheduled for next Saturday at the main stadium.",
        "category": "sports",
        "date": "2024-12-01",
        "tags": ["football", "finals", "eagles", "league"]
    }
]

CAMPUS_ACHIEVEMENTS = [
    {
        "achievement": "Top Engineering University in Myanmar 2024",
        "description": "HMAWBI ranked #1 in engineering education by Myanmar Education Rankings",
        "year": "2024"
    },
    {
        "achievement": "95% Graduate Employment Rate",
        "description": "Our graduates find jobs within 6 months of graduation",
        "year": "2024"
    },
    {
        "achievement": "International Partnership Expansion",
        "description": "New partnerships with universities in Singapore, Japan, and Germany",
        "year": "2024"
    }
]

# Easy data management functions for news
def add_university_news(title, content, category="general", tags=None):
    """Add new university news"""
    if tags is None:
        tags = []

    new_news = {
        "title": title,
        "content": content,
        "category": category,
        "date": "2024-12-20",  # You can make this dynamic
        "tags": tags
    }
    UNIVERSITY_NEWS.append(new_news)
    return True

def get_news_by_category(category):
    """Get news by specific category"""
    return [news for news in UNIVERSITY_NEWS if news.get("category") == category]

def search_news(keyword):
    """Search news by keyword in title, content, or tags"""
    keyword = keyword.lower()
    results = []
    for news in UNIVERSITY_NEWS:
        if (keyword in news["title"].lower() or 
            keyword in news["content"].lower() or 
            any(keyword in tag.lower() for tag in news["tags"])):
            results.append(news)
    return results

# Quick add examples
def add_sports_news():
    """Example: Add sports achievement"""
    return add_university_news(
        "Volleyball Team Victory! 🏐",
        "The IT Engineering volleyball team defeated Civil Engineering 3-1 in the championship finals!",
        "sports",
        ["volleyball", "it", "championship"]
    )

def add_academic_news():
    """Example: Add academic achievement"""
    return add_university_news(
        "Student Research Published 📚",
        "Final year Electrical Engineering student published research on renewable energy in international journal!",
        "academic",
        ["research", "electrical", "renewable_energy", "publication"]
    )

if __name__ == "__main__":
    # Demo usage
    print("Sample Joke:")
    print(f"Q: {FUNNY_JOKES[0]['setup']}")
    print(f"A: {FUNNY_JOKES[0]['punchline']}")

    print("\nSample Encouragement:")
    print(PERSONAL_ENCOURAGEMENT[0]['message'])

    print("\nSample University News:")
    print(f"Title: {UNIVERSITY_NEWS[0]['title']}")
    print(f"Content: {UNIVERSITY_NEWS[0]['content']}")

    print(f"\nTotal Content: {len(FUNNY_JOKES)} jokes, {len(PERSONAL_ENCOURAGEMENT)} encouragements, {len(UNIVERSITY_NEWS)} news items")