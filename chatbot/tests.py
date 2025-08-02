from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Conversation, Message, UniversityProgram, CareerPath, AdmissionResource, StudentCampaign
from .ai_processor import UniversityGuidanceChatbot
import json

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_index_view(self):
        """Test index page loads"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'University Guide')

    def test_chat_view(self):
        """Test chat page loads"""
        response = self.client.get(reverse('chat'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'chat-messages')

    def test_process_message_post(self):
        """Test message processing"""
        data = {'message': 'Hello, I need help with university admissions'}
        response = self.client.post(
            reverse('process_message'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('bot_response', response_data)

    def test_program_explorer_view(self):
        """Test program explorer page"""
        response = self.client.get(reverse('program_explorer'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Program Explorer')

    def test_resources_view(self):
        """Test resources page"""
        response = self.client.get(reverse('resources'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'University Resources')

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_conversation_creation(self):
        """Test conversation model"""
        conversation = Conversation.objects.create(
            user=self.user,
            topic_category='admissions'
        )
        self.assertTrue(conversation.session_id)
        self.assertEqual(conversation.user, self.user)
        self.assertEqual(conversation.topic_category, 'admissions')

    def test_university_program_creation(self):
        """Test university program model"""
        program = UniversityProgram.objects.create(
            name='Computer Science',
            university='Test University',
            level='undergraduate',
            description='Test program',
            requirements='High school diploma',
            duration='4 years'
        )
        self.assertEqual(program.name, 'Computer Science')
        self.assertEqual(program.level, 'undergraduate')

    def test_career_path_creation(self):
        """Test career path model"""
        career = CareerPath.objects.create(
            title='Software Engineer',
            description='Develop software applications',
            required_education='Bachelor\'s degree',
            skills_needed='Programming, problem-solving',
            salary_range='$70,000 - $120,000'
        )
        self.assertEqual(career.title, 'Software Engineer')

class ChatbotTests(TestCase):
    def setUp(self):
        self.chatbot = UniversityGuidanceChatbot()

    def test_chatbot_initialization(self):
        """Test chatbot initializes properly"""
        self.assertIsNotNone(self.chatbot)

    def test_generate_response(self):
        """Test response generation"""
        message = "What programs do you offer?"
        conversation_history = []
        response = self.chatbot.generate_response(message, conversation_history)
        self.assertIn('message', response)
        self.assertIsInstance(response['message'], str)