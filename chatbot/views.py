from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Conversation, Message, UniversityProgram, CareerPath, AdmissionResource, StudentCampaign
from .ai_processor import UniversityGuidanceChatbot
import json
import uuid 
import logging
from django.utils import timezone 

logger = logging.getLogger(__name__)

def index(request):
    """Landing page for University Guidance Assistant"""
    return render(request, 'index.html')

def chat_view(request):
    """Main university guidance chat interface"""
    # Create or get conversation session
    session_id = request.session.get('conversation_id')
    if not session_id:
        conversation = Conversation.objects.create()
        request.session['conversation_id'] = str(conversation.session_id)
    else:
        try:
            conversation = Conversation.objects.get(session_id=session_id)
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create()
            request.session['conversation_id'] = str(conversation.session_id)

    # Get conversation history
    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    return render(request, 'chatbot/chat.html', {
        'messages': messages,
        'conversation_id': conversation.session_id
    })

@require_http_methods(["POST"])
def process_message(request):
    """Process user message and return bot response"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Get or create conversation based on session_id
        session_id = request.session.get('conversation_id')
        if not session_id:
            conversation = Conversation.objects.create()
            request.session['conversation_id'] = str(conversation.session_id)
        else:
            try:
                conversation = Conversation.objects.get(session_id=session_id)
            except Conversation.DoesNotExist:
                # If a session_id exists but the conversation doesn't, create a new one
                conversation = Conversation.objects.create()
                request.session['conversation_id'] = str(conversation.session_id)

        # Save user message
        user_msg = Message.objects.create(
            conversation=conversation,
            message_type='user',
            content=user_message
        )

        # Generate bot response
        chatbot = UniversityGuidanceChatbot()

        # Get conversation history for context (last 10 messages)
        recent_messages = Message.objects.filter(
            conversation=conversation
        ).order_by('-timestamp')[:10]

        conversation_history = []
        for msg in reversed(recent_messages):
            messages_for_history = {
                'role': 'user' if msg.message_type == 'user' else 'assistant',
                'content': msg.content
            }
            conversation_history.append(messages_for_history)

        try:
            chatbot = UniversityGuidanceChatbot()
            response = chatbot.generate_response(user_message, conversation_history)

            # Save bot response
            bot_msg = Message.objects.create(
                conversation=conversation,
                message_type='bot',
                content=response['message'],
                helpfulness_score=response.get('helpfulness')
            )

            # Get relevant resources based on conversation topic
            relevant_resources = []
            if response.get('is_urgent'):
                relevant_resources = list(AdmissionResource.objects.filter(
                    is_priority=True
                ).values('title', 'description', 'url', 'deadline_date'))

            return JsonResponse({
                'bot_response': response['message'],
                'is_urgent': response.get('is_urgent', False),
                'helpfulness': response.get('helpfulness'),
                'relevant_resources': relevant_resources,
                'timestamp': bot_msg.timestamp.isoformat(),
                'message_id': bot_msg.id
            })

        except Exception as e:
            logger.error(f"Error in chat processing: {e}")
            return JsonResponse({
                'error': 'Internal server error processing message.'
            }, status=500)

    except json.JSONDecodeError:
        logger.error(f"JSON Decode Error in process_message. Request Body: {request.body.decode('utf-8')}")
        return JsonResponse({'error': 'Invalid JSON format in request.'}, status=400)
    except Exception as e:
        logger.error(f"Unhandled error in process_message: {e}", exc_info=True) # exc_info=True to log full traceback
        return JsonResponse({'error': 'Internal server error processing message.'}, status=500)

def program_explorer(request):
    """University program exploration interface"""
    if request.method == 'POST':
        try:
            program_level = request.POST.get('program_level')
            interest_area = request.POST.get('interest_area', '')

            # Filter programs based on criteria
            programs = UniversityProgram.objects.all()
            if program_level:
                programs = programs.filter(level=program_level)
            if interest_area:
                programs = programs.filter(name__icontains=interest_area)

            programs_data = list(programs.values(
                'name', 'university', 'level', 'description', 'duration', 'career_prospects'
            )[:10])

            return JsonResponse({
                'status': 'success', 
                'programs': programs_data,
                'message': f'Found {len(programs_data)} programs matching your criteria!'
            })
        except Exception as e:
            logger.error(f"Error in program search: {e}", exc_info=True)
            return JsonResponse({'error': 'Error searching programs.'}, status=500)

    # GET request - show the explorer interface
    programs = UniversityProgram.objects.all()[:10]  # Show some sample programs
    career_paths = CareerPath.objects.all()[:5]  # Show some career options

    return render(request, 'chatbot/program_explorer.html', {
        'recent_programs': programs,
        'career_paths': career_paths
    })

def resources(request):
    """University resources and opportunities page"""
    admission_resources = AdmissionResource.objects.filter(is_priority=True)
    scholarship_resources = AdmissionResource.objects.filter(resource_type='scholarship')
    student_campaigns = StudentCampaign.objects.filter(is_active=True)[:10]

    return render(request, 'chatbot/resources.html', {
        'admission_resources': admission_resources,
        'scholarship_resources': scholarship_resources,
        'student_campaigns': student_campaigns
    })

def clear_chat(request):
    """Clear current chat session"""
    session_id = request.session.get('conversation_id')
    if session_id:
        try:
            # Mark the conversation as inactive if it exists
            conversation = Conversation.objects.get(session_id=session_id)
            conversation.is_active = False
            conversation.ended_at = timezone.now()
            conversation.save()
        except (Conversation.DoesNotExist, ValueError):
            pass # No active conversation or invalid session_id

        # Remove the conversation_id from the session to start fresh
        if 'conversation_id' in request.session:
            del request.session['conversation_id']

    return redirect('chat')

# University guidance admin functionality