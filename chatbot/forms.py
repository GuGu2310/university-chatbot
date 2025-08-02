
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

class UserProfileForm(forms.ModelForm):
    ACADEMIC_LEVEL_CHOICES = [
        ('high_school', 'High School'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('doctorate', 'Doctorate'),
    ]
    
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 13,
            'max': 120,
            'placeholder': 'Your age (optional)'
        }),
        label="Age"
    )
    
    academic_level = forms.ChoiceField(
        choices=ACADEMIC_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Academic Level"
    )
    
    interests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'What are your academic interests? (e.g., Computer Science, Medicine, Arts)'
        }),
        label="Academic Interests"
    )
    
    consent_given = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="I consent to using this university guidance service"
    )
    
    privacy_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label="I have read and accept the privacy policy"
    )
    
    class Meta:
        model = UserProfile
        fields = ['age', 'academic_level', 'interests', 'consent_given', 'privacy_accepted']

class UniversitySearchForm(forms.Form):
    PROGRAM_LEVEL_CHOICES = [
        ('', 'Any Level'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('doctorate', 'Doctorate'),
        ('certificate', 'Certificate')
    ]
    
    program_level = forms.ChoiceField(
        choices=PROGRAM_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="Program Level"
    )
    
    interest_area = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your area of interest (e.g., Engineering, Business)'
        }),
        label="Area of Interest"
    )
    
    university = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'University name (optional)'
        }),
        label="University"
    )

class FeedbackForm(forms.Form):
    RATING_CHOICES = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent')
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label="How would you rate your experience with the university guidance chatbot?"
    )
    
    feedback = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Please share your feedback about the university guidance chatbot...'
        }),
        label="Your Feedback"
    )
    
    improvement_suggestions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any suggestions for improvement? (Optional)'
        }),
        label="Suggestions for Improvement"
    )

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message'
        })
    )
