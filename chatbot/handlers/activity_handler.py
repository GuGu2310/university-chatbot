"""
Activity Handler for HMAWBI University Chatbot
Handles clubs, news, events, and scholarships
"""

from typing import Dict, List, Any, Optional
import random
import logging

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

    def handle_clubs(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to clubs, including specific membership requirements."""
        response = random.choice(self.response_templates['clubs'])
        message_lower = user_message.lower()

        if 'clubs' in context_data and context_data['clubs']:
            clubs_data = context_data['clubs']

            # Check if asking for specific club by name - improved matching
            specific_club = None
            
            # First, try exact name matching
            for club in clubs_data:
                club_name_lower = club['name'].lower()
                if club_name_lower in message_lower:
                    specific_club = club
                    break
            
            # If no exact match, try partial matching for common club name patterns
            if not specific_club:
                for club in clubs_data:
                    club_name_lower = club['name'].lower()
                    club_words = club_name_lower.split()
                    
                    # Check if any significant words from the club name are in the message
                    # This handles cases like "guitar club" matching "Guitar Club"
                    for word in club_words:
                        if len(word) > 3 and word in message_lower:  # Only check meaningful words
                            # Additional verification - check if it's really about this club
                            if any(club_keyword in message_lower for club_keyword in ['club', 'organization', 'group', 'society']):
                                specific_club = club
                                break
                    
                    if specific_club:
                        break
            
            # Additional check for membership requirements queries
            asking_for_membership = any(phrase in message_lower for phrase in [
                'membership requirements', 'membership requirement', 'how to join', 
                'join', 'membership', 'requirements', 'subscribe', 'subscription'
            ])

            if specific_club:
                # Provide detailed info for a specific club, including membership requirements
                response = f"Here's information about **{specific_club['name']}**:\n\n"
                response += f"📝 Description: {specific_club.get('description', 'Student organization')}\n"
                response += f"🏷️ Type: {specific_club.get('club_type', 'Student Club')}\n"
                
                # If specifically asking about membership, highlight that information
                if asking_for_membership:
                    response += f"\n📋 **Membership Requirements for {specific_club['name']}:**\n"
                    membership_req = specific_club.get('membership_requirements', 'Open to all students')
                    response += f"   {membership_req}\n\n"
                    
                    # Add additional membership details if available
                    if specific_club.get('membership_fee'):
                        response += f"💰 Membership Fee: {specific_club.get('membership_fee')}\n"
                    if specific_club.get('application_process'):
                        response += f"📄 Application Process: {specific_club.get('application_process')}\n"
                        
                    response += f"📧 Contact: {specific_club.get('contact_email', 'Contact student services')}\n"
                    response += f"📅 Meeting Schedule: {specific_club.get('meeting_schedule', 'TBA')}\n"
                    response += "\n💡 Contact the club directly or student services for more information about joining!"
                else:
                    # Provide general club information
                    response += f"👨‍🏫 Advisor: {specific_club.get('advisor', 'TBA')}\n"
                    response += f"📅 Meeting Schedule: {specific_club.get('meeting_schedule', 'TBA')}\n"
                    response += f"📋 Membership Requirements: {specific_club.get('membership_requirements', 'Open to all students')}\n"
                    response += f"📧 Contact: {specific_club.get('contact_email', 'Contact student services')}\n"
                    response += f"📅 Established: {specific_club.get('established_date', 'N/A')}\n"
                    
                    if specific_club.get('membership_fee'):
                        response += f"💰 Membership Fee: {specific_club.get('membership_fee')}\n"
                    
                    response += "\n💡 Contact the club directly or student services for more information about joining!"
                    
            elif asking_for_membership and not specific_club:
                # If asking about membership but no specific club was identified
                response = "I'd be happy to help you with club membership information! Here are our available clubs:\n\n"
                for club in clubs_data[:8]: # List clubs with membership info
                    response += f"• **{club.get('name', 'Club')}** ({club.get('club_type', 'Student Club')})\n"
                    membership_req = club.get('membership_requirements', 'Open to all students')
                    response += f"  📋 Requirements: {membership_req}\n\n"
                response += "💡 Ask me about a specific club (e.g., 'Guitar Club membership requirements') for detailed information!"
                
            else:
                # List general clubs if no specific query
                response += "\n\n"
                for club in clubs_data[:8]: # List first 8 clubs
                    response += f"• {club.get('name', 'Club')} ({club.get('club_type', 'Student Club')})\n"
                response += "\n💡 Ask me about a specific club for detailed information including meeting schedules and membership requirements!"
                response += "\n💡 You can ask: 'What are the membership requirements for [Club Name]?' or 'How do I join [Club Name]?'"
        else: # If no club data is available
            response += "\n\nSorry, I couldn't retrieve club information at the moment. Please check back later."

        return response

    def handle_events(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to events, showing upcoming and past events."""
        response = random.choice(self.response_templates['events'])
        message_lower = user_message.lower()

        upcoming_events = context_data.get('events', [])
        past_events = context_data.get('past_events', [])

        # Combine upcoming and past events for flexible querying
        all_events = upcoming_events + past_events

        specific_event = None
        for event in all_events:
            if event.get('title', '').lower() in message_lower:
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
        
        elif "past events" in message_lower or "previous events" in message_lower:
            # Specifically handle requests for past events
            if past_events:
                response = "Here are some of our previous events:\n\n"
                for i, event in enumerate(past_events[:3], 1): # Show up to 3 past events
                    response += f"{i}. **{event.get('title', 'Event')}** ({event.get('event_type', 'Event')})\n"
                    response += f"   📅 {event.get('start_date', 'TBA')}\n\n"
                response += "Would you like to know about any specific past event?"
            else:
                response = "I don't have information on past events at the moment. Please check back later."
        
        else: # General event query - show both upcoming and recent past events
            if upcoming_events or past_events:
                response += "\n\n"
                
                # Show upcoming events first
                if upcoming_events:
                    response += "**📅 Upcoming Events:**\n"
                    for event in upcoming_events[:3]: # List first 3 upcoming events
                        response += f"• **{event.get('title', 'Event')}** ({event.get('event_type', 'Event')})\n"
                        response += f"  📅 {event.get('start_date', 'TBA')} at {event.get('location', 'TBA')}\n\n"
                
                # Show recent past events
                if past_events:
                    response += "**📅 Recent Past Events:**\n"
                    for event in past_events[:3]: # Show last 3 past events
                        response += f"• **{event.get('title', 'Event')}** ({event.get('event_type', 'Event')})\n"
                        response += f"  📅 {event.get('start_date', 'TBA')} at {event.get('location', 'TBA')}\n\n"
                
                response += "💡 Ask me about a specific event for detailed information including registration details!"
            else: # If no event data is available
                response += "\n\nSorry, I couldn't retrieve event information at the moment. Please check back later."

        return response

    def handle_news(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to university news."""
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
            return "I'm having trouble accessing the news right now. Please try again later or contact our information desk."