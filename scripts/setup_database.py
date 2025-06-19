#!/usr/bin/env python
"""
Database setup script for Placement Management System
Run this script to create the database tables and initial data
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/path/to/your/project')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_management.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, TutorProfile, ProviderProfile

def setup_database():
    """Set up the database with initial migrations and sample data"""
    
    print("🔄 Running migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Database migrations completed!")
    
    # Create superuser if it doesn't exist
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        print("👤 Creating superuser...")
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            user_type='tutor'
        )
        print("✅ Superuser created! Username: admin, Password: admin123")
    
    # Create sample data
    print("📝 Creating sample data...")
    
    # Sample Provider
    if not User.objects.filter(username='provider1').exists():
        provider_user = User.objects.create_user(
            username='provider1',
            email='provider@company.com',
            password='provider123',
            first_name='John',
            last_name='Smith',
            user_type='provider'
        )
        ProviderProfile.objects.create(
            user=provider_user,
            company_name='Tech Solutions Pvt Ltd',
            company_address='123 Business Park, Tech City',
            contact_person='John Smith',
            website='https://techsolutions.com'
        )
    
    # Sample Tutor
    if not User.objects.filter(username='tutor1').exists():
        tutor_user = User.objects.create_user(
            username='tutor1',
            email='tutor@college.edu',
            password='tutor123',
            first_name='Dr. Sarah',
            last_name='Johnson',
            user_type='tutor'
        )
        TutorProfile.objects.create(
            user=tutor_user,
            employee_id='EMP001',
            department='Computer Science',
            designation='Professor'
        )
    
    # Sample Student
    if not User.objects.filter(username='student1').exists():
        student_user = User.objects.create_user(
            username='student1',
            email='student@college.edu',
            password='student123',
            first_name='Alice',
            last_name='Brown',
            user_type='student'
        )
        StudentProfile.objects.create(
            user=student_user,
            student_id='STU001',
            course='Computer Science Engineering',
            year=3,
            cgpa=8.5
        )
    
    print("✅ Sample data created!")
    print("\n🎉 Database setup completed successfully!")
    print("\n📋 Sample Login Credentials:")
    print("Admin: admin / admin123")
    print("Provider: provider1 / provider123")
    print("Tutor: tutor1 / tutor123")
    print("Student: student1 / student123")
    print("\n🚀 You can now run: python manage.py runserver")

if __name__ == '__main__':
    setup_database()
