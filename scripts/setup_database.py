#!/usr/bin/env python
"""
<<<<<<< HEAD
Database Setup Script for Placement Management System
This script sets up the database with initial data and configurations.
Run this after creating and applying migrations.
=======
Database setup script for Placement Management System
Run this script to create the database tables and initial data
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
"""

import os
import sys
import django
<<<<<<< HEAD
from datetime import date, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
=======

# Add the project directory to Python path
sys.path.append('/path/to/your/project')
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_management.settings')
django.setup()

<<<<<<< HEAD
from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, TutorProfile, ProviderProfile
from placements.models import PlacementRequest, Message
from django.utils import timezone

User = get_user_model()

def create_superuser():
    """Create a superuser for admin access"""
    try:
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@placement.com',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                user_type='tutor',
                is_verified=True
            )
            print(f"✅ Superuser created: {admin_user.username}")
        else:
            print("ℹ️  Superuser already exists")
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

def create_sample_tutors():
    """Create sample tutor accounts"""
    tutors_data = [
        {
            'username': 'tutor1',
            'email': 'tutor1@university.edu',
            'password': 'tutor123',
            'first_name': 'Dr. Sarah',
            'last_name': 'Johnson',
            'employee_id': 'T001',
            'department': 'Computer Science',
            'designation': 'Senior Lecturer',
            'office_location': 'Building A, Room 101'
        },
        {
            'username': 'tutor2',
            'email': 'tutor2@university.edu',
            'password': 'tutor123',
            'first_name': 'Prof. Michael',
            'last_name': 'Chen',
            'employee_id': 'T002',
            'department': 'Business Administration',
            'designation': 'Associate Professor',
            'office_location': 'Building B, Room 205'
        }
    ]
    
    for tutor_data in tutors_data:
        try:
            if not User.objects.filter(username=tutor_data['username']).exists():
                user = User.objects.create_user(
                    username=tutor_data['username'],
                    email=tutor_data['email'],
                    password=tutor_data['password'],
                    first_name=tutor_data['first_name'],
                    last_name=tutor_data['last_name'],
                    user_type='tutor',
                    is_verified=True
                )
                
                TutorProfile.objects.create(
                    user=user,
                    employee_id=tutor_data['employee_id'],
                    department=tutor_data['department'],
                    designation=tutor_data['designation'],
                    office_location=tutor_data['office_location']
                )
                print(f"✅ Tutor created: {user.get_full_name()}")
            else:
                print(f"ℹ️  Tutor already exists: {tutor_data['username']}")
        except Exception as e:
            print(f"❌ Error creating tutor {tutor_data['username']}: {e}")

def create_sample_providers():
    """Create sample provider accounts"""
    providers_data = [
        {
            'username': 'techcorp',
            'email': 'hr@techcorp.com',
            'password': 'provider123',
            'first_name': 'John',
            'last_name': 'Smith',
            'company_name': 'TechCorp Solutions',
            'company_address': '123 Innovation Drive, Tech City, TC 12345',
            'contact_person': 'John Smith',
            'website': 'https://techcorp.com',
            'company_size': '100-500',
            'industry': 'Technology'
        },
        {
            'username': 'globalbank',
            'email': 'internships@globalbank.com',
            'password': 'provider123',
            'first_name': 'Maria',
            'last_name': 'Garcia',
            'company_name': 'Global Bank International',
            'company_address': '456 Finance Street, Banking District, BD 67890',
            'contact_person': 'Maria Garcia',
            'website': 'https://globalbank.com',
            'company_size': '1000+',
            'industry': 'Banking & Finance'
        }
    ]
    
    for provider_data in providers_data:
        try:
            if not User.objects.filter(username=provider_data['username']).exists():
                user = User.objects.create_user(
                    username=provider_data['username'],
                    email=provider_data['email'],
                    password=provider_data['password'],
                    first_name=provider_data['first_name'],
                    last_name=provider_data['last_name'],
                    user_type='provider',
                    is_verified=True
                )
                
                ProviderProfile.objects.create(
                    user=user,
                    company_name=provider_data['company_name'],
                    company_address=provider_data['company_address'],
                    contact_person=provider_data['contact_person'],
                    website=provider_data['website'],
                    company_size=provider_data['company_size'],
                    industry=provider_data['industry']
                )
                print(f"✅ Provider created: {provider_data['company_name']}")
            else:
                print(f"ℹ️  Provider already exists: {provider_data['username']}")
        except Exception as e:
            print(f"❌ Error creating provider {provider_data['username']}: {e}")

def create_sample_students():
    """Create sample student accounts"""
    students_data = [
        {
            'username': 'student1',
            'email': 'student1@university.edu',
            'password': 'student123',
            'first_name': 'Alex',
            'last_name': 'Thompson',
            'student_id': 'S2024001',
            'course': 'Computer Science',
            'year': 3,
            'cgpa': 3.8
        },
        {
            'username': 'student2',
            'email': 'student2@university.edu',
            'password': 'student123',
            'first_name': 'Emma',
            'last_name': 'Wilson',
            'student_id': 'S2024002',
            'course': 'Business Administration',
            'year': 2,
            'cgpa': 3.6
        }
    ]
    
    for student_data in students_data:
        try:
            if not User.objects.filter(username=student_data['username']).exists():
                user = User.objects.create_user(
                    username=student_data['username'],
                    email=student_data['email'],
                    password=student_data['password'],
                    first_name=student_data['first_name'],
                    last_name=student_data['last_name'],
                    user_type='student',
                    is_verified=True
                )
                
                StudentProfile.objects.create(
                    user=user,
                    student_id=student_data['student_id'],
                    course=student_data['course'],
                    year=student_data['year'],
                    cgpa=student_data['cgpa']
                )
                print(f"✅ Student created: {user.get_full_name()}")
            else:
                print(f"ℹ️  Student already exists: {student_data['username']}")
        except Exception as e:
            print(f"❌ Error creating student {student_data['username']}: {e}")

def create_sample_placements():
    """Create sample placement requests"""
    try:
        # Get sample users
        student1 = StudentProfile.objects.get(student_id='S2024001')
        student2 = StudentProfile.objects.get(student_id='S2024002')
        provider1 = ProviderProfile.objects.get(company_name='TechCorp Solutions')
        provider2 = ProviderProfile.objects.get(company_name='Global Bank International')
        
        # Create sample placement requests
        placements_data = [
            {
                'student': student1,
                'provider': provider1,
                'company_name': 'TechCorp Solutions',
                'job_title': 'Software Development Intern',
                'job_description': 'Work on web development projects using modern technologies.',
                'start_date': date.today() + timedelta(days=30),
                'end_date': date.today() + timedelta(days=120),
                'location': 'Tech City, TC',
                'status': 'pending'
            },
            {
                'student': student2,
                'provider': provider2,
                'company_name': 'Global Bank International',
                'job_title': 'Business Analyst Intern',
                'job_description': 'Assist in analyzing business processes and data.',
                'start_date': date.today() + timedelta(days=45),
                'end_date': date.today() + timedelta(days=135),
                'location': 'Banking District, BD',
                'status': 'approved_by_provider'
            }
        ]
        
        for placement_data in placements_data:
            if not PlacementRequest.objects.filter(
                student=placement_data['student'],
                company_name=placement_data['company_name']
            ).exists():
                PlacementRequest.objects.create(**placement_data)
                print(f"✅ Placement request created for {placement_data['student'].user.get_full_name()}")
            else:
                print(f"ℹ️  Placement request already exists for {placement_data['student'].user.get_full_name()}")
                
    except Exception as e:
        print(f"❌ Error creating sample placements: {e}")

def main():
    """Main function to set up the database"""
    print("🚀 Setting up Placement Management System Database...")
    print("=" * 50)
    
    # Create superuser
    print("\n1. Creating superuser...")
    create_superuser()
    
    # Create sample tutors
    print("\n2. Creating sample tutors...")
    create_sample_tutors()
    
    # Create sample providers
    print("\n3. Creating sample providers...")
    create_sample_providers()
    
    # Create sample students
    print("\n4. Creating sample students...")
    create_sample_students()
    
    # Create sample placements
    print("\n5. Creating sample placement requests...")
    create_sample_placements()
    
    print("\n" + "=" * 50)
    print("✅ Database setup completed!")
    print("\n📋 Default Login Credentials:")
    print("Admin: admin / admin123")
    print("Tutor: tutor1 / tutor123")
    print("Provider: techcorp / provider123")
    print("Student: student1 / student123")
    print("\n🌐 Access the admin panel at: http://localhost:8000/admin/")

if __name__ == '__main__':
    main()
=======
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
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
