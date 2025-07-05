"""
Mock data for dynamic frontend demonstration
"""
from datetime import datetime, timedelta
import random

# Mock Users Data
MOCK_USERS = {
    'students': [
        {
            'id': 1,
            'username': 'student1',
            'password': 'student123',
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice@college.edu',
            'phone': '9876543210',
            'student_id': 'CS2021001',
            'course': 'Computer Science Engineering',
            'year': 3,
            'cgpa': 8.5,
            'profile_pic': '/static/images/student1.jpg'
        },
        {
            'id': 2,
            'username': 'student2',
            'password': 'student123',
            'first_name': 'Bob',
            'last_name': 'Smith',
            'email': 'bob@college.edu',
            'phone': '9876543211',
            'student_id': 'CS2021002',
            'course': 'Computer Science Engineering',
            'year': 3,
            'cgpa': 7.8,
            'profile_pic': '/static/images/student2.jpg'
        },
        {
            'id': 3,
            'username': 'student3',
            'password': 'student123',
            'first_name': 'Carol',
            'last_name': 'Davis',
            'email': 'carol@college.edu',
            'phone': '9876543212',
            'student_id': 'EC2021001',
            'course': 'Electronics Engineering',
            'year': 4,
            'cgpa': 9.1,
            'profile_pic': '/static/images/student3.jpg'
        }
    ],
    'tutors': [
        {
            'id': 1,
            'username': 'tutor1',
            'password': 'tutor123',
            'first_name': 'Dr. Sarah',
            'last_name': 'Wilson',
            'email': 'sarah@college.edu',
            'phone': '9876543220',
            'employee_id': 'EMP001',
            'department': 'Computer Science',
            'designation': 'Professor',
            'profile_pic': '/static/images/tutor1.jpg'
        },
        {
            'id': 2,
            'username': 'tutor2',
            'password': 'tutor123',
            'first_name': 'Dr. Michael',
            'last_name': 'Brown',
            'email': 'michael@college.edu',
            'phone': '9876543221',
            'employee_id': 'EMP002',
            'department': 'Electronics',
            'designation': 'Associate Professor',
            'profile_pic': '/static/images/tutor2.jpg'
        }
    ],
    'providers': [
        {
            'id': 1,
            'username': 'provider1',
            'password': 'provider123',
            'first_name': 'John',
            'last_name': 'Anderson',
            'email': 'john@techcorp.com',
            'phone': '9876543230',
            'company_name': 'TechCorp Solutions',
            'company_address': '123 Tech Park, Bangalore',
            'contact_person': 'John Anderson',
            'website': 'https://techcorp.com',
            'profile_pic': '/static/images/provider1.jpg'
        },
        {
            'id': 2,
            'username': 'provider2',
            'password': 'provider123',
            'first_name': 'Lisa',
            'last_name': 'Chen',
            'email': 'lisa@innovate.com',
            'phone': '9876543231',
            'company_name': 'Innovate Labs',
            'company_address': '456 Innovation Street, Mumbai',
            'contact_person': 'Lisa Chen',
            'website': 'https://innovatelabs.com',
            'profile_pic': '/static/images/provider2.jpg'
        },
        {
            'id': 3,
            'username': 'provider3',
            'password': 'provider123',
            'first_name': 'David',
            'last_name': 'Kumar',
            'email': 'david@startupinc.com',
            'phone': '9876543232',
            'company_name': 'StartupInc',
            'company_address': '789 Startup Hub, Hyderabad',
            'contact_person': 'David Kumar',
            'website': 'https://startupinc.com',
            'profile_pic': '/static/images/provider3.jpg'
        }
    ]
}

# Mock Placement Requests
MOCK_PLACEMENTS = [
    {
        'id': 1,
        'student_id': 1,
        'provider_id': 1,
        'company_name': 'TechCorp Solutions',
        'job_title': 'Software Developer Intern',
        'job_description': 'Work on web development projects using Django and React. Learn modern software development practices.',
        'start_date': datetime.now() + timedelta(days=30),
        'end_date': datetime.now() + timedelta(days=120),
        'location': 'Bangalore, Karnataka',
        'status': 'approved_by_tutor',
        'created_at': datetime.now() - timedelta(days=5),
        'documents': 'resume_alice.pdf'
    },
    {
        'id': 2,
        'student_id': 2,
        'provider_id': 2,
        'company_name': 'Innovate Labs',
        'job_title': 'Data Science Intern',
        'job_description': 'Work with machine learning models and data analysis. Gain experience in Python and AI.',
        'start_date': datetime.now() + timedelta(days=45),
        'end_date': datetime.now() + timedelta(days=135),
        'location': 'Mumbai, Maharashtra',
        'status': 'approved_by_provider',
        'created_at': datetime.now() - timedelta(days=3),
        'documents': 'resume_bob.pdf'
    },
    {
        'id': 3,
        'student_id': 3,
        'provider_id': 3,
        'company_name': 'StartupInc',
        'job_title': 'Frontend Developer',
        'job_description': 'Build responsive web applications using React and modern CSS frameworks.',
        'start_date': datetime.now() + timedelta(days=60),
        'end_date': datetime.now() + timedelta(days=150),
        'location': 'Hyderabad, Telangana',
        'status': 'pending',
        'created_at': datetime.now() - timedelta(days=1),
        'documents': 'resume_carol.pdf'
    },
    {
        'id': 4,
        'student_id': 1,
        'provider_id': 2,
        'company_name': 'Innovate Labs',
        'job_title': 'Backend Developer',
        'job_description': 'Develop REST APIs and work with databases. Learn about scalable backend systems.',
        'start_date': datetime.now() + timedelta(days=75),
        'end_date': datetime.now() + timedelta(days=165),
        'location': 'Mumbai, Maharashtra',
        'status': 'rejected',
        'created_at': datetime.now() - timedelta(days=7),
        'documents': 'resume_alice_v2.pdf'
    },
    {
        'id': 5,
        'student_id': 2,
        'provider_id': 1,
        'company_name': 'TechCorp Solutions',
        'job_title': 'Mobile App Developer',
        'job_description': 'Create mobile applications using React Native and Flutter.',
        'start_date': datetime.now() + timedelta(days=90),
        'end_date': datetime.now() + timedelta(days=180),
        'location': 'Bangalore, Karnataka',
        'status': 'completed',
        'created_at': datetime.now() - timedelta(days=120),
        'documents': 'resume_bob_v2.pdf'
    }
]

# Mock Messages
MOCK_MESSAGES = [
    {
        'id': 1,
        'sender_id': 1,
        'sender_type': 'student',
        'recipient_id': 1,
        'recipient_type': 'tutor',
        'subject': 'Question about placement approval',
        'content': 'Hello Dr. Wilson, I wanted to ask about the status of my placement request at TechCorp Solutions.',
        'created_at': datetime.now() - timedelta(hours=2),
        'is_read': False
    },
    {
        'id': 2,
        'sender_id': 1,
        'sender_type': 'tutor',
        'recipient_id': 1,
        'recipient_type': 'student',
        'subject': 'Re: Question about placement approval',
        'content': 'Hi Alice, your placement request has been approved. Congratulations!',
        'created_at': datetime.now() - timedelta(hours=1),
        'is_read': True
    }
]

# Mock Visit Schedules
MOCK_VISITS = [
    {
        'id': 1,
        'placement_id': 1,
        'tutor_id': 1,
        'visit_date': datetime.now() + timedelta(days=40),
        'purpose': 'Initial placement visit and student evaluation',
        'notes': 'Check student progress and company facilities',
        'completed': False
    },
    {
        'id': 2,
        'placement_id': 5,
        'tutor_id': 1,
        'visit_date': datetime.now() - timedelta(days=30),
        'purpose': 'Final evaluation visit',
        'notes': 'Student performed excellently. Company satisfied with work.',
        'completed': True
    }
]

# Helper functions to get mock data
def get_user_by_credentials(username, password, user_type=None):
    """Get user by username and password"""
    if user_type:
        users = MOCK_USERS.get(f"{user_type}s", [])
    else:
        users = []
        for user_list in MOCK_USERS.values():
            users.extend(user_list)
    
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def get_user_by_id(user_id, user_type):
    """Get user by ID and type"""
    users = MOCK_USERS.get(f"{user_type}s", [])
    for user in users:
        if user['id'] == user_id:
            return user
    return None

def get_placements_by_student(student_id):
    """Get placements for a specific student"""
    return [p for p in MOCK_PLACEMENTS if p['student_id'] == student_id]

def get_placements_by_provider(provider_id):
    """Get placements for a specific provider"""
    return [p for p in MOCK_PLACEMENTS if p['provider_id'] == provider_id]

def get_placements_by_status(status):
    """Get placements by status"""
    return [p for p in MOCK_PLACEMENTS if p['status'] == status]

def get_placement_by_id(placement_id):
    """Get placement by ID"""
    for placement in MOCK_PLACEMENTS:
        if placement['id'] == placement_id:
            return placement
    return None

def get_messages_for_user(user_id, user_type):
    """Get messages for a specific user"""
    return [m for m in MOCK_MESSAGES 
            if (m['recipient_id'] == user_id and m['recipient_type'] == user_type) or
               (m['sender_id'] == user_id and m['sender_type'] == user_type)]

def get_visits_by_tutor(tutor_id):
    """Get visits for a specific tutor"""
    return [v for v in MOCK_VISITS if v['tutor_id'] == tutor_id]

def get_placement_stats():
    """Get overall placement statistics"""
    total = len(MOCK_PLACEMENTS)
    pending = len([p for p in MOCK_PLACEMENTS if p['status'] == 'pending'])
    approved = len([p for p in MOCK_PLACEMENTS if p['status'] in ['approved_by_provider', 'approved_by_tutor']])
    completed = len([p for p in MOCK_PLACEMENTS if p['status'] == 'completed'])
    rejected = len([p for p in MOCK_PLACEMENTS if p['status'] == 'rejected'])
    
    return {
        'total': total,
        'pending': pending,
        'approved': approved,
        'completed': completed,
        'rejected': rejected
    }
