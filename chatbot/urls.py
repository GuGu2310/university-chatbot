from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chat'),
    path('process-message/', views.process_message, name='process_message'),
    path('chat/clear/', views.clear_chat, name='clear_chat'),
    path('program-explorer/', views.program_explorer, name='program_explorer'),
    path('resources/', views.resources, name='resources'),
    path('api/question-categories/', views.get_question_categories, name='question_categories'),
]