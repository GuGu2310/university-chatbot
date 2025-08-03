
"""
Data Manager for HMAWBI University Chatbot
Provides utilities for managing and updating university data
"""

import json
import os
from typing import Dict, List, Any
from .data.university_programs import UNIVERSITY_PROGRAMS, CAMPUS_INFO, ADMISSION_INFO, STUDENT_LIFE
from .data.responses_templates import CONVERSATION_STARTERS, CASUAL_RESPONSES, STUDY_TIPS, CAREER_ADVICE
from .data.student_engagement import FUNNY_JOKES, PERSONAL_ENCOURAGEMENT, FUN_FACTS, add_joke, add_encouragement, add_fun_fact

class DataManager:
    """Centralized data management for university information"""
    
    def __init__(self):
        self.data_sources = {
            'programs': UNIVERSITY_PROGRAMS,
            'campus': CAMPUS_INFO,
            'admission': ADMISSION_INFO,
            'student_life': STUDENT_LIFE,
            'responses': {
                'starters': CONVERSATION_STARTERS,
                'casual': CASUAL_RESPONSES,
                'study_tips': STUDY_TIPS,
                'career_advice': CAREER_ADVICE
            },
            'engagement': {
                'jokes': FUNNY_JOKES,
                'encouragement': PERSONAL_ENCOURAGEMENT,
                'fun_facts': FUN_FACTS
            }
        }
    
    def get_program_info(self, program_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific program"""
        return self.data_sources['programs'].get(program_name, {})
    
    def get_all_programs(self) -> Dict[str, Any]:
        """Get information about all programs"""
        return self.data_sources['programs']
    
    def add_program(self, program_name: str, program_data: Dict[str, Any]) -> bool:
        """Add a new program to the database"""
        try:
            self.data_sources['programs'][program_name] = program_data
            return True
        except Exception as e:
            print(f"Error adding program: {e}")
            return False
    
    def update_program(self, program_name: str, field: str, value: Any) -> bool:
        """Update a specific field of a program"""
        try:
            if program_name in self.data_sources['programs']:
                self.data_sources['programs'][program_name][field] = value
                return True
            return False
        except Exception as e:
            print(f"Error updating program: {e}")
            return False
    
    def get_campus_info(self) -> Dict[str, Any]:
        """Get campus information"""
        return self.data_sources['campus']
    
    def get_admission_info(self) -> Dict[str, Any]:
        """Get admission information"""
        return self.data_sources['admission']
    
    def add_scholarship(self, scholarship_data: Dict[str, str]) -> bool:
        """Add a new scholarship to admission info"""
        try:
            self.data_sources['admission']['scholarships'].append(scholarship_data)
            return True
        except Exception as e:
            print(f"Error adding scholarship: {e}")
            return False
    
    def update_fees(self, fee_type: str, amount: str) -> bool:
        """Update fee information"""
        try:
            if fee_type in self.data_sources['admission']['fees']:
                self.data_sources['admission']['fees'][fee_type] = amount
                return True
            return False
        except Exception as e:
            print(f"Error updating fees: {e}")
            return False
    
    def add_study_tip(self, tip: str) -> bool:
        """Add a new study tip"""
        try:
            if tip not in self.data_sources['responses']['study_tips']:
                self.data_sources['responses']['study_tips'].append(tip)
                return True
            return False
        except Exception as e:
            print(f"Error adding study tip: {e}")
            return False
    
    def add_career_advice(self, advice: str) -> bool:
        """Add new career advice"""
        try:
            if advice not in self.data_sources['responses']['career_advice']:
                self.data_sources['responses']['career_advice'].append(advice)
                return True
            return False
        except Exception as e:
            print(f"Error adding career advice: {e}")
            return False
    
    def export_data_to_json(self, filepath: str) -> bool:
        """Export all data to JSON file for backup"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.data_sources, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def import_data_from_json(self, filepath: str) -> bool:
        """Import data from JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    imported_data = json.load(f)
                self.data_sources.update(imported_data)
                return True
            return False
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def validate_program_data(self, program_data: Dict[str, Any]) -> List[str]:
        """Validate program data structure"""
        required_fields = [
            'duration', 'description', 'career_paths', 'entry_requirements',
            'subjects', 'job_prospects', 'salary_range'
        ]
        
        missing_fields = []
        for field in required_fields:
            if field not in program_data:
                missing_fields.append(field)
        
        return missing_fields
    
    def search_programs(self, query: str) -> List[str]:
        """Search programs by keyword"""
        query = query.lower()
        matching_programs = []
        
        for program_name, program_data in self.data_sources['programs'].items():
            # Search in program name
            if query in program_name.lower():
                matching_programs.append(program_name)
                continue
            
            # Search in description
            if query in program_data.get('description', '').lower():
                matching_programs.append(program_name)
                continue
            
            # Search in career paths
            career_paths = program_data.get('career_paths', [])
            if any(query in career.lower() for career in career_paths):
                matching_programs.append(program_name)
                continue
        
        return matching_programs
    
    def add_joke(self, setup: str, punchline: str, category: str = "general") -> bool:
        """Add a new joke to the engagement content"""
        try:
            return add_joke(setup, punchline, category)
        except Exception as e:
            print(f"Error adding joke: {e}")
            return False
    
    def add_encouragement_message(self, message: str, tone: str = "encouraging", context: str = "general") -> bool:
        """Add a new encouragement message"""
        try:
            return add_encouragement(message, tone, context)
        except Exception as e:
            print(f"Error adding encouragement: {e}")
            return False
    
    def add_fun_fact_item(self, fact: str) -> bool:
        """Add a new fun fact"""
        try:
            return add_fun_fact(fact)
        except Exception as e:
            print(f"Error adding fun fact: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the data"""
        return {
            'total_programs': len(self.data_sources['programs']),
            'total_scholarships': len(self.data_sources['admission']['scholarships']),
            'total_study_tips': len(self.data_sources['responses']['study_tips']),
            'total_career_advice': len(self.data_sources['responses']['career_advice']),
            'student_organizations': len(self.data_sources['student_life']['clubs_organizations']),
            'annual_events': len(self.data_sources['student_life']['annual_events']),
            'total_jokes': len(self.data_sources['engagement']['jokes']),
            'total_encouragements': len(self.data_sources['engagement']['encouragement']),
            'total_fun_facts': len(self.data_sources['engagement']['fun_facts'])
        }

# Example usage functions
def quick_add_program():
    """Example function to quickly add a new program"""
    manager = DataManager()
    
    new_program = {
        "duration": "6 years Bachelor + 2 years ME",
        "description": "New engineering program description",
        "career_paths": ["Engineer", "Specialist", "Manager"],
        "entry_requirements": "Mathematics, Physics with minimum 75% marks",
        "subjects": ["Subject 1", "Subject 2", "Subject 3"],
        "job_prospects": "Growing opportunities in the field",
        "salary_range": "600,000 - 2,500,000 MMK per month",
        "specializations": ["Specialization 1", "Specialization 2"],
        "industry_connections": ["Company 1", "Company 2"]
    }
    
    program_name = "New Engineering Program"
    success = manager.add_program(program_name, new_program)
    print(f"Program added: {success}")

def backup_data():
    """Backup all data to JSON file"""
    manager = DataManager()
    success = manager.export_data_to_json('university_data_backup.json')
    print(f"Data backup: {success}")

if __name__ == "__main__":
    # Example usage
    manager = DataManager()
    stats = manager.get_statistics()
    print("University Data Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
