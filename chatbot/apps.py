from django.apps import AppConfig

class ChatbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatbot'
    verbose_name = 'University Chatbot'
    
    def ready(self):
        """Initialize app when Django starts"""
        import chatbot.signals