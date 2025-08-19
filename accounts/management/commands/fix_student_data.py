from django.core.management.base import BaseCommand
from accounts.models import StudentProfile, TutorProfile, Course, User, Department
from django.db import transaction

class Command(BaseCommand):
    help = 'Fix missing student data - assign tutors and add course descriptions'

    def handle(self, *args, **options):
        self.stdout.write("🔧 Fixing student data...")
        
        with transaction.atomic():
            # Fix course descriptions first
            self.fix_course_descriptions()
            
            # Ensure we have a tutor
            self.ensure_tutor_exists()
            
            # Fix student 6 specifically
            self.fix_student_6()
        
        self.stdout.write(self.style.SUCCESS("✨ Data fix completed!"))
    
    def fix_course_descriptions(self):
        """Add descriptions to courses that don't have them"""
        self.stdout.write("📚 Fixing course descriptions...")
        
        courses = Course.objects.filter(description__in=['', None])
        
        course_descriptions = {
            'law': "Comprehensive law program covering legal theory, practice, and jurisprudence. Students study constitutional law, criminal law, civil law, and legal research methods.",
            'computer': "Computer Science program focusing on programming, algorithms, data structures, software engineering, and emerging technologies.",
            'cs': "Computer Science program focusing on programming, algorithms, data structures, software engineering, and emerging technologies.",
            'business': "Business administration program covering management, finance, marketing, operations, and strategic planning.",
            'engineering': "Engineering program with focus on technical skills, problem-solving, design thinking, and practical applications.",
            'medicine': "Medical program providing comprehensive healthcare education including anatomy, physiology, pathology, and clinical practice.",
            'science': "Science program covering fundamental scientific principles, research methods, and practical laboratory skills.",
        }
        
        for course in courses:
            # Find matching description
            description = None
            for keyword, desc in course_descriptions.items():
                if keyword.lower() in course.name.lower() or keyword.lower() in course.code.lower():
                    description = desc
                    break
            
            if not description:
                description = f"Comprehensive {course.name} program designed to provide students with theoretical knowledge and practical skills in their field of study."
            
            course.description = description
            course.save()
            self.stdout.write(f"✅ {course.code}: {description[:80]}...")
    
    def ensure_tutor_exists(self):
        """Ensure there's at least one tutor in the system"""
        self.stdout.write("👨‍🏫 Checking tutors...")
        
        tutors = TutorProfile.objects.all()
        if tutors.exists():
            self.stdout.write(f"✅ Found {tutors.count()} tutors")
            return
        
        self.stdout.write("⚠️ No tutors found. Creating sample tutor...")
        
        # Create a department if none exists
        department, created = Department.objects.get_or_create(
            code='CS',
            defaults={
                'name': 'Computer Science',
                'description': 'Department of Computer Science and Technology'
            }
        )
        
        # Create a tutor user
        tutor_user, created = User.objects.get_or_create(
            username='dr_smith',
            defaults={
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'dr.smith@university.edu',
                'user_type': 'tutor',
                'is_verified': True
            }
        )
        
        if created:
            tutor_user.set_password('password123')
            tutor_user.save()
        
        # Create tutor profile
        tutor_profile, created = TutorProfile.objects.get_or_create(
            user=tutor_user,
            defaults={
                'employee_id': 'TUT001',
                'department': department,
                'designation': 'Assistant Professor',
                'office_location': 'CS Building, Room 201'
            }
        )
        
        if created:
            self.stdout.write("✅ Created sample tutor: Dr. John Smith")
    
    def fix_student_6(self):
        """Fix specific data for student 6"""
        self.stdout.write("🎓 Fixing student 6 data...")
        
        try:
            student = StudentProfile.objects.get(pk=6)
            self.stdout.write(f"📚 Student: {student.user.get_full_name()}")
            
            # Assign tutor if not assigned
            if not student.tutor:
                tutor = TutorProfile.objects.first()
                if tutor:
                    student.tutor = tutor
                    student.save()
                    self.stdout.write(f"✅ Assigned tutor: {tutor.user.get_full_name()}")
            
            # Add phone number if missing
            if not student.user.phone:
                student.user.phone = '+1234567890'
                student.user.save()
                self.stdout.write("✅ Added sample phone number")
            
            # Add address if missing
            if not student.address:
                student.address = '123 University Street, Campus City, State 12345'
                student.save()
                self.stdout.write("✅ Added sample address")
            
            # Add CGPA if missing
            if not student.cgpa:
                student.cgpa = 3.0
                student.save()
                self.stdout.write("✅ Added sample CGPA")
            
            self.stdout.write("✅ Student 6 data fixed!")
            
        except StudentProfile.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Student 6 not found!"))
