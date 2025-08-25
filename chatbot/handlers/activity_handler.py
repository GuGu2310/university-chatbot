"""
Activity Handler for HMAWBI University Chatbot
Handles clubs, news, events, and scholarships
"""

from typing import Dict, List, Any, Optional
import random
import logging
import traceback # Import traceback for more detailed error logging

logger = logging.getLogger(__name__)


class ActivityHandler:
    """Handler for clubs, news, events, and scholarships queries"""
    
    def __init__(self):
        self.response_templates = {
            'scholarships': [
                "HMAWBI University offers various scholarship opportunities:",
                "Scholarship programs available at our university:",
                "Financial aid and scholarship options:"
            ],
            'clubs': [
                "HMAWBI University has many active student clubs and organizations:",
                "Our student clubs offer great opportunities for involvement:",
                "Join one of our vibrant student organizations:"
            ],
            'events': [
                "Here are upcoming events at HMAWBI University:",
                "Our university hosts various events throughout the year:",
                "Check out these exciting events coming up:"
            ],
            'news': [
                "Here's what's happening at HMAWBI University:",
                "Latest news and updates from our university:",
                "Stay informed with our university news:"
            ]
        }

    def handle_scholarships(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to scholarships, including specific details."""
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
                # Safely access scholarship name and ensure it's a string
                scholarship_name = scholarship.get('name')
                if isinstance(scholarship_name, str) and scholarship_name.lower() in message_lower:
                    specific_scholarship = scholarship
                    break

            if specific_scholarship:
                # Provide detailed info for a specific scholarship
                response = f"Here's detailed information about **{specific_scholarship.get('name', 'Scholarship')}**:\n\n"
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

    def handle_clubs(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to clubs, including specific membership requirements."""
        message_lower = user_message.lower()

        if 'clubs' in context_data and context_data['clubs']:
            clubs_data = context_data['clubs']

            # FIRST: Check for GENERAL club listing queries
            general_club_patterns = [
                'which club do we have', 'what club do we have', 'which clubs do we have', 
                'what clubs do we have', 'which club are there', 'what club are there',
                'which clubs are there', 'what clubs are there', 'list of club', 
                'list of clubs', 'all club', 'all clubs', 'available club', 
                'available clubs', 'what clubs', 'which clubs', 'show me clubs',
                'tell me about clubs', 'clubs available', 'club list'
            ]
            
            # Check exact matches for general queries
            is_general_query = any(pattern in message_lower for pattern in general_club_patterns)
            
            # Also check for general membership questions
            asking_for_general_membership = (
                any(phrase in message_lower for phrase in [
                    'membership requirements', 'membership requirement', 'how to join clubs',
                    'club membership', 'join clubs'
                ]) and not any(club.get('name', '').lower() in message_lower for club in clubs_data)
            )

            # If it's a general query, return the list immediately
            if is_general_query:
                response = "🏫 **Available Clubs at HMAWBI University:**\n\n"
                for club in clubs_data:
                    response += f"🎯 **{club.get('name', 'Club')}**\n"
                    response += f"   📝 Type: {club.get('club_type', 'Student Club')}\n"
                    response += f"   👨‍🏫 Advisor: {club.get('advisor', 'TBA')}\n\n"
                response += "💡 Ask me about a specific club for detailed information including meeting schedules and membership requirements!"
                return response

            if asking_for_general_membership:
                response = "🏫 **Club Membership Information at HMAWBI University:**\n\n"
                for club in clubs_data:
                    response += f"🎯 **{club.get('name', 'Club')}** ({club.get('club_type', 'Student Club')})\n"
                    membership_req = club.get('membership_requirements', 'Open to all students')
                    response += f"   📋 Requirements: {membership_req}\n"
                    if club.get('membership_fee'):
                        response += f"   💰 Fee: {club.get('membership_fee')}\n"
                    response += f"   📧 Contact: {club.get('contact_email', 'Contact student services')}\n\n"
                response += "💡 Ask me about a specific club for detailed information!"
                return response

            # SECOND: Only if NOT a general query, look for specific clubs
            specific_club = None
            
            # Check if asking for specific club membership requirements
            asking_for_membership = any(phrase in message_lower for phrase in [
                'membership requirements', 'membership requirement', 'how to join', 
                'join', 'membership', 'requirements', 'subscribe', 'subscription'
            ])
            
            # Look for specific club names - but only if it's not a general query
            for club in clubs_data:
                club_name_lower = club.get('name', '').lower()
                if club_name_lower:
                    # Check if the EXACT club name appears in the message
                    if club_name_lower in message_lower:
                        # Additional check to make sure it's really about this club
                        # Avoid false positives like "which" matching "guitar"
                        club_words = club_name_lower.split()
                        message_words = message_lower.split()
                        
                        # Check if all words of the club name appear in the message
                        if all(word in message_words for word in club_words):
                            specific_club = club
                            break

            # Handle specific club response
            if specific_club:
                response = f"Here's information about **{specific_club.get('name', 'Club')}**:\n\n"
                response += f"📝 Description: {specific_club.get('description', 'Student organization')}\n"
                response += f"🏷️ Type: {specific_club.get('club_type', 'Student Club')}\n"
                
                if asking_for_membership:
                    response += f"\n📋 **Membership Requirements for {specific_club.get('name', 'the Club')}:**\n"
                    membership_req = specific_club.get('membership_requirements', 'Open to all students')
                    response += f"   {membership_req}\n\n"
                    
                    if specific_club.get('membership_fee'):
                        response += f"💰 Membership Fee: {specific_club.get('membership_fee')}\n"
                    if specific_club.get('application_process'):
                        response += f"📄 Application Process: {specific_club.get('application_process')}\n"
                        
                    response += f"📅 Meeting Schedule: {specific_club.get('meeting_schedule', 'TBA')}\n"
                    response += f"📧 Contact: {specific_club.get('contact_email', 'Contact student services')}\n"
                    response += "\n💡 Contact the club directly or student services for more information about joining!"
                else:
                    response += f"👨‍🏫 Advisor: {specific_club.get('advisor', 'TBA')}\n"
                    response += f"📅 Meeting Schedule: {specific_club.get('meeting_schedule', 'TBA')}\n"
                    response += f"📋 Membership Requirements: {specific_club.get('membership_requirements', 'Open to all students')}\n"
                    response += f"📧 Contact: {specific_club.get('contact_email', 'Contact student services')}\n"
                    response += f"📅 Established: {specific_club.get('established_date', 'N/A')}\n"
                    
                    if specific_club.get('membership_fee'):
                        response += f"💰 Membership Fee: {specific_club.get('membership_fee')}\n"
                    
                    response += "\n💡 Contact the club directly or student services for more information about joining!"
                
                return response

            # DEFAULT: If no specific club found and not a general query, show list
            response = random.choice(self.response_templates['clubs']) + "\n\n"
            for club in clubs_data[:8]:
                response += f"• {club.get('name', 'Club')} ({club.get('club_type', 'Student Club')})\n"
            response += "\n💡 Ask me about a specific club for detailed information!"
            response += "\n💡 You can ask: 'What are the membership requirements for [Club Name]?'"
            
            return response
        else:
            return random.choice(self.response_templates['clubs']) + "\n\nSorry, I couldn't retrieve club information at the moment. Please check back later."

    def handle_events(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to events, showing upcoming and past events."""
        # Start with a generic response in case of any immediate failure
        response = random.choice(self.response_templates['events']) 
        
        try:
            message_lower = user_message.lower()

            # --- GETTING DATA ---
            # Use .get() with a default empty list to prevent errors if keys are missing
            upcoming_events = context_data.get('events', [])
            past_events = context_data.get('past_events', [])

            # --- DEBUGGING OUTPUT ---
            # Use logger.debug if your logging is configured to show debug messages.
            # Otherwise, use print() for immediate output during testing.
            logger.debug(f"--- Debugging Event Handling ---")
            logger.debug(f"Query: '{user_message}'")
            logger.debug(f"Upcoming events received ({len(upcoming_events)} items): {upcoming_events}")
            logger.debug(f"Past events received ({len(past_events)} items): {past_events}")
            logger.debug(f"--------------------------------")
            # --- END DEBUGGING OUTPUT ---

            # --- Data Validation: Filter for valid event dictionaries with titles ---
            # This is crucial to prevent errors if data is malformed or missing key fields
            upcoming_events = [e for e in upcoming_events if isinstance(e, dict) and e.get('title')]
            past_events = [e for e in past_events if isinstance(e, dict) and e.get('title')]
            # --- End Data Validation ---

            # Combine upcoming and past events for flexible querying
            all_events = upcoming_events + past_events

            specific_event = None
            # Only attempt to find a specific event if there are events to search through
            if all_events:
                for event in all_events:
                    # Safely get event title and check if it's a string before comparing
                    event_title = event.get('title')
                    if isinstance(event_title, str) and event_title.lower() in message_lower:
                        specific_event = event
                        break

            # --- EVENT RESPONSE GENERATION ---
            if specific_event:
                # Build response for a specific event, using .get() for safety
                response = f"Here's information about **{specific_event.get('title', 'Event')}**:\n\n"
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
            
            elif "past events" in message_lower or "previous events" in message_lower:
                # Handle specific requests for past events
                if past_events:
                    response = "Here are some of our previous events:\n\n"
                    # List up to 3 past events, safely accessing their details
                    for i, event in enumerate(past_events[:3], 1):
                        event_title = event.get('title', 'Event')
                        event_type = event.get('event_type', 'Event')
                        start_date = event.get('start_date', 'TBA')
                        response += f"{i}. **{event_title}** ({event_type})\n"
                        response += f"   📅 {start_date}\n\n"
                    response += "Would you like to know about any specific past event?"
                else:
                    response = "I don't have information on past events at the moment. Please check back later."
            
            else: # General event query - show a mix of upcoming and recent past events
                if upcoming_events or past_events:
                    response += "\n\n"
                    
                    # Show upcoming events first, limited to 3
                    if upcoming_events:
                        response += "**📅 Upcoming Events:**\n"
                        for event in upcoming_events[:3]:
                            event_title = event.get('title', 'Event')
                            event_type = event.get('event_type', 'Event')
                            start_date = event.get('start_date', 'TBA')
                            location = event.get('location', 'TBA')
                            response += f"• **{event_title}** ({event_type})\n"
                            response += f"  📅 {start_date} at {location}\n\n"
                    
                    # Show recent past events, limited to 3
                    if past_events:
                        response += "**📅 Recent Past Events:**\n"
                        for event in past_events[:3]:
                            event_title = event.get('title', 'Event')
                            event_type = event.get('event_type', 'Event')
                            start_date = event.get('start_date', 'TBA')
                            location = event.get('location', 'TBA')
                            response += f"• **{event_title}** ({event_type})\n"
                            response += f"  📅 {start_date} at {location}\n\n"
                    
                    response += "💡 Ask me about a specific event for detailed information including registration details!"
                else: # If no event data is available at all
                    response += "\n\nSorry, I couldn't retrieve event information at the moment. Please check back later."

            return response

        except Exception as e:
            # Catch any unforeseen exceptions during event handling
            # Log the error with traceback for detailed debugging
            logger.error(f"Unhandled error in handle_events for query '{user_message}': {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Also log the data received to help identify the problematic data structure
            logger.error(f"Data received for upcoming_events: {context_data.get('events', [])}")
            logger.error(f"Data received for past_events: {context_data.get('past_events', [])}")
            
            # Return the generic error message to the user
            return "I'm sorry, I'm having trouble processing your request right now. Please try again or contact our student services office for immediate assistance."

    def handle_news(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to university news."""
        message_lower = user_message.lower()
        
        if 'news' in context_data and context_data['news']:
            news_items = context_data['news']
            
            # Check if user is asking for a specific news article
            specific_news = self._find_specific_news(message_lower, news_items)
            
            if specific_news:
                # Return the full story for the specific news
                return self._format_full_news_story(specific_news)
            else:
                # Show news list with titles (existing functionality)
                response = random.choice(self.response_templates['news'])
                response += "\n\n**📰 Latest University News:**\n\n"
                
                for i, news_item in enumerate(news_items, 1):
                    title = news_item.get('title', f'News Item {i}')
                    date = news_item.get('date', 'Date not specified')
                    
                    # Show brief summary
                    content = news_item.get('content', 'No content available.')
                    if len(content) > 150:
                        content = content[:147] + "..."
                    
                    response += f"**{i}. {title}**\n"
                    response += f"📅 {date}\n"
                    response += f"📄 {content}\n\n"
                
                response += "💡 **Ask me about a specific news title for the full story!**\n"
                response += "Example: 'Tell me about [news title]' or 'Full story of [news title]'"
                
                return response
        else:
            return "I couldn't retrieve the latest university news at the moment. Please check back later or visit our official website."

    def _find_specific_news(self, message_lower: str, news_items: list) -> dict:
        """Find a specific news article based on user query"""
        
        # Keywords that indicate user wants a specific news story
        story_keywords = ['tell me about', 'full story', 'more about', 'details about', 'story of']
        
        # Check if user is asking for a specific story
        asking_for_story = any(keyword in message_lower for keyword in story_keywords)
        
        if not asking_for_story:
            return None
        
        # Try to match news titles
        for news_item in news_items:
            title = news_item.get('title', '').lower()
            
            # Remove common words for better matching
            title_words = title.replace('university', '').replace('hmawbi', '').strip()
            
            # Split title into individual words for partial matching
            title_keywords = [word.strip() for word in title_words.split() if len(word.strip()) > 2]
            
            # Check if any significant words from title appear in user message
            if title_keywords and any(keyword in message_lower for keyword in title_keywords):
                return news_item
            
            # Also check for exact phrase matching
            if title_words and title_words in message_lower:
                return news_item
        
        return None

    def _format_full_news_story(self, news_item: dict) -> str:
        """Format the full news story"""
        title = news_item.get('title', 'University News')
        date = news_item.get('date', 'Date not specified')
        content = news_item.get('content', 'No content available.')
        author = news_item.get('author', '')
        category = news_item.get('category', '')
        
        response = f"📰 **{title}**\n\n"
        response += f"📅 **Date:** {date}\n"
        
        if author:
            response += f"✍️ **Author:** {author}\n"
        if category:
            response += f"🏷️ **Category:** {category}\n"
        
        response += f"\n📄 **Full Story:**\n{content}\n\n"
        response += "📰 Want to see other news? Ask 'What are the latest news?' or 'Show me university news'"
        
        return response