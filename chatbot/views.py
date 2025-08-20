from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Conversation, Message, UniversityProgram, Scholarship, UniversityEvent
from .ai_processor import UniversityGuidanceChatbot
import json
import logging
import traceback
from django.utils import timezone 
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

def index(request):
    """Landing page for University Guidance Assistant"""
    return render(request, 'index.html')

def chat_view(request):
    """Main university guidance chat interface"""
    # Create or get conversation session
    session_id = request.session.get('conversation_id')
    conversation: Optional[Conversation] = None

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
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
        else:
            user_message = request.POST.get('message', '').strip()

        logger.info(f"Received message: '{user_message}'")

        if not user_message:
            logger.warning("Empty message received")
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Get or create conversation based on session_id
        session_id = request.session.get('conversation_id')
        conversation: Optional[Conversation] = None

        if not session_id:
            conversation = Conversation.objects.create()
            request.session['conversation_id'] = str(conversation.session_id)
            logger.info(f"Created new conversation: {conversation.session_id}")
        else:
            try:
                conversation = Conversation.objects.get(session_id=session_id)
                logger.info(f"Using existing conversation: {conversation.session_id}")
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create()
                request.session['conversation_id'] = str(conversation.session_id)
                logger.info(f"Created new conversation after DoesNotExist: {conversation.session_id}")

        # Save user message
        user_msg: Message = Message.objects.create(
            conversation=conversation,
            message_type='user',
            content=user_message
        )
        logger.info(f"Saved user message: {user_msg.pk}")

        # Get conversation history for context (last 10 messages)
        recent_messages = Message.objects.filter(
            conversation=conversation
        ).order_by('-timestamp')[:10]

        conversation_history: List[Dict[str, str]] = []
        for msg in reversed(recent_messages):
            message_for_history = {
                'role': 'user' if msg.message_type == 'user' else 'assistant',
                'content': msg.content
            }
            conversation_history.append(message_for_history)

        logger.info(f"Prepared conversation history with {len(conversation_history)} messages")

        try:
            # Initialize chatbot and generate response
            chatbot = UniversityGuidanceChatbot()
            logger.info("Initialized chatbot successfully")

            response = chatbot.generate_response(user_message, conversation_history)
            logger.info(f"Generated response with intent: {response.get('intent', 'unknown')}")

            # Save bot response
            bot_msg: Message = Message.objects.create(
                conversation=conversation,
                message_type='bot',
                content=response['message'],
                helpfulness_score=response.get('helpfulness')
            )
            logger.info(f"Saved bot message: {bot_msg.pk}")

            # Get relevant resources based on conversation topic
            relevant_resources: List[Dict[str, Any]] = []
            if response.get('is_urgent'):
                try:
                    relevant_resources = list(Scholarship.objects.filter(
                        is_active=True
                    ).values('name', 'description', 'benefit_amount', 'application_deadline'))
                    logger.info(f"Added {len(relevant_resources)} urgent resources")
                except Exception as resource_error:
                    logger.error(f"Error getting relevant resources: {resource_error}")

            return JsonResponse({
                'bot_response': response['message'],
                'is_urgent': response.get('is_urgent', False),
                'helpfulness': response.get('helpfulness'),
                'intent': response.get('intent', 'unknown'),
                'relevant_resources': relevant_resources,
                'timestamp': bot_msg.timestamp.isoformat(),
                'message_id': bot_msg.pk
            })

        except Exception as chatbot_error:
            logger.error(f"Error in chatbot processing: {chatbot_error}")
            logger.error(f"Chatbot error traceback: {traceback.format_exc()}")

            # Save error response
            error_response = "I'm sorry, I'm having trouble processing your request right now. Please try again or contact our student services office for immediate assistance."
            bot_msg: Message = Message.objects.create(
                conversation=conversation,
                message_type='bot',
                content=error_response,
                helpfulness_score=0.3
            )

            return JsonResponse({
                'bot_response': error_response,
                'is_urgent': False,
                'helpfulness': 0.3,
                'intent': 'error',
                'relevant_resources': [],
                'timestamp': bot_msg.timestamp.isoformat(),
                'message_id': bot_msg.pk,
                'error_debug': str(chatbot_error) if logger.level == logging.DEBUG else None
            })

    except json.JSONDecodeError as json_error:
        logger.error(f"JSON Decode Error in process_message: {json_error}")
        logger.error(f"Request Body: {request.body.decode('utf-8', errors='replace')}")
        return JsonResponse({'error': 'Invalid JSON format in request.'}, status=400)

    except Exception as general_error:
        logger.error(f"Unhandled error in process_message: {general_error}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return JsonResponse({
            'error': 'Internal server error processing message.',
            'debug_info': str(general_error) if logger.level == logging.DEBUG else None
        }, status=500)

def program_explorer(request):
    """University program exploration interface"""
    if request.method == 'POST':
        try:
            program_level = request.POST.get('program_level')
            interest_area = request.POST.get('interest_area', '')

            # Filter programs based on criteria
            programs = UniversityProgram.objects.filter(is_active=True)
            if program_level:
                programs = programs.filter(level=program_level)
            if interest_area:
                programs = programs.filter(name__icontains=interest_area)

            programs_data: List[Dict[str, Any]] = []
            for program in programs[:10]:
                # Safe handling of level display - avoid get_level_display entirely
                level_display = str(program.level) if hasattr(program, 'level') else 'Unknown'

                programs_data.append({
                    'name': program.name,
                    'level': level_display,
                    'description': program.description,
                    'duration': program.duration,
                    'career_paths': program.career_paths,
                    'entry_requirements': program.entry_requirements
                })

            return JsonResponse({
                'status': 'success', 
                'programs': programs_data,
                'message': f'Found {len(programs_data)} programs matching your criteria!'
            })
        except Exception as e:
            logger.error(f"Error in program search: {e}")
            logger.error(f"Program search error traceback: {traceback.format_exc()}")
            return JsonResponse({'error': 'Error searching programs.'}, status=500)

    # GET request - show the explorer interface
    try:
        programs = UniversityProgram.objects.filter(is_active=True)[:10]
        scholarships = Scholarship.objects.filter(is_active=True)[:5]
    except Exception as e:
        logger.error(f"Error loading program explorer data: {e}")
        programs = []
        scholarships = []

    return render(request, 'chatbot/program_explorer.html', {
        'recent_programs': programs,
        'scholarships': scholarships
    })

def resources(request):
    """University resources and opportunities page"""
    try:
        scholarships = Scholarship.objects.filter(is_active=True)
        events = UniversityEvent.objects.filter(
            is_public=True,
            start_date__gte=timezone.now()
        ).order_by('start_date')[:10]
    except Exception as e:
        logger.error(f"Error loading resources data: {e}")
        scholarships = []
        events = []

    return render(request, 'chatbot/resources.html', {
        'scholarships': scholarships,
        'events': events
    })

def clear_chat(request):
    """Clear current chat session"""
    try:
        session_id = request.session.get('conversation_id')
        if session_id:
            try:
                # Mark the conversation as inactive if it exists
                conversation = Conversation.objects.get(session_id=session_id)
                conversation.is_active = False
                conversation.ended_at = timezone.now()
                conversation.save()
                logger.info(f"Marked conversation {session_id} as inactive")
            except (Conversation.DoesNotExist, ValueError) as e:
                logger.warning(f"Could not find conversation to clear: {e}")
            except Exception as e:
                logger.error(f"Error updating conversation: {e}")

            # Remove the conversation_id from the session to start fresh
            try:
                if 'conversation_id' in request.session:
                    del request.session['conversation_id']
                    request.session.modified = True
                    logger.info("Cleared conversation_id from session")
            except Exception as e:
                logger.error(f"Error clearing session: {e}")

        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Chat cleared successfully'
            })

        # For regular HTTP requests, redirect to chat view
        try:
            return redirect('chat_view')  # Try the named URL first
        except Exception:
            return redirect('/chat/')  # Fallback to absolute URL

    except Exception as e:
        logger.error(f"Error in clear_chat: {e}")
        logger.error(f"Clear chat error traceback: {traceback.format_exc()}")

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': 'Error clearing chat session'
            }, status=500)

        # Return a safe fallback redirect
        return redirect('/chat/')

def get_question_categories(request):
    """Get available question categories for the chatbot"""
    categories: Dict[str, List[str]] = {
        "Programs": [
            "What engineering programs do you offer?",
            "Can you tell me more about the curriculum for Civil Engineering?",
            "Are there any specializations available within IT programs?",
            "What is the duration of each program?",
            "Which program has the highest employment rate?"
        ],
        "Admissions": [
            "What are the admission requirements?",
            "How do I apply for the university?",
            "When is the application deadline?",
            "What documents do I need for admission?",
            "Are there entrance exams?"
        ],
        "Campus Information": [
            "What facilities are available on campus?",
            "Is there accommodation for students?",
            "What are the sports facilities like?",
            "Tell me about the library facilities",
            "What clubs and activities are available?"
        ],
        "Financial Information": [
            "What are the tuition fees?",
            "Are there any scholarships available?",
            "How can I apply for financial aid?",
            "What are the living costs?",
            "Are there payment plan options?"
        ],
        "Student Life": [
            "What is student life like at HMAWBI?",
            "Are there clubs and activities for students?",
            "What kind of support does the university provide?",
            "Tell me about campus events",
            "How is the food on campus?"
        ],
        "Career Prospects": [
            "What is the employment rate for graduates?",
            "Does the university help with internships?",
            "What kind of industries do your graduates work in?",
            "What are the salary expectations?",
            "Are there job placement services?"
        ],
        "News & Updates": [
            "What are the latest university news?",
            "Tell me about recent achievements",
            "Are there any upcoming events?",
            "What's happening on campus?",
            "Show me university announcements"
        ]
    }

    return JsonResponse({
        'status': 'success',
        'categories': categories
    })

def test_chatbot(request):
    """Test endpoint for debugging chatbot functionality"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)

    try:
        test_message = request.GET.get('message', 'Hello, tell me about programs')
        chatbot = UniversityGuidanceChatbot()
        response = chatbot.generate_response(test_message)

        return JsonResponse({
            'status': 'success',
            'test_message': test_message,
            'response': response,
            'debug_info': {
                'intent': response.get('intent'),
                'helpfulness': response.get('helpfulness'),
                'is_urgent': response.get('is_urgent')
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'traceback': traceback.format_exc()
        })