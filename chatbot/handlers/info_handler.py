"""
Info Handler for HMAWBI University Chatbot
Handles university information, admission, and contact information
"""

from typing import Dict, List, Any, Optional
import random
import logging

logger = logging.getLogger(__name__)


class InfoHandler:
    """Handler for university information, admission, and contact queries"""
    
    def __init__(self):
        self.response_templates = {
            'admission': [
                "For admission information at HMAWBI University:",
                "Here's what you need to know about applying to HMAWBI University:",
                "Admission to HMAWBI University involves several steps:"
            ],
            'contact': [
                "Here's information about contacting departments at HMAWBI University:",
                "Need to reach a specific department? Here's how:",
                "Contact details for HMAWBI University departments:"
            ],
            'university_info': [
                "Here's general information about HMAWBI University:",
                "Let me share some key information about our university:",
                "About HMAWBI University:"
            ]
        }

    def handle_admission(self, context_data: Dict[str, Any]) -> str:
        """Handles responses related to university admissions."""
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

    def handle_contact(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to contact information for departments."""
        response = random.choice(self.response_templates['contact'])
        
        if 'contact' in context_data and context_data['contact']:
            message_lower = user_message.lower()
            specific_department = None

            # IMPROVED: Check if asking for a specific department
            for department_name, department_data in context_data['contact'].items():
                dept_lower = department_name.lower()
                
                # Original exact matching
                if dept_lower in message_lower:
                    specific_department = department_name
                    break
                    
                # Handle "Department of X" vs "X department" word order
                if dept_lower.startswith('department of'):
                    subject = dept_lower.replace('department of', '').strip()
                    subject_variations = [
                        f"{subject} department",
                        f"{subject}department", 
                        subject
                    ]
                    if any(variation in message_lower for variation in subject_variations):
                        specific_department = department_name
                        break
                        
                # Handle office names
                elif 'office' in dept_lower:
                    office_type = dept_lower.replace('office', '').strip()
                    if office_type in message_lower:
                        specific_department = department_name
                        break
                        
                # Handle partial matching (remove spaces and check)
                elif dept_lower.replace(" ", "") in message_lower.replace(" ", ""):
                    specific_department = department_name
                    break

            if specific_department:
                # Provide detailed info for a specific department
                dept_data = context_data['contact'][specific_department]
                response = f"Here's the contact information for **{specific_department}**:\n\n"
                response += f"📞 **Phone:** {dept_data.get('phone', 'Not specified')}\n"
                response += f"📧 **Email:** {dept_data.get('email', 'Not specified')}\n"
                response += f"👨‍🏫 **Teacher:** {dept_data.get('teacher', 'Not specified')}\n"
                if dept_data.get('location'):
                    response += f"📍 **Location:** {dept_data.get('location', 'Not specified')}\n"
                response += f"🕒 **Office Hours:** {dept_data.get('hours', 'Not specified')}\n"
                response += f"📝 **Description:** {dept_data.get('description', 'Not specified')}\n"
                response += "\nWould you like to know about other departments?"
            else:
                # Show ALL departments (not just 5)
                departments = list(context_data['contact'].keys())  # FIXED: Removed [:5]
                response += "\n\n" + "\n".join(['• ' + dept for dept in departments])
                response += "\n\nWould you like detailed contact information for any specific department?"
        else:
            # If no contact data is available
            response = "I couldn't retrieve any department contact information at the moment. Please check back later or contact the main university line."
        
        return response

    def handle_university_info(self, user_message: str, context_data: Dict[str, Any]) -> str:
        """Handles responses related to university information (rector, history, location, etc.)"""
        message_lower = user_message.lower()

        if 'university_info' in context_data and context_data['university_info']:
            university_info_data = context_data['university_info']

            specific_info_type = None
            response = ""

            # Prioritize EXTREMELY specific rector/pro-rector queries
            if any(phrase in message_lower for phrase in ['who is rector', 'rector name', 'current rector', 'rector is']):
                # Look for entries specifically mentioning "Rector" in title
                for info_type_key, info_item in university_info_data.items():
                    if 'rector' in info_item.get('title', '').lower() and 'pro-rector' not in info_item.get('title', '').lower():
                        response = f"🎓 **{info_item.get('title', 'University Rector')}**\n"
                        response += f"{info_item.get('content', 'Contact administration for current rector information.')}\n"
                        if info_item.get('description') and info_item.get('description') != 'Not specified':
                            response += f"\n💡 {info_item.get('description')}\n"
                        response += "\n📞 Need to contact the rector's office? Ask for contact information!"
                        return response

                # Fallback: Check general leadership entry for rector
                for info_type_key, info_item in university_info_data.items():
                    if 'leadership' in info_type_key.lower():
                        content = info_item.get('content', '')
                        if 'rector:' in content.lower() and 'pro-rector:' not in content.lower():
                            lines = content.split('\n')
                            rector_info = None
                            for line in lines:
                                if 'rector:' in line.lower() and 'pro-rector' not in line.lower():
                                    rector_info = line.strip()
                                    break
                            if rector_info:
                                response = f"🎓 **University Rector**\n{rector_info}\n"
                                response += "\n📞 Need to contact the rector's office? Ask for contact information!"
                                return response

                # If still no rector info found, use general response
                response = "I couldn't find specific information for the rector. You might find details in the general 'University Leadership' information. Would you like me to show that?"
                return response

            elif any(phrase in message_lower for phrase in ['who is pro-rector', 'pro-rector name', 'current pro-rector', 'pro rector name']):
                # Look for entries specifically mentioning "Pro-Rector" in title
                for info_type_key, info_item in university_info_data.items():
                    if 'pro-rector' in info_item.get('title', '').lower():
                        response = f"🎓 **{info_item.get('title', 'University Pro-Rector')}**\n"
                        response += f"{info_item.get('content', 'Contact administration for current pro-rector information.')}\n"
                        if info_item.get('description') and info_item.get('description') != 'Not specified':
                            response += f"\n💡 {info_item.get('description')}\n"
                        response += "\n📞 Need to contact the pro-rector's office? Ask for contact information!"
                        return response

                # Fallback: Check general leadership entry for pro-rector
                for info_type_key, info_item in university_info_data.items():
                    if 'leadership' in info_type_key.lower():
                        content = info_item.get('content', '')
                        if 'pro-rector:' in content.lower():
                            lines = content.split('\n')
                            pro_rector_info = None
                            for line in lines:
                                if 'pro-rector:' in line.lower():
                                    pro_rector_info = line.strip()
                                    break
                            if pro_rector_info:
                                response = f"🎓 **University Pro-Rector**\n{pro_rector_info}\n"
                                response += "\n📞 Need to contact the pro-rector's office? Ask for contact information!"
                                return response

                # If still no pro-rector info found, use general response
                response = "I couldn't find specific information for the pro-rector. You might find details in the general 'University Leadership' information. Would you like me to show that?"
                return response

            # Check for general "Leadership" queries (that are not specifically rector/pro-rector)
            elif any(word in message_lower for word in ['leadership', 'administration', 'officials', 'management team']):
                for info_type_key in university_info_data.keys():
                    if 'leadership' in info_type_key.lower():
                        specific_info_type = info_type_key
                        break

            # Check for location keywords  
            elif any(word in message_lower for word in ['location', 'address', 'transportation', 'bus', 'directions', 'how to get', 'where is']):
                for info_type_key in university_info_data.keys():
                    if any(word in info_type_key.lower() for word in ['location', 'transportation']):
                        specific_info_type = info_type_key
                        break

            # Check for history keywords
            elif any(word in message_lower for word in ['history', 'background', 'founded', 'established']):
                for info_type_key in university_info_data.keys():
                    if 'history' in info_type_key.lower():
                        specific_info_type = info_type_key
                        break

            # General fallback matching for other university info types
            else:
                for info_type_key, info_content in university_info_data.items():
                    if info_type_key.lower() in message_lower:
                        specific_info_type = info_type_key
                        break

            if specific_info_type:
                # Provide ONLY the specific info requested
                info_item = university_info_data[specific_info_type]
                response = f"Here is the information about **{specific_info_type}** at HMAWBI University:\n\n"
                response += f"📍 **{info_item.get('title', specific_info_type)}**\n"
                response += f"{info_item.get('content', 'No content available.')}\n"
                if info_item.get('description') and info_item.get('description') != 'Not specified':
                    response += f"\n💡 {info_item.get('description')}\n"

                # Add helpful follow-up suggestion
                if 'location' in specific_info_type.lower():
                    response += "\n🚌 Need directions or transportation details? Just ask!"
                elif 'leadership' in specific_info_type.lower():
                    response += "\n📞 Need to contact university administration? Ask for contact information!"

            else:
                # Show overview if user asks generally about "university information"
                if any(phrase in message_lower for phrase in ['university information', 'about university', 'tell me about university', 'general information']):
                    response = random.choice(self.response_templates['university_info']) + "\n\n"
                    for info_type_key, info_item in university_info_data.items():
                        response += f"📚 **{info_item.get('title', info_type_key)}**:\n"
                        content_snippet = info_item.get('content', 'No details available.')
                        if len(content_snippet) > 100:
                            content_snippet = content_snippet[:97] + "..."
                        response += f"   {content_snippet}\n\n"
                    response += "💡 You can ask for specific details like 'Who is the rector?', 'university location', or 'university history'."
                else:
                    # If no match found, suggest what's available
                    available_types = list(university_info_data.keys())
                    response = f"I can help you with information about HMAWBI University. Here's what I can tell you about:\n\n"
                    for info_type in available_types:
                        response += f"• {info_type}\n"
                    response += f"\n💡 Try asking: 'Who is the rector?', 'Who is the pro-rector?', or 'Tell me about university location'"
        else:
            # If no university info data is available
            response = random.choice(self.response_templates['university_info']) + "\n\nSorry, I couldn't retrieve university information at the moment. Please check back later."

        return response